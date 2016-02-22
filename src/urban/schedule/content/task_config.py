# -*- coding: utf-8 -*-

from plone import api
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model

from urban.schedule import _
from urban.schedule.content.task import IAutomatedTask
from urban.schedule.interfaces import IDefaultTaskUser
from urban.schedule.interfaces import ICreationCondition
from urban.schedule.interfaces import IEndCondition
from urban.schedule.interfaces import IStartCondition
from urban.schedule.interfaces import IStartDate
from urban.schedule.interfaces import TaskAlreadyExists

from zope import schema
from zope.component import getAdapter
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import implements


class ITaskConfig(model.Schema):
    """
    TaskConfig dexterity schema.
    """
    enabled = schema.Bool(
        title=_(u'Enabled'),
        default=True,
        required=False,
    )

    default_assigned_user = schema.Choice(
        title=_(u'Assigned user'),
        description=_(u'Select default user assigned to this task.'),
        vocabulary='schedule.assigned_user',
        required=True,
    )

    creation_state = schema.Choice(
        title=_(u'Task container creation state'),
        description=_(u'Select the state of the container where the task is automatically created.'),
        vocabulary='schedule.container_state',
        required=False,
    )

    creation_conditions = schema.List(
        title=_(u'Creation conditions'),
        description=_(u'Select creation conditions of the task'),
        value_type=schema.Choice(source='schedule.creation_conditions'),
        required=True,
    )

    starting_states = schema.Choice(
        title=_(u'Task container start states'),
        description=_(u'Select the state of the container where the task is automatically started.'),
        vocabulary='schedule.container_state',
        required=False,
    )

    start_conditions = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Choice(source='schedule.start_conditions'),
        required=True,
    )

    ending_states = schema.Set(
        title=_(u'Task container end states'),
        description=_(u'Select the states of the container where the task is automatically closed.'),
        value_type=schema.Choice(source='schedule.container_state'),
        required=False,
    )

    end_conditions = schema.List(
        title=_(u'End conditions'),
        description=_(u'Select end conditions of the task.'),
        value_type=schema.Choice(source='schedule.end_conditions'),
        required=True,
    )

    start_date = schema.Choice(
        title=_(u'Start date'),
        description=_(u'Select the start date used to compute the due date.'),
        vocabulary='schedule.start_date',
        required=True,
    )

    additional_delay = schema.Int(
        title=_(u'Additional delay'),
        description=_(u'This delay is added to the due date of the task.'),
        required=False,
    )

    warning_delay = schema.Int(
        title=_(u'Warning delay'),
        required=False,
    )


class BaseTaskConfig(object):
    """
    TaskConfig dexterity class.
    """

    def get_task_type(self):
        """
        To override.
        Return the content type of task to create.
        """

    def is_main_taskconfig(self):
        """
        Tells wheter this task config is a sub task or not.
        """
        return self.getParentNode() is self.get_schedule_config()

    def get_schedule_config(self):
        """
        Return the parent ScheduleConfig.
        """
        from urban.schedule.content.schedule_config import IScheduleConfig

        context = self
        while(not IScheduleConfig.providedBy(context)):
            context = context.getParentNode()

        return context

    def get_scheduled_portal_type(self):
        """
        Return the portal_type of the selected scheduled_contenttype.
        """
        schedule_config = self.get_schedule_config()
        return schedule_config.get_scheduled_portal_type()

    def get_scheduled_interface(self):
        """
        Return the registration interface of the selected scheduled_contenttype.
        """
        schedule_config = self.get_schedule_config()
        return schedule_config.get_scheduled_interface()

    def user_to_assign(self, task_container, task):
        """
        Returns a default user to assign to the AutomatedTask.
        """
        # the value could be either the name of an adapter to call or the id
        # of an existing user
        user_id = self.default_assigned_user
        # try to get the adapter named 'user_id'
        assign_user = queryMultiAdapter(
            (task_container, task),
            IDefaultTaskUser,
            name=user_id
        )
        if assign_user:
            default_user = assign_user.user_id()

        # if no user was found use user_id
        user_id = default_user or user_id
        return user_id

    def query_task_instances(self, root_container, states=[], the_objects=False):
        """
        Catalog query to return every AutomatedTask created
        from this TaskConfig contained in 'root_container'.
        """
        catalog = api.portal.get_tool('portal_catalog')

        query = {
            'object_provides': IAutomatedTask.__identifier__,
            'path': {'query': '/'.join(root_container.getPhysicalPath())},
            'task_config_UID': self.UID()
        }
        if states:
            query['review_state'] = states

        task_brains = catalog(**query)

        if the_objects:
            return [brain.getObject() for brain in task_brains]

        return task_brains

    def get_task(self, task_container):
        """
        Return the unique AutomatedTask object created from this
        TaskConfig in 'task_container' if it exists.
        """
        tasks = self.query_task_instances(task_container)
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def get_created_task(self, task_container):
        """
        Return the unique AutomatedTask object created from this
        TaskConfig in 'task_container' if it exists and is not started yet..
        """
        tasks = self.query_task_instances(
            task_container,
            states=['created', 'to_assign']
        )
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def get_started_task(self, task_container):
        """
        Return the unique AutomatedTask object created from this
        TaskConfig in 'task_container' if it exists and is started.
        """
        tasks = self.query_task_instances(
            task_container,
            states=['to_do', 'in_progress', 'realized']
        )
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def get_open_task(self, task_container):
        """
        Return the unique AutomatedTask object created from this
        TaskConfig in 'task_container' if it exists and is not closed yet.
        """
        tasks = self.query_task_instances(
            task_container,
            states=['created', 'to_assign', 'to_do', 'in_progress', 'realized']
        )
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def get_closed_task(self, task_container):
        """
        Return the unique AutomatedTask object created from this
        TaskConfig in 'task_container' if it exists and is closed.
        """
        tasks = self.query_task_instances(
            task_container,
            states='closed'
        )
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def task_already_exists(self, task_container):
        """
        Check if the task_container already has a task from this config.
        """
        return self.query_task_instances(task_container)

    def should_create_task(self, task_container):
        """
        Evaluate:
         - If the task container is on the state selected on 'starting_states'
         - All the creation conditions of a task with 'kwargs'.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically create a task.
        """
        # config should be enabled
        if not self.enabled:
            return False

        # does the Task already exists?
        if self.task_already_exists(task_container):
            return False

        # task container state match creation_state value?
        if api.content.get_state(task_container) != self.creation_state:
            return False

        # each conditions is matched?
        for condition_name in self.creation_conditions or []:
            condition = getAdapter(
                task_container,
                interface=ICreationCondition,
                name=condition_name
            )
            if not condition.evaluate():
                return False

        return True

    def should_start_task(self, task_container, task):
        """
        Evaluate:
         - If the task container is on the state selected on 'starting_states'
         - All the starting conditions of a task with 'kwargs'.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically start a task.
        """

        # task container state match starting_states value?
        if api.content.get_state(task_container) not in (self.starting_states or []):
            return False

        # each conditions is matched?
        for condition_name in self.start_conditions or []:
            condition = getMultiAdapter(
                (task_container, task),
                interface=IStartCondition,
                name=condition_name
            )
            if not condition.evaluate():
                return False

        return True

    def should_end_task(self, task_container, task):
        """
        Evaluate:
         - If the task container is on the state selected on 'ending_states'
         - All the existence conditions of a task.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically close a task.
        """

        # task container state match any ending_states value?
        if api.content.get_state(task_container) not in (self.ending_states or []):
            return False

        # each conditions is matched?
        for condition_name in self.end_conditions or []:
            condition = getMultiAdapter(
                (task_container, task),
                interface=IEndCondition,
                name=condition_name
            )
            if not condition.evaluate():
                return False

        return True

    def create_task(self, task_container):
        """
        To implements in subclasses.
        """

    def start_task(self, task):
        """
        Default implementation is to put the task on the state 'to_do'.
        """
        if api.content.get_state(task) == 'created':
            api.content.transition(obj=task, transition='do_to_assign')
        if api.content.get_state(task) == 'to_assign' and task.assigned_user:
            api.content.transition(obj=task, transition='do_to_do')

    def end_task(self, task):
        """
        Default implementation is to put the task on the state 'closed'.
        """
        if api.content.get_state(task) == 'created':
            api.content.transition(obj=task, transition='do_to_assign')
        if api.content.get_state(task) == 'to_assign':
            api.content.transition(obj=task, transition='do_to_do')
        if api.content.get_state(task) == 'to_do':
            api.content.transition(obj=task, transition='do_realized')
        if api.content.get_state(task) == 'realized':
            api.content.transition(obj=task, transition='do_closed')

    def compute_due_date(self, task_container, task):
        """
        Evaluate 'task_container' and 'task' to compute the due date of a task.
        This should be checked in a zope event to automatically compute and set the
        due date of 'task'.
        """
        date_adapter = getMultiAdapter(
            (task_container, task),
            interface=IStartDate,
            name=self.start_date
        )
        start_date = date_adapter.start_date()
        if not start_date:
            return None

        additional_delay = self.additional_delay or 0
        due_date = start_date + additional_delay
        due_date = due_date.asdatetime().date()

        return due_date

    def _create_task_instance(self, creation_place):
        """
        Helper method to use to implement 'create_task'.
        """
        task_id = 'TASK_{}'.format(self.id)

        if task_id in creation_place.objectIds():
            raise TaskAlreadyExists(task_id)

        task_portal_type = self.get_task_type()
        portal_types = api.portal.get_tool('portal_types')
        type_info = portal_types.getTypeInfo(task_portal_type)

        task = type_info._constructInstance(
            container=creation_place,
            id=task_id,
            title=self.Title(),
            schedule_config_UID=self.get_schedule_config().UID(),
            task_config_UID=self.UID(),
        )
        return task


class TaskConfig(Item, BaseTaskConfig):
    """
    TaskConfig dexterity class.
    """

    implements(ITaskConfig)

    def get_task_type(self):
        """
        Return the content type of task to create.
        """
        return 'AutomatedTask'

    def create_task(self, task_container, creation_place=None):
        """
        Just create the task and return it.
        """
        creation_place = creation_place or task_container
        task = self._create_task_instance(creation_place)

        task.due_date = self.compute_due_date(task_container, task)
        task.assigned_user = self.user_to_assign(task_container, task)

        return task


class IMacroTaskConfig(ITaskConfig):
    """
    TaskConfig dexterity schema.
    """

    creation_conditions = schema.List(
        title=_(u'Creation conditions'),
        description=_(u'Select creation conditions of the task'),
        value_type=schema.Choice(source='schedule.macrotask_creation_conditions'),
        required=True,
    )

    starting_states = schema.Choice(
        title=_(u'Task container start states'),
        description=_(u'Select the state of the container where the task is automatically started.'),
        vocabulary='schedule.container_state',
        required=False,
    )

    start_conditions = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Choice(source='schedule.macrotask_start_conditions'),
        required=True,
    )

    ending_states = schema.Set(
        title=_(u'Task container end states'),
        description=_(u'Select the states of the container where the task is automatically closed.'),
        value_type=schema.Choice(source='schedule.container_state'),
        required=False,
    )

    end_conditions = schema.List(
        title=_(u'End conditions'),
        description=_(u'Select end conditions of the task.'),
        value_type=schema.Choice(source='schedule.macrotask_end_conditions'),
        required=True,
    )

    start_date = schema.Choice(
        title=_(u'Start date'),
        description=_(u'Select the start date used to compute the due date.'),
        vocabulary='schedule.macrotask_start_date',
        required=True,
    )

    additional_delay = schema.Int(
        title=_(u'Additional delay'),
        description=_(u'This delay is added to the due date of the task.'),
        required=False,
    )

    warning_delay = schema.Int(
        title=_(u'Warning delay'),
        required=False,
    )


class MacroTaskConfig(Container, BaseTaskConfig):
    """
    MacroTaskConfig dexterity class.
    """

    implements(IMacroTaskConfig)

    def get_task_type(self):
        """
        Return the content type of task to create.
        """
        return 'AutomatedMacroTask'

    def get_subtask_configs(self):
        """
        Return all the subtasks configs of this macro task.
        """
        return self.objectValues()

    def create_task(self, task_container):
        """
        Create the macrotask and subtasks.
        """
        macrotask = self._create_task_instance(task_container)

        for config in self.get_subtask_configs():
            if config.should_create_task(task_container):
                config.create_task(task_container, creation_place=macrotask)

        # compute due date only after all substasks are created
        macrotask.due_date = self.compute_due_date(task_container, macrotask)
        macrotask.assigned_user = self.user_to_assign(task_container, macrotask)

        return macrotask

    def should_end_task(self, task_container, task):
        """
        See 'should_end_task' in BaseTaskConfig
        Evaluate:
         - If the task container is on the state selected on 'ending_states'
         - All the existence conditions of a task with 'task' and 'kwargs'.
           Returns True only if ALL the conditions are matched.
         - If all the subtasks are ended.
        This should be checked in a zope event to automatically close a task.
        """
        task_done = super(MacroTaskConfig, self).should_end_task(task_container, task)
        if not task_done:
            return False

        subtasks_done = all([subtask.is_done() for subtask in task.get_subtasks()])
        if not subtasks_done:
            return False

        return True

    def end_task(self, task):
        """
        Default implementation is to put the task on the state 'closed'.
        """
        if api.content.get_state(task) == 'created':
            api.content.transition(obj=task, transition='do_to_assign')
        if api.content.get_state(task) == 'to_assign':
            api.content.transition(obj=task, transition='do_to_do')
        if api.content.get_state(task) == 'to_do':
            api.content.transition(obj=task, transition='do_realized')
        if api.content.get_state(task) == 'realized':
            api.content.transition(obj=task, transition='do_closed')

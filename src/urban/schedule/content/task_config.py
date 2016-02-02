# -*- coding: utf-8 -*-

from plone import api
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model

from urban.schedule import _
from urban.schedule.content.task import IScheduleTask
from urban.schedule.interfaces import IDueDate
from urban.schedule.interfaces import IEndCondition
from urban.schedule.interfaces import IStartCondition
from urban.schedule.interfaces import IDefaultTaskUser

from zope import schema
from zope.component import getAdapter
from zope.component import queryAdapter
from zope.interface import implements


class ITaskConfig(model.Schema):
    """
    TaskConfig dexterity schema.
    """

    default_assigned_user = schema.Choice(
        title=_(u'Assigned user'),
        description=_(u'Select default user assigned to this task.'),
        vocabulary='urban.schedule.assigned_user',
        required=True,
    )

    starting_state = schema.Choice(
        title=_(u'Task container start state'),
        description=_(u'Select the state of the container where the task is automatically created.'),
        vocabulary='urban.schedule.container_state',
        required=False,
    )

    start_conditions = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Choice(source='urban.schedule.start_conditions'),
        required=True,
    )

    ending_states = schema.Set(
        title=_(u'Task container end states'),
        description=_(u'Select the states of the container where the task is automatically closed.'),
        value_type=schema.Choice(source='urban.schedule.container_state'),
        required=False,
    )

    end_conditions = schema.List(
        title=_(u'End conditions'),
        description=_(u'Select end conditions of the task.'),
        value_type=schema.Choice(source='urban.schedule.end_conditions'),
        required=True,
    )

    due_date_computation = schema.Choice(
        title=_(u'Due date'),
        description=_(u'Select how to compute the due date.'),
        vocabulary='urban.schedule.due_date',
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

    def user_to_assign(self, task_container):
        """
        Returns a default user to assign to the ScheduleTask.
        """
        # the value could be either the name of an adapter to call or the id
        # of an existing user
        user_id = self.default_assigned_user
        # try to get the adapter named 'user_id'
        assign_user = queryAdapter(task_container, IDefaultTaskUser, name=user_id)
        if assign_user:
            return assign_user.user_id()
        # else just return user_id
        return user_id

    def query_task_instances(self, root_container, states=[], the_objects=False):
        """
        Catalog query to return every ScheduleTask created
        from this TaskConfig contained in 'root_container'.
        """
        catalog = api.portal.get_tool('portal_catalog')

        query = {
            'object_provides': IScheduleTask.__identifier__,
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
        Return the unique ScheduleTask object created from this
        TaskConfig in 'task_container' if it exists.
        """
        tasks = self.query_task_instances(task_container)
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def get_open_task(self, task_container):
        """
        Return the unique ScheduleTask object created from this
        TaskConfig in 'task_container' if it exists and is open.
        """
        tasks = self.query_task_instances(
            task_container,
            states=['created', 'to_assign', 'realized']
        )
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def get_closed_task(self, task_container):
        """
        Return the unique ScheduleTask object created from this
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

    def should_start_task(self, task_container):
        """
        Evaluate:
         - If the task container is on the state selected on 'starting_state'
         - All the existence conditions of a task with 'kwargs'.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically create a task.
        """

        # does the Task already exists?
        if self.task_already_exists(task_container):
            return False

        # task container state match starting_state value?
        if api.content.get_state(task_container) != self.starting_state:
            return False

        # each conditions is matched?
        for condition_name in self.start_conditions or []:
            condition = getAdapter(
                task_container,
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
         - All the existence conditions of a task with 'task' and 'kwargs'.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically close a task.
        """

        # task container state match any ending_states value?
        if api.content.get_state(task_container) not in self.ending_states:
            return False

        # each conditions is matched?
        for condition_name in self.end_conditions or []:
            condition = getAdapter(
                task_container,
                interface=IEndCondition,
                name=condition_name
            )
            if not condition.evaluate(task):
                return False

        return True

    def end_task(self, task):
        """
        Default implementation is to put the task on the state 'closed'.
        """
        if api.content.get_state(task) == 'created':
            api.content.transition(obj=task, transition='do_to_assign')
        if api.content.get_state(task) == 'to_do':
            api.content.transition(obj=task, transition='do_realized')
        if api.content.get_state(task) == 'realized':
            api.content.transition(obj=task, transition='do_closed')

    def compute_due_date(self, task_container):
        """
        Evaluate 'task_container' and 'kwargs' to compute the due date of a task.
        This should be checked in a zope event to automatically compute and set the
        due date of 'task'.
        """
        date_adapter = getAdapter(
            task_container,
            interface=IDueDate,
            name=self.due_date_computation
        )
        base_due_date = date_adapter.due_date()
        additional_delay = self.additional_delay or 0
        due_date = base_due_date + additional_delay
        due_date = due_date.asdatetime().date()

        return due_date


class TaskConfig(Item, BaseTaskConfig):
    """
    TaskConfig dexterity class.
    """

    implements(ITaskConfig)

    def get_task_type(self):
        """
        Return the content type of task to create.
        """
        return 'ScheduleTask'


class MacroTaskConfig(Container, BaseTaskConfig):
    """
    TaskConfig dexterity class.
    """

    implements(ITaskConfig)

    def evaluate_end_condition(self, task, **kwargs):
        """
        Evaluate 'task' and 'kwargs' to return the boolean end condition of a task.
        This should be checked in a zope event to automatically close/reopen a task.
        Also checks subtasks of this task.
        """
        task_done = super(MacroTaskConfig, self).evaluate_end_condition()
        if not task_done:
            return False

        subtasks_done = all([subtask.is_done() for subtask in task.get_subtasks()])
        if not subtasks_done:
            return False

        return True

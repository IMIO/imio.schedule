# -*- coding: utf-8 -*-

from imio.schedule import _
from imio.schedule.config import CREATION
from imio.schedule.config import DONE
from imio.schedule.config import STARTED
from imio.schedule.config import states_by_status
from imio.schedule.content.task import IAutomatedTask
from imio.schedule.content.subform_context_choice import SubFormContextChoice
from imio.schedule.interfaces import ICreationCondition
from imio.schedule.interfaces import IDefaultTaskGroup
from imio.schedule.interfaces import IDefaultTaskUser
from imio.schedule.interfaces import IEndCondition
from imio.schedule.interfaces import IStartCondition
from imio.schedule.interfaces import TaskAlreadyExists
from imio.schedule.interfaces import ICalculationDelay

from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model

from zope import schema
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.component.interface import getInterface
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.interface import implements


class ICreationConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.creation_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class IStartConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.start_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class IEndConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.end_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class IRecurrenceConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.creation_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class ITaskConfig(model.Schema):
    """
    TaskConfig dexterity schema.
    """

    model.fieldset(
        'general',
        label=_(u"General informations"),
        fields=[
            'enabled', 'start_date',
            'warning_delay', 'default_assigned_group',
            'default_assigned_user', 'marker_interfaces'
        ]
    )

    enabled = schema.Bool(
        title=_(u'Enabled'),
        default=True,
        required=False,
    )

    start_date = schema.Choice(
        title=_(u'Start date'),
        description=_(u'Select the start date used to compute the due date.'),
        vocabulary='schedule.start_date',
        required=True,
    )

    warning_delay = schema.Int(
        title=_(u'Warning delay'),
        required=False,
    )

    default_assigned_group = schema.Choice(
        title=_(u'Assigned group'),
        description=_(u'Select default group assigned to this task.'),
        vocabulary='schedule.assigned_group',
        required=False,
    )

    default_assigned_user = schema.Choice(
        title=_(u'Assigned user'),
        description=_(u'Select default user assigned to this task.'),
        vocabulary='schedule.assigned_user',
        required=True,
    )

    marker_interfaces = schema.Set(
        title=_(u'Marker interfaces'),
        description=_(u'Custom marker interfaces for this task.'),
        value_type=schema.Choice(source='schedule.task_marker_interfaces'),
        required=False,
    )

    model.fieldset(
        'creation',
        label=_(u"Creation"),
        fields=['creation_state', 'creation_conditions']
    )

    creation_state = schema.Set(
        title=_(u'Task container creation state'),
        description=_(u'Select the state of the container where the task is automatically created.'),
        value_type=schema.Choice(source='schedule.container_state'),
        required=False,
    )

    creation_conditions = schema.List(
        title=_(u'Creation conditions'),
        description=_(u'Select creation conditions of the task'),
        value_type=schema.Object(
            title=_(u'Conditions'),
            schema=ICreationConditionSchema,
        ),
        required=False,
    )

    model.fieldset(
        'start',
        label=_(u"Start"),
        fields=['starting_states', 'start_conditions']
    )

    starting_states = schema.Set(
        title=_(u'Task container start states'),
        description=_(u'Select the state of the container where the task is automatically started.'),
        value_type=schema.Choice(source='schedule.container_state'),
        required=False,
    )

    start_conditions = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Object(
            title=_(u'Conditions'),
            schema=IStartConditionSchema,
        ),
        required=False,
    )

    model.fieldset(
        'ending',
        label=_(u"Ending"),
        fields=['ending_states', 'end_conditions']
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
        value_type=schema.Object(
            title=_(u'Conditions'),
            schema=IEndConditionSchema,
        ),
        required=False,
    )

    model.fieldset(
        'delay',
        label=_(u'Calculation delay'),
        fields=['calculation_delay'],
    )

    calculation_delay = schema.List(
        title=_(u'Calculation delay method'),
        value_type=schema.Choice(
            title=_(u'Calculation delay'),
            vocabulary='schedule.calculation_delay',
            default='schedule.calculation_default_delay',
        ),
        required=True,
    )

    model.fieldset(
        'recurrence',
        label=_(u'Recurrence'),
        fields=[
            'activate_recurrency',
            'recurrence_states',
            'recurrence_conditions',
        ],
    )

    activate_recurrency = schema.Bool(
        title=_(u'Activate recurrency'),
        required=False,
        default=False,
    )

    recurrence_states = schema.Set(
        title=_(u'Task container recurrence states'),
        description=_(u'Select the state of the container where the task should be recurred'),
        value_type=schema.Choice(source='schedule.container_state'),
        required=False,
    )

    recurrence_conditions = schema.List(
        title=_(u'Recurrence condition'),
        description=_(u'Select recurrence conditions of the task.'),
        value_type=schema.Object(
            title=_('Conditions'),
            schema=IRecurrenceConditionSchema,
        ),
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

    def level(self):
        """
        Return depth contenance level.
        """
        level = self.aq_parent.level() + 1
        return level

    def is_main_taskconfig(self):
        """
        Tells wheter this task config is a sub task or not.
        """
        return self.level() == 1

    def get_schedule_config(self):
        """
        Return the parent ScheduleConfig.
        """
        from imio.schedule.content.schedule_config import IScheduleConfig

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

    def group_to_assign(self, task_container, task):
        """
        Returns a default group to assign to the AutomatedTask.
        """
        # the value could be either the name of an adapter to call or the id
        # of an existing group
        group_id = self.default_assigned_group
        # try to get the adapter named 'group_id'
        default_group = None
        assign_group = queryMultiAdapter(
            (task_container, task),
            IDefaultTaskGroup,
            name=group_id
        )
        if assign_group:
            default_group = assign_group.group_id()

        # if no group was found use group_id
        group_id = default_group or group_id
        return group_id

    def user_to_assign(self, task_container, task):
        """
        Returns a default user to assign to the AutomatedTask.
        """
        # the value could be either the name of an adapter to call or the id
        # of an existing user
        user_id = self.default_assigned_user
        # try to get the adapter named 'user_id'
        default_user = None
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

        task_brains = catalog.unrestrictedSearchResults(**query)

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
            states=states_by_status[CREATION]
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
            states=states_by_status[STARTED]
        )
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def get_open_task(self, task_container):
        """
        Return the unique AutomatedTask object created from this
        TaskConfig in 'task_container' if it exists and is not closed yet.
        """
        states = states_by_status[CREATION] + states_by_status[STARTED]
        tasks = self.query_task_instances(
            task_container,
            states=states
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
            states=states_by_status[DONE]
        )
        task_instance = tasks and tasks[0].getObject() or None
        return task_instance

    def task_already_exists(self, task_container):
        """
        Check if the task_container already has a task from this config.
        """
        return self.query_task_instances(task_container)

    def evaluate_conditions(self, conditions, to_adapt, interface):
        """
        """
        value = True
        for condition_object in conditions or []:
            value = self.evaluate_one_condition(
                to_adapt=to_adapt,
                interface=interface,
                name=condition_object.condition,
            )
            operator = condition_object.operator

            # in these cases, its useless to evaluate further because:
            # TRUE or (... ) <=> TRUE
            if operator == 'OR' and value is True:
                return True
            # FALSE and (... ) <=> FALSE
            elif operator == 'AND' and value is False:
                return False
            # else, just continue to loop to evaluate the rest of the expression because:
            # FALSE or (... ) <=> (... )
            # TRUE and (... ) <=> (... )
            # so only the remaining '(... )' expression is relevant

        # return the last value
        return value

    def evaluate_one_condition(self, to_adapt, interface, name):
        """
        """
        condition = getMultiAdapter(
            to_adapt,
            interface=interface,
            name=name
        )
        value = condition.evaluate() and True or False
        return value

    def get_conditions_status(self, conditions, to_adapt, interface):
        """
        Return two lists of all conditions status for a given task
        and task container.
        The first list is all the matched conditions, the second is
        all the unmatched conditions.
        """
        matched = []
        not_matched = []
        for condition_object in conditions or []:
            value = self.evaluate_one_condition(
                to_adapt=to_adapt,
                interface=interface,
                name=condition_object.condition,
            )
            if value:
                matched.append(condition_object.condition)
            else:
                not_matched.append(condition_object.condition)

        return matched, not_matched

    def should_create_task(self, task_container, parent_container=None):
        """
        Evaluate:
         - If the task container is on the state selected on 'starting_states'
         - All the creation conditions of a task with 'kwargs'.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically create a task.
        """
        # schedule config should be enabled
        schedule_config = self.get_schedule_config()
        if not schedule_config.enabled:
            return False

        # config should be enabled
        if not self.enabled:
            return False

        # does the Task already exists?
        if self.task_already_exists(parent_container or task_container):
            return False

        # task container state match creation_state value?
        if not self.match_creation_state(task_container):
            return False

        # each conditions is matched?
        if not self.match_creation_conditions(task_container):
            return False

        return True

    def match_creation_state(self, task_container):
        """
        """
        if not self.creation_state:
            return True

        container_state = api.content.get_state(task_container)
        return container_state in (self.creation_state or [])

    def match_creation_conditions(self, task_container):
        """
        """
        return self.evaluate_conditions(
            conditions=self.creation_conditions,
            to_adapt=(task_container, self),
            interface=ICreationCondition,
        )

    def should_start_task(self, task_container, task):
        """
        Evaluate:
         - If the task container is on the state selected on 'starting_states'
         - All the starting conditions of a task with 'kwargs'.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically start a task.
        """

        # task container state match starting_states value?
        if not self.match_starting_states(task_container):
            return False

        # each conditions is matched?
        if not self.match_start_conditions(task_container, task):
            return False

        if not task.assigned_user:
            return False

        return True

    def match_starting_states(self, task_container):
        """
        """
        if not self.starting_states:
            return True

        container_state = api.content.get_state(task_container)
        return container_state in (self.starting_states or [])

    def match_start_conditions(self, task_container, task):
        """
        """
        return self.evaluate_conditions(
            conditions=self.start_conditions,
            to_adapt=(task_container, task),
            interface=IStartCondition,
        )

    def start_conditions_status(self, task_container, task):
        """
        Return status of each start condition.
        """
        return self.get_conditions_status(
            conditions=self.start_conditions,
            to_adapt=(task_container, task),
            interface=IStartCondition,
        )

    def should_end_task(self, task_container, task):
        """
        Evaluate:
         - If the task has an assigned user
         - If the task container is on the state selected on 'ending_states'
         - All the existence conditions of a task.
           Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically close a task.
        """

        if not task.assigned_user:
            return False

        # task container state match any ending_states value?
        if not self.match_ending_states(task_container):
            return False

        if not self.match_end_conditions(task_container, task):
            return False

        return True

    def match_ending_states(self, task_container):
        """
        """
        if not self.ending_states:
            return True

        container_state = api.content.get_state(task_container)
        return container_state in (self.ending_states or [])

    def match_end_conditions(self, task_container, task):
        """
        """
        return self.evaluate_conditions(
            conditions=self.end_conditions,
            to_adapt=(task_container, task),
            interface=IEndCondition,
        )

    def end_conditions_status(self, task_container, task):
        """
        Return status of each end condition.
        """
        return self.get_conditions_status(
            conditions=self.end_conditions,
            to_adapt=(task_container, task),
            interface=IEndCondition,
        )

    def should_recurred(self, task_container):
        """
        Evaluate if the a new task should be created for the task container
        depending on the recurrence condition
        """
        # schedule config should be enabled
        schedule_config = self.get_schedule_config()
        if not schedule_config.enabled:
            return False

        if getattr(self, 'activate_recurrency', False) is False:
            return False

        if self.match_recurrence_states(task_container) is False:
            return False

        if not getattr(self, 'recurrence_conditions', None):
            return True

        return self.evaluate_conditions(
            conditions=self.recurrence_conditions,
            to_adapt=(task_container, self),
            interface=ICreationCondition,
        )

    def match_recurrence_states(self, task_container):
        """
        """
        if not self.recurrence_states:
            return True

        container_state = api.content.get_state(task_container)
        return container_state in (self.recurrence_states or [])

    def create_task(self, task_container):
        """
        To implements in subclasses.
        """

    def start_task(self, task):
        """
        Default implementation is to put the task on the state 'to_do'.
        """
        with api.env.adopt_roles(['Manager']):
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
            with api.env.adopt_roles(['Reviewer']):
                api.content.transition(obj=task, transition='do_closed')

    def compute_due_date(self, task_container, task):
        """
        Evaluate 'task_container' and 'task' to compute the due date of a task.
        This should be checked in a zope event to automatically compute and set the
        due date of 'task'.
        """
        adapters = getattr(self, 'calculation_delay', [])
        # Backward compatibility
        if not adapters:
            adapters = ['schedule.calculation_default_delay']
        due_date = None
        for adapter in adapters:
            calculator = getMultiAdapter(
                (task_container, task),
                interface=ICalculationDelay,
                name=adapter,
            )
            due_date = calculator.due_date

        return due_date

    def _create_task_instance(self, creation_place, task_id):
        """
        Helper method to use to implement 'create_task'.
        """
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

        marker_interfaces = [getInterface('', i) for i in self.marker_interfaces or []]
        alsoProvides(task, *marker_interfaces)

        return task

    @property
    def default_task_id(self):
        return 'TASK_{0}'.format(self.id)

    def create_recurring_task(self, task_container, creation_place=None):
        """
        Create a recurring task
        """
        creation_place = creation_place or task_container
        object_ids = creation_place.objectIds()
        related_ids = [i for i in object_ids
                       if i.startswith(self.default_task_id)]
        if len(related_ids) > 0:
            object_id = related_ids[-1]
            if api.content.get_state(creation_place[object_id]) != 'closed':
                return
        if self.default_task_id in object_ids:
            task_id = '{0}-{1}'.format(
                self.default_task_id,
                len(related_ids),
            )
        else:
            task_id = self.default_task_id
        return self.create_task(
            task_container,
            creation_place=creation_place,
            task_id=task_id,
        )


class TaskConfig(Container, BaseTaskConfig):
    """
    TaskConfig dexterity class.
    """

    implements(ITaskConfig)

    def get_task_type(self):
        """
        Return the content type of task to create.
        """
        return 'AutomatedTask'

    def create_task(self, task_container, creation_place=None, task_id=None):
        """
        Just create the task and return it.
        """
        creation_place = creation_place or task_container
        task_id = task_id or self.default_task_id
        task = self._create_task_instance(creation_place, task_id)

        task.assigned_group = self.group_to_assign(task_container, task)
        task.assigned_user = self.user_to_assign(task_container, task)
        task.due_date = self.compute_due_date(task_container, task)
        task.reindexObject()

        return task


class IMacroCreationConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.macrotask_creation_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class IMacroStartConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.macrotask_start_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class IMacroEndConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.macrotask_end_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class IMacroRecurrenceConditionSchema(Interface):

    condition = SubFormContextChoice(
        title=_(u'Condition'),
        vocabulary='schedule.macrotask_creation_conditions',
        # vocabulary='schedule.recurrence_conditions',
        required=True,
    )

    operator = schema.Choice(
        title=_(u'Operator'),
        vocabulary='schedule.logical_operator',
        default='AND',
    )


class IMacroTaskConfig(ITaskConfig):
    """
    TaskConfig dexterity schema.
    """

    start_date = schema.Choice(
        title=_(u'Start date'),
        description=_(u'Select the start date used to compute the due date.'),
        vocabulary='schedule.macrotask_start_date',
        required=True,
    )

    creation_conditions = schema.List(
        title=_(u'Creation conditions'),
        description=_(u'Select creation conditions of the task'),
        value_type=schema.Object(
            title=_(u'Conditions'),
            schema=IMacroCreationConditionSchema,
        ),
        required=False,
    )

    start_conditions = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Object(
            title=_(u'Conditions'),
            schema=IMacroStartConditionSchema,
        ),
        required=False,
    )

    end_conditions = schema.List(
        title=_(u'End conditions'),
        description=_(u'Select end conditions of the task.'),
        value_type=schema.Object(
            title=_(u'Conditions'),
            schema=IMacroEndConditionSchema,
        ),
        required=False,
    )

    recurrence_conditions = schema.List(
        title=_(u'Recurrence condition'),
        description=_(u'Select recurrence conditions of the task.'),
        value_type=schema.Object(
            title=_('Conditions'),
            schema=IMacroRecurrenceConditionSchema,
        ),
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
        catalog = api.portal.get_tool('portal_catalog')
        config_path = '/'.join(self.getPhysicalPath())

        query = {
            'object_provides': ITaskConfig.__identifier__,
            'path': {'query': config_path, 'depth': 1},
            'sort_on': 'getObjPositionInParent',
        }

        config_brains = catalog(**query)
        subtask_configs = [brain.getObject() for brain in config_brains]

        return subtask_configs

    def create_task(self, task_container, creation_place=None, task_id=None):
        """
        Create the macrotask and subtasks.
        """
        creation_place = creation_place or task_container
        task_id = task_id or self.default_task_id
        macrotask = self._create_task_instance(creation_place, task_id)

        for config in self.get_subtask_configs():
            if config.should_create_task(task_container):
                config.create_task(task_container, creation_place=macrotask)

        # compute some fields only after all substasks are created
        macrotask.assigned_group = self.group_to_assign(task_container, macrotask)
        macrotask.assigned_user = self.user_to_assign(task_container, macrotask)
        macrotask.due_date = self.compute_due_date(task_container, macrotask)
        macrotask.reindexObject()

        return macrotask

    def should_end_task(self, task_container, task):
        """
        See 'should_end_task' in BaseTaskConfig
        Evaluate:
         - If the task has an assigned user
         - If the task container is on the state selected on 'ending_states'
         - All the existence conditions of a task with 'task' and 'kwargs'.
           Returns True only if ALL the conditions are matched.
         - If all the subtasks are ended.
        This should be checked in a zope event to automatically close a task.
        """
        task_done = super(MacroTaskConfig, self).should_end_task(task_container, task)
        if not task_done:
            return False

        subtasks_done = all([subtask.get_status() == DONE for subtask in task.get_subtasks()])
        if not subtasks_done:
            return False

        return True

# -*- coding: utf-8 -*-

from plone import api
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model

from urban.schedule import _
from urban.schedule.content.task import IScheduleTask
from urban.schedule.interfaces import IEndCondition
from urban.schedule.interfaces import IStartCondition

from zope import schema
from zope.component import getAdapter
from zope.interface import implements


class ITaskConfig(model.Schema):
    """
    TaskConfig dexterity schema.
    """

    start_conditions = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Choice(source='urban.schedule.start_conditions'),
        required=True,
    )

    starting_state = schema.Choice(
        title=_(u'Task container start state'),
        description=_(u'Select the state of the container where the task is automatically created.'),
        vocabulary='urban.schedule.container_state',
        required=False,
    )

    end_conditions = schema.List(
        title=_(u'End conditions'),
        description=_(u'Select end conditions of the task.'),
        value_type=schema.Choice(source='urban.schedule.end_conditions'),
        required=True,
    )

    ending_states = schema.Set(
        title=_(u'Task container end states'),
        description=_(u'Select the states of the container where the task is automatically closed.'),
        value_type=schema.Choice(source='urban.schedule.container_state'),
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

    def query_task_instances(self, root_container, the_objects=False):
        """
        Catalog query to return every ScheduleTask created
        from this TaskConfig contained in 'root_container'.
        """
        catalog = api.portal.get_tool('portal_catalog')

        task_brains = catalog(
            object_provides=IScheduleTask.__identifier__,
            path={'query': '/'.join(root_container.getPhysicalPath())},
            task_config_UID=self.UID()
        )

        if the_objects:
            return [brain.getObject() for brain in task_brains]

        return task_brains

    def task_already_exists(self, task_container):
        """
        Check if the task_container already has a task from this config.
        """
        return self.query_task_instances(task_container)

    def should_start_task(self, task_container, **kwargs):
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

        # task container state is allowed?
        if api.content.get_state(task_container) != self.starting_state:
            return False

        # each conditions is macthed?
        for condition_name in self.start_conditions or []:
            condition = getAdapter(
                task_container,
                interface=IStartCondition,
                name=condition_name
            )
            if not condition.evaluate(**kwargs):
                return False

        return True

    def should_end_task(self, task_container, task, **kwargs):
        """
        Evaluate all the end conditions of a task with 'kwargs'.
        Returns True only if ALL the conditions are matched.
        This should be checked in a zope event to automatically close/reopen a task.
        """

        for condition_name in self.end_conditions or []:
            condition = getAdapter(
                task_container,
                interface=IEndCondition,
                name=condition_name
            )
            if not condition.evaluate(task, **kwargs):
                return False

        return True

    def compute_due_date(self, task, **kwargs):
        """
        Evaluate 'task' and 'kwargs' to compute the due date of a task.
        This should be checked in a zope event to automatically compute and set the
        due date of 'task'.
        """


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

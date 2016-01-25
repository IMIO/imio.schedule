# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model

from urban.schedule import _
from urban.schedule.content.schedule_config import IScheduleConfig

from zope import schema
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

    def get_schedule_config(self):
        """
        """
        context = self
        while(not IScheduleConfig.providedBy(context)):
            context = context.aq_parent

        return context

    def get_scheduled_portal_type(self):
        """
        Return the portal_type of the selected task_container.
        """
        schedule_config = self.get_schedule_config()
        return schedule_config.get_scheduled_portal_type()

    def get_scheduled_interface(self):
        """
        Return the registration interface of the selected task_container.
        """
        schedule_config = self.get_schedule_config()
        return schedule_config.get_scheduled_interface()

    def evaluate_start_condition(self, **kwargs):
        """
        Evaluate 'kwargs' to return the boolean condition of existence of a task.
        This should be checked in a zope event to automatically create a task.
        """

    def evaluate_end_condition(self, task, **kwargs):
        """
        Evaluate 'task' and 'kwargs' to return the boolean end condition of a task.
        This should be checked in a zope event to automatically close/reopen a task.
        """

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

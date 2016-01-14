# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model

from urban.schedule import _

from zope import schema
from zope.interface import implements


class ITaskConfig(model.Schema):
    """
    PODTemplate dexterity schema.
    """

    start_condition = schema.Choice(
        title=_(u'Start condition'),
        required=True,
    )

    end_condition = schema.Choice(
        title=_(u'End condition'),
        required=True,
    )

    allowed_states = schema.Choice(
        title=_(u'Allowed states'),
        required=True,
    )


class BaseTaskConfig(object):
    """
    PODTemplate dexterity class.
    """

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
    PODTemplate dexterity class.
    """

    implements(ITaskConfig)


class ConfigurableTaskConfig(Container, BaseTaskConfig):
    """
    PODTemplate dexterity class.
    """

    implements(ITaskConfig)

    def evaluate_end_condition(self, task, **kwargs):
        """
        Evaluate 'task' and 'kwargs' to return the boolean end condition of a task.
        This should be checked in a zope event to automatically close/reopen a task.
        All
        """
        task_done = super(ConfigurableTaskConfig, self).evaluate_end_condition()
        if not task_done:
            return False

        subtasks_done = all([subtask.is_done() for subtask in task.get_subtasks()])
        if not subtasks_done:
            return False

        return True

# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.formwidget.masterselect import MasterSelectField
from plone.supermodel import model

from urban.schedule import _

from zope import schema
from zope.interface import implements


def get_states_vocabulary(selected_content_type):
    """
    Return workflow states of the selected content type
    in the MasterSelectField 'content_type' as a vocabulary
    for the slave field 'allowed_states'.
    """


class ITaskConfig(model.Schema):
    """
    TaskConfig dexterity schema.
    """

    content_type = MasterSelectField(
        title=_(u'Task container content type'),
        description=_(u'Select the content type where the task will be created.'),
        vocabulary='urban.schedule.content_type',
        slave_fields=(
            {
                'name': 'allowed_states',
                'action': 'vocabulary',
                'vocab_method': get_states_vocabulary,
                'control_param': 'selected_content_type',
            },
        ),
        required=True,
    )

    start_condition = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Choice(source='urban.schedule.start_conditions'),
        required=True,
    )

    end_condition = schema.List(
        title=_(u'End conditions'),
        description=_(u'Select end conditions of the task.'),
        value_type=schema.Choice(source='urban.schedule.end_conditions'),
        required=True,
    )


class BaseTaskConfig(object):
    """
    TaskConfig dexterity class.
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

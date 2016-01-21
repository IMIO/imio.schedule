# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.formwidget.masterselect import MasterSelectField
from plone.supermodel import model

from urban.schedule import _

from zope import schema
from zope.interface import implements

import ast


def get_container_state_vocabulary(selected_task_container):
    """
    Return workflow states of the selected task_container.
    """
    # avoid circular import
    from urban.schedule.content.vocabulary import get_states_vocabulary

    portal_type, module_path, interface_name = ast.literal_eval(selected_task_container)
    vocabulary = get_states_vocabulary(portal_type)

    return vocabulary


class ITaskConfig(model.Schema):
    """
    TaskConfig dexterity schema.
    """

    task_container = MasterSelectField(
        title=_(u'Task container content type'),
        description=_(u'Select the content type where the task will be created.'),
        vocabulary='urban.schedule.task_container',
        slave_fields=(
            {
                'name': 'container_state',
                'action': 'vocabulary',
                'vocab_method': get_container_state_vocabulary,
                'control_param': 'selected_task_container',
            },
        ),
        required=True,
    )

    container_state = schema.Choice(
        title=_(u'Task container state'),
        description=_(u'Select the state of the container where the task should start.'),
        vocabulary='urban.schedule.container_state',
        required=False,
    )

    start_conditions = schema.List(
        title=_(u'Start conditions'),
        description=_(u'Select start conditions of the task'),
        value_type=schema.Choice(source='urban.schedule.start_conditions'),
        required=True,
    )

    end_conditions = schema.List(
        title=_(u'End conditions'),
        description=_(u'Select end conditions of the task.'),
        value_type=schema.Choice(source='urban.schedule.end_conditions'),
        required=True,
    )


class BaseTaskConfig(object):
    """
    TaskConfig dexterity class.
    """

    def get_container_portal_type(self):
        """
        Return the portal_type of the selected task_container.
        """
        return self.task_container and self.task_container[0] or ''

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

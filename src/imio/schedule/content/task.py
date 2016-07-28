# -*- coding: utf-8 -*-

from collective.task import _ as CTMF
from collective.task.behaviors import ITask
from collective.task.behaviors import get_parent_assigned_group
from collective.task.behaviors import get_users_vocabulary
from collective.task.field import LocalRoleMasterSelectField

from plone import api
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.dexterity.content import Item

from imio.schedule.config import DONE
from imio.schedule.config import status_by_state
from imio.schedule.interfaces import ScheduleConfigNotFound
from imio.schedule.interfaces import TaskConfigNotFound

from zope.interface import implements


class IAutomatedTask(ITask):
    """
    AutomatedTask dexterity schema.
    """

    directives.order_before(assigned_group='assigned_user')
    directives.order_before(assigned_group='ITask.assigned_user')
    assigned_group = LocalRoleMasterSelectField(
        title=CTMF(u"Assigned group"),
        required=True,
        vocabulary="collective.task.AssignedGroups",
        slave_fields=(
            {'name': 'ITask.assigned_user',
             'slaveID': '#form-widgets-ITask-assigned_user',
             'action': 'vocabulary',
             'vocab_method': get_users_vocabulary,
             'control_param': 'group',
             },
        ),
        defaultFactory=get_parent_assigned_group
    )


class BaseAutomatedTask(object):
    """
    Base class for AutomatedTask content types.
    """

    task_config_UID = ''
    schedule_config_UID = ''

    def get_container(self):
        """
        Return the task container.
        """
        container = self
        while IAutomatedTask.providedBy(container):
            container = container.getParentNode()

        return container

    def get_schedule_config(self):
        """
        Return associated schedule config.
        """
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(UID=self.schedule_config_UID)
        if brains:
            return brains[0].getObject()
        else:
            raise ScheduleConfigNotFound(
                'UID {}'.format(self.schedule_config_UID)
            )

    def get_task_config(self):
        """
        Return associated task config.
        """
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(UID=self.task_config_UID)
        if brains:
            return brains[0].getObject()
        else:
            raise TaskConfigNotFound(
                'UID {}'.format(self.task_config_UID)
            )

    def get_status(self):
        """
        Return the status of the task
        """
        return status_by_state[api.content.get_state(self)]

    def start_conditions_status(self):
        """
        See start_conditions_status of TaskConfig.
        """
        task_config = self.get_task_config()
        container = self.get_container()
        status = task_config.start_conditions_status(container, self)
        return status

    def starting_states_status(self):
        """
        """
        config = self.get_task_config()
        starting_states = config.starting_states
        if not starting_states:
            return

        container = self.get_container()
        container_state = api.content.get_state(container)
        return (container_state, starting_states)

    def end_conditions_status(self):
        """
        See end_conditions_status of TaskConfig.
        """
        task_config = self.get_task_config()
        container = self.get_container()
        status = task_config.end_conditions_status(container, self)
        return status

    def ending_states_status(self):
        """
        """
        config = self.get_task_config()
        ending_states = config.ending_states
        if not ending_states:
            return

        container = self.get_container()
        container_state = api.content.get_state(container)
        return (container_state, ending_states)

    def get_state(self):
        return api.content.get_state(self)

    def get_subtasks(self):
        """
        A normal task has no sub tasks.
        """
        return []

    @property
    def end_date(self):
        """
        """
        if self.get_status() == DONE:
            wf_history = self.workflow_history['task_workflow'][::-1]
            for action in wf_history:
                if status_by_state[action['review_state']] is DONE:
                    end_date = action['time']
                    return end_date.asdatetime()
        return None


class AutomatedTask(Item, BaseAutomatedTask):
    """
    """

    implements(IAutomatedTask)


class IAutomatedMacroTask(IAutomatedTask):
    """
    AutomatedTask dexterity schema.
    """


class AutomatedMacroTask(Container, BaseAutomatedTask):
    """
    """

    implements(IAutomatedMacroTask)

    def get_subtasks(self):
        """
        Return all sub tasks of this macro task.
        """
        sub_tasks = [obj for obj in self.objectValues() if ITask.providedBy(obj)]
        return sub_tasks

    def get_last_subtasks(self):
        """
        Return each last unique sub task of this macro task.
        """
        subtask_type = set()
        sub_tasks = []

        for obj in reversed(self.objectValues()):
            if ITask.providedBy(obj):
                subtask = obj
                if subtask.task_config_UID not in subtask_type:
                    subtask_type.add(subtask.task_config_UID)
                    sub_tasks.append(subtask)

        return reversed(sub_tasks)

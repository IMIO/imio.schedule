# -*- coding: utf-8 -*-

from collective.task.behaviors import ITask

from plone import api
from plone.dexterity.content import Container
from plone.dexterity.content import Item

from imio.schedule.config import status_by_state
from imio.schedule.interfaces import ScheduleConfigNotFound
from imio.schedule.interfaces import TaskConfigNotFound

from zope.interface import implements


class IAutomatedTask(ITask):
    """
    AutomatedTask dexterity schema.
    """


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


class AutomatedTask(Item, BaseAutomatedTask):
    """
    """

    implements(IAutomatedTask)


class AutomatedMacroTask(Container, BaseAutomatedTask):
    """
    """

    implements(IAutomatedTask)

    def get_subtasks(self):
        """
        Return all sub tasks of this macro task.
        """
        sub_tasks = [obj for obj in self.objectValues() if ITask.providedBy(obj)]
        return sub_tasks

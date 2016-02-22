# -*- coding: utf-8 -*-

from collective.task.behaviors import ITask

from plone import api
from plone.dexterity.content import Container
from plone.dexterity.content import Item

from urban.schedule.interfaces import ScheduleConfigNotFound
from urban.schedule.interfaces import TaskConfigNotFound

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

    def is_done(self):
        """
        Default implementation is to say if the task
        is on state 'closed'.
        """
        closed = api.content.get_state(self) == 'closed'
        return closed


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

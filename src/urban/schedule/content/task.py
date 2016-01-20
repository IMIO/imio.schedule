# -*- coding: utf-8 -*-

from collective.task.behaviors import ITask

from plone.dexterity.content import Container
from plone.dexterity.content import Item

from zope.interface import implements


class BaseConfigurableTask(object):
    """
    Base class for ConfigurableTask content types.
    """

    def get_task_config(self):
        """
        Return associated task config.
        """

    def is_done(self):
        """
        Return True is this task is evaluated as done.
        """
        config = self.get_task_config()
        contexts = self.get_evaluation_contexts()
        is_done = config.evaluate_end_condition(task=self, **contexts)
        return is_done

    def get_evaluation_contexts(self):
        """
        Return additional objects and values to be passed to evaluate
        start and end condition of the task.
        """
        return {}


class ConfigurableTask(Item, BaseConfigurableTask):
    """
    """

    implements(ITask)


class ConfigurableMacroTask(Container, BaseConfigurableTask):
    """
    """

    implements(ITask)

    def get_subtasks(self):
        """
        Return all sub tasks of this macro task.
        """
        sub_tasks = [obj for obj in self.objectValues() if ITask.providedBy(obj)]
        return sub_tasks

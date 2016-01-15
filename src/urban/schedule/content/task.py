# -*- coding: utf-8 -*-

from collective.task.behaviors import ITask

from plone.dexterity.content import Container
from plone.dexterity.content import Item

from zope.interface import implements


class ConfigurableTask(Item):
    """
    """

    implements(ITask)

    def get_task_config(self):
        """
        Return associated task config.
        """

    def is_done(self):
        """
        Return True is this task is considered as done.
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


class ConfigurableMacroTask(Container):
    """
    """

    implements(ITask)

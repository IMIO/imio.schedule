# -*- coding: utf-8 -*-

from urban.schedule.interfaces import ICondition
from urban.schedule.interfaces import IEndCondition
from urban.schedule.interfaces import IStartCondition

from zope.interface import implements


class Condition(object):
    """
    Base class for TaskConfig conditions.
    """

    implements(ICondition)

    def __init__(self, task_container):
        self.task_container = task_container


class StartCondition(object):
    """
    """

    implements(IStartCondition)

    def evaluate(self, **kwargs):
        """
        To override.
        Do something with task_container and **kwargs to
        evaluate if the condition is True or False
        """


class EndCondition(object):
    """
    """

    implements(IEndCondition)

    def evaluate(self, task, **kwargs):
        """
        To override.
        Do something with task, task_container and **kwargs to
        evaluate if the condition is True or False
        """

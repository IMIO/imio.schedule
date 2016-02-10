# -*- coding: utf-8 -*-

from urban.schedule.interfaces import ICondition
from urban.schedule.interfaces import ICreationCondition
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


class CreationCondition(Condition):
    """
    Creation condition of a ScheduleTask.
    """

    implements(ICreationCondition)

    def evaluate(self, **kwargs):
        """
        To override.
        Do something with task_container and **kwargs to
        evaluate if the condition is True or False
        """


class StartCondition(Condition):
    """
    Start/creation condition of a ScheduleTask.
    """

    implements(IStartCondition)

    def evaluate(self, **kwargs):
        """
        To override.
        Do something with task_container and **kwargs to
        evaluate if the condition is True or False
        """


class EndCondition(Condition):
    """
    End condition of a ScheduleTask.
    """

    implements(IEndCondition)

    def evaluate(self, task, **kwargs):
        """
        To override.
        Do something with task, task_container and **kwargs to
        evaluate if the condition is True or False
        """

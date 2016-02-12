# -*- coding: utf-8 -*-

from urban.schedule.content.logic import TaskLogic
from urban.schedule.interfaces import ICondition
from urban.schedule.interfaces import ICreationCondition
from urban.schedule.interfaces import IEndCondition
from urban.schedule.interfaces import IMacroTaskCreationCondition
from urban.schedule.interfaces import IMacroTaskEndCondition
from urban.schedule.interfaces import IMacroTaskStartCondition
from urban.schedule.interfaces import IStartCondition

from zope.interface import implements


class Condition(TaskLogic):
    """
    Base class for TaskConfig conditions.
    """

    implements(ICondition)


class CreationCondition(Condition):
    """
    Creation condition of a ScheduleTask.
    """

    implements(ICreationCondition)

    def evaluate(self):
        """
        To override.
        Do something with task_container and **kwargs to
        evaluate if the condition is True or False
        """


class StartCondition(Condition):
    """
    Start condition of a ScheduleTask.
    """

    implements(IStartCondition)

    def evaluate(self):
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

    def evaluate(self, task):
        """
        To override.
        Do something with task, task_container and **kwargs to
        evaluate if the condition is True or False
        """


class MacroTaskCreationCondition(Condition):
    """
    Creation condition of a ScheduleMacroTask.
    """

    implements(IMacroTaskCreationCondition)

    def evaluate(self):
        """
        To override.
        Do something with task_container and **kwargs to
        evaluate if the condition is True or False
        """


class MacroTaskStartCondition(Condition):
    """
    Start condition of a ScheduleMacroTask.
    """

    implements(IMacroTaskStartCondition)

    def evaluate(self):
        """
        To override.
        Do something with task_container and **kwargs to
        evaluate if the condition is True or False
        """


class MacroTaskEndCondition(Condition):
    """
    End condition of a ScheduleMacroTask.
    """

    implements(IMacroTaskEndCondition)

    def evaluate(self, task):
        """
        To override.
        Do something with task, task_container and **kwargs to
        evaluate if the condition is True or False
        """


class CreateIfSubtaskCanBeCreated(MacroTaskCreationCondition):
    """
    Return True if at least one substask can be created.
    """

    def evaluate(self):
        """
        """


class CreateIfAllSubtasksCanBeCreated(MacroTaskCreationCondition):
    """
    Return True if all substasks can be created.
    """

    def evaluate(self):
        """
        """


class StartIfAnySubtaskStarted(MacroTaskStartCondition):
    """
    Return True if at least one substask started.
    """

    def evaluate(self):
        """
        """


class StartIfAllSubtasksStarted(MacroTaskStartCondition):
    """
    Return True if all substasks started.
    """

    def evaluate(self):
        """
        """

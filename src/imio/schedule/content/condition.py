# -*- coding: utf-8 -*-

from imio.schedule.content.logic import CreationTaskLogic
from imio.schedule.content.logic import TaskLogic
from imio.schedule.interfaces import ICondition
from imio.schedule.interfaces import ICreationCondition
from imio.schedule.interfaces import IEndCondition
from imio.schedule.interfaces import IMacroTaskCreationCondition
from imio.schedule.interfaces import IMacroTaskEndCondition
from imio.schedule.interfaces import IMacroTaskStartCondition
from imio.schedule.interfaces import IStartCondition

from zope.interface import implements


class Condition(TaskLogic):
    """
    Base class for TaskConfig conditions.
    """

    implements(ICondition)
    display_status = True


class CreationCondition(CreationTaskLogic):
    """
    Creation condition of a AutomatedTask.
    """

    implements(ICreationCondition)

    def evaluate(self):
        """
        To override.
        evaluate if the condition is True or False
        """


class StartCondition(Condition):
    """
    Start condition of a AutomatedTask.
    """

    implements(IStartCondition)

    def evaluate(self):
        """
        To override.
        evaluate if the condition is True or False
        """


class EndCondition(Condition):
    """
    End condition of a AutomatedTask.
    """

    implements(IEndCondition)

    def evaluate(self):
        """
        To override.
        evaluate if the condition is True or False
        """


class MacroTaskCreationCondition(CreationCondition):
    """
    Creation condition of a AutomatedMacroTask.
    """

    implements(IMacroTaskCreationCondition)

    def evaluate(self):
        """
        To override.
        evaluate if the condition is True or False
        """


class MacroTaskStartCondition(Condition):
    """
    Start condition of a AutomatedMacroTask.
    """

    implements(IMacroTaskStartCondition)

    def evaluate(self):
        """
        To override.
        evaluate if the condition is True or False
        """


class MacroTaskEndCondition(Condition):
    """
    End condition of a AutomatedMacroTask.
    """

    implements(IMacroTaskEndCondition)

    def evaluate(self):
        """
        To override.
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


class RecurrencyCondition(Condition):

    def __init__(self, task_container, task_config):
        self.task_container = task_container
        self.task_config = task_config


class NoRecurencyCondition(RecurrencyCondition):

    def evaluate(self):
        return False

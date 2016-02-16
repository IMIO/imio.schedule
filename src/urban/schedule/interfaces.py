# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IUrbanScheduleLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IScheduledContentTypeVocabulary(Interface):
    """
    Adapts a ScheduleConfig instance into a vocabulary.
    """


class ITaskLogic(Interface):
    """
    Base interface for all the TaskConfig logic items:
        - conditions,
        - date computation
        - user assignment
    """


class ICreationTaskLogic(Interface):
    """
    Base interface for all the TaskConfig creation logic items.
    """


class IDefaultTaskUser(ITaskLogic):
    """
    Adapts a TaskContainer into a plone user to assign to a task.
    """


class ICondition(ITaskLogic):
    """
    Condition object adapting a TaskContainer and task.
    """


class ITaskCreationCondition(ICreationTaskLogic):
    """
    Condition object adapting a TaskContainer.
    """


class ICreationCondition(ICondition):
    """
    Creation condition of task.
    """

    def evaluate(self):
        """
        Do something with task_container to
        evaluate if the condition is True or False
        """


class IStartCondition(ICondition):
    """
    Start condition of task.
    """

    def evaluate(self, task):
        """
        Do something with task, task_container to
        evaluate if the condition is True or False
        """


class IEndCondition(ICondition):
    """
    End condition of task.
    """

    def evaluate(self, task):
        """
        Do something with task, task_container to
        evaluate if the condition is True or False
        """


class IStartDate(ITaskLogic):
    """
    Adapts a TaskContainer into the start date used to compute
    the task due date.
    """

    def due_date(self):
        """
        Compute a due date from task_container
        then return it.
        """


class IMacroTaskCreationCondition(ICreationCondition):
    """
    Creation condition of macro task.
    """


class IMacroTaskStartCondition(IStartCondition):
    """
    Start condition of macro task.
    """


class IMacroTaskEndCondition(IEndCondition):
    """
    End condition of macro task.
    """


class IMacroTaskStartDate(IStartDate):
    """
    Adapts a TaskContainer into the start date used to compute
    the macro task due date.
    """


class IToTaskConfig(Interface):
    """
    Interface for adapters returning the task config of
    a context providing ITaskContainer.
    """


class ScheduleConfigNotFound(Exception):
    """
    Raised when a ScheduleConfig is not found.
    """


class TaskConfigNotFound(Exception):
    """
    Raised when a TaskConfig is not found.
    """

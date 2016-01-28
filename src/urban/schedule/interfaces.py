# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IUrbanScheduleLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    """ """


class ICondition(Interface):
    """
    Condition object adapting a TaskContainer.
    """


class IStartCondition(ICondition):
    """
    Start/creation condition of task.
    """

    def evaluate(self, **kwargs):
        """
        Do something with task_container and **kwargs to
        evaluate if the condition is True or False
        """


class IEndCondition(ICondition):
    """
    End condition of task.
    """

    def evaluate(self, task, **kwargs):
        """
        Do something with task, task_container and **kwargs to
        evaluate if the condition is True or False
        """


class IScheduledContentTypeVocabulary(Interface):
    """
    Adapts a ScheduleConfig instance into a vocabulary.
    """


class IToTaskConfig(Interface):
    """
    Interface for adapters returning the task config of
    a context providing ITaskContainer.
    """


class TaskConfigNotFound(Exception):
    """
    Raised when a TaskConfig is not found.
    """

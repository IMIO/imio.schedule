# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IUrbanScheduleLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
    """ """


class ICondition(Interface):
    """
    Condition object.
    """

    def evaluate(self):
        """
        Represent the condition evaluation by returning True or False.
        """


class IScheduledContentTypeVocabulary(Interface):
    """
    Adapts a ScheduleConfig instance into a vocabulary.
    """


class IStartConditionsVocabulary(Interface):
    """
    Adapts a TaskConfig instance into a vocabulary.
    """


class IEndConditionsVocabulary(Interface):
    """
    Adapts a TaskConfig instance into a vocabulary.
    """


class IToTaskConfig(Interface):
    """
    Interface for adapters returning the task config of
    a context providing ITaskContainer.
    """

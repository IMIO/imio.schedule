# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from imio.schedule import _


class IImioScheduleLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IScheduledContentTypeVocabulary(Interface):
    """
    Adapts a ScheduleConfig instance into a vocabulary.
    """


class ITaskLogic(Interface):
    """
    Base interface for the following TaskConfig logic items:
        - conditions,
        - date computation
        - user assignment
    """


class IDefaultTaskGroup(ITaskLogic):
    """
    Adapts a TaskContainer into a plone group to assign to a task.
    """


class IDefaultTaskUser(ITaskLogic):
    """
    Adapts a TaskContainer into a plone user to assign to a task.
    """


class ICondition(ITaskLogic):
    """
    Condition object adapting a TaskContainer and task.
    """

    def evaluate(self):
        """
        evaluate if the condition is True or False
        """


class ICreationCondition(ICondition):
    """
    Creation condition of task.
    """


class IStartCondition(ICondition):
    """
    Start condition of task.
    """


class IEndCondition(ICondition):
    """
    End condition of task.
    """


class IStartDate(ITaskLogic):
    """
    Adapts a TaskContainer into the start date used to compute
    the task due date.
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


class IScheduleView(Interface):
    """
    Marker interface to provides on folderish with the schedule faceted view.
    """


class IScheduleCollection(Interface):
    """
    Marker interface for collections associated to schedule/task config.
    """


class ITaskMarkerInterface(IInterface):
    """
    Marker interface for for AutomatedTask custom marker interfaces vocabulary.
    """


class ScheduleConfigNotFound(Exception):
    """
    Raised when a ScheduleConfig is not found.
    """


class TaskConfigNotFound(Exception):
    """
    Raised when a TaskConfig is not found.
    """


class TaskAlreadyExists(Exception):
    """
    Raised when a Task already exists.
    """


class IRecurrenceCondition(ITaskLogic):
    """
    Base interface for the TaskConfig recurrence conditions
    """


class ICalculationDelay(ITaskLogic):
    """
    Base interface for the TaskConfig calculation delay methods
    """


class IToIcon(Interface):
    """
    Adapts an object into an icon.
    """

    def get_icon_url(self):
        """
        Return the icon url.
        """


class ISettings(model.Schema):

    working_days = schema.List(
        title=_(u'List of working days'),
        value_type=schema.Choice(
            title=_(u'Day'),
            vocabulary='imio.schedule.working_days',
        ),
        required=True,
    )

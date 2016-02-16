# -*- coding: utf-8 -*-

from DateTime import DateTime

from plone import api

from urban.schedule.interfaces import ICreationTaskLogic
from urban.schedule.interfaces import IDefaultTaskUser
from urban.schedule.interfaces import IMacroTaskStartDate
from urban.schedule.interfaces import IStartDate
from urban.schedule.interfaces import ITaskLogic

from zope.interface import implements


class CreationTaskLogic(object):
    """
    Base class for any object adapting a task container into
    some task logic (condition, user assigment, due date..)
    called during the task craetion.
    """

    implements(ICreationTaskLogic)

    def __init__(self, task_container):
        self.task_container = task_container


class TaskLogic(object):
    """
    Base class for any object adapting a task container and a task
    into some logic (condition, user assigment, due date..).
    """

    implements(ITaskLogic)

    def __init__(self, task_container, task):
        self.task_container = task_container
        self.task = task


class StartDate(TaskLogic):
    """
    Base class for TaskConfig due dates.
    """

    implements(IStartDate)

    def due_date(self):
        """
        To override.
        Compute a due date from task_container
        then return it.
        """


class MacroTaskStartDate(StartDate):
    """
    Base class for TaskConfig due dates.
    """

    implements(IMacroTaskStartDate)

    def start_date(self):
        """
        To override.
        Compute a due date from task_container
        then return it.
        """


class SubtaskHighestDueDate(MacroTaskStartDate):
    """
    Return the highest due date of the subtasks.
    """

    def start_date(self):
        """
        Return the highest due date of the subtasks.
        """
        subtasks = self.task.get_subtasks()
        if not subtasks:
            return None
        due_dates = [DateTime(str(t.due_date)) for t in subtasks if t.due_date]
        return max(due_dates)


class AssignTaskUser(TaskLogic):
    """
    Base class for adapters adapting a TaskContainer to return a user to
    assign to its tasks.
    Register adapters inheriting this class in the products using
    urban.schedule and override 'user_id' method.
    """
    implements(IDefaultTaskUser)

    def user_id(self):
        """
        To override.
        """


class AssignCurrentUser(AssignTaskUser):
    """
    Return the current connected user to assign it as default assigned
    user of a new ScheduleTask.
    """

    def user_id(self):
        """
        Return the id of the current user.
        """
        user = api.user.get_current()
        user_id = user.getUserName()
        return user_id

# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.interfaces import IDefaultTaskUser

from zope.interface import implements


class AssignTaskUser(object):
    """
    Base class for adapters adapting a TaskContainer to return a user to
    assign to its tasks.
    Register adapters inheriting this class in the products using
    urban.schedule and override 'user_id' method.
    """
    implements(IDefaultTaskUser)

    def __init__(self, task_container):
        self.task_container = task_container

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

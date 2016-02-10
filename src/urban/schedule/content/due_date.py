# -*- coding: utf-8 -*-

from urban.schedule.interfaces import IStartDate

from zope.interface import implements


class StartDate(object):
    """
    Base class for TaskConfig due dates.
    """

    implements(IStartDate)

    def __init__(self, task_container):
        self.task_container = task_container

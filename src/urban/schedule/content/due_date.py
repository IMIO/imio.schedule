# -*- coding: utf-8 -*-

from urban.schedule.interfaces import IDueDate

from zope.interface import implements


class DueDate(object):
    """
    Base class for TaskConfig due dates.
    """

    implements(IDueDate)

    def __init__(self, task_container):
        self.task_container = task_container

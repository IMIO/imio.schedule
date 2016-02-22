# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface


class IDisplayTaskStatus(Interface):
    """
    Adapts a task instance into a z3c table cell
    displaying the task status.
    """

    def render(self):
        """
        """

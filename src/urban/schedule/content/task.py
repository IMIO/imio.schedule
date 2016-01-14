# -*- coding: utf-8 -*-

from collective.task.behaviors import ITask

from plone.dexterity.content import Container
from plone.dexterity.content import Item

from zope.interface import implements


class ConfigurableTask(Item):
    """
    """

    implements(ITask)


class ConfigurableMacroTask(Container):
    """
    """

    implements(ITask)

# -*- coding: utf-8 -*-

from z3c.form.object import FactoryAdapter
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from imio.schedule.content.task_config import ICreationConditionSchema
from imio.schedule.content.task_config import IStartConditionSchema
from imio.schedule.content.task_config import IEndConditionSchema
from imio.schedule.content.task_config import IMacroCreationConditionSchema
from imio.schedule.content.task_config import IMacroStartConditionSchema
from imio.schedule.content.task_config import IMacroEndConditionSchema


class BaseConditionObject(object):
    """
    Base class for condition objects.
    """

    __name__ = ''
    __parent__ = None

    def __init__(self, condition=None, operator=None):
        if condition is not None:
            self.__dict__['condition'] = condition
        if operator is not None:
            self.__dict__['operator'] = operator

    def getId(self):
        return self.__name__ or ''


class CreationConditionObject(BaseConditionObject):
    implements(ICreationConditionSchema)

    condition = FieldProperty(ICreationConditionSchema['condition'])
    operator = FieldProperty(ICreationConditionSchema['operator'])


class CreationConditionAdapter(FactoryAdapter):
    factory = CreationConditionObject


class StartConditionObject(BaseConditionObject):
    implements(IStartConditionSchema)

    condition = FieldProperty(IStartConditionSchema['condition'])
    operator = FieldProperty(IStartConditionSchema['operator'])


class StartConditionAdapter(FactoryAdapter):
    factory = StartConditionObject


class EndConditionObject(BaseConditionObject):
    implements(IEndConditionSchema)

    condition = FieldProperty(IEndConditionSchema['condition'])
    operator = FieldProperty(IEndConditionSchema['operator'])


class EndConditionAdapter(FactoryAdapter):
    factory = EndConditionObject


class MacroCreationConditionObject(BaseConditionObject):
    implements(IMacroCreationConditionSchema)

    condition = FieldProperty(IMacroCreationConditionSchema['condition'])
    operator = FieldProperty(IMacroCreationConditionSchema['operator'])


class MacroCreationConditionAdapter(FactoryAdapter):
    factory = MacroCreationConditionObject


class MacroStartConditionObject(BaseConditionObject):
    implements(IMacroStartConditionSchema)

    condition = FieldProperty(IMacroStartConditionSchema['condition'])
    operator = FieldProperty(IMacroStartConditionSchema['operator'])


class MacroStartConditionAdapter(FactoryAdapter):
    factory = MacroStartConditionObject


class MacroEndConditionObject(BaseConditionObject):
    implements(IMacroEndConditionSchema)

    condition = FieldProperty(IMacroEndConditionSchema['condition'])
    operator = FieldProperty(IMacroEndConditionSchema['operator'])


class MacroEndConditionAdapter(FactoryAdapter):
    factory = MacroEndConditionObject

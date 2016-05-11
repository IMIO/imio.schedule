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


class CreationConditionObject(object):
    implements(ICreationConditionSchema)

    condition = FieldProperty(ICreationConditionSchema['condition'])
    operator = FieldProperty(ICreationConditionSchema['operator'])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''


class CreationConditionAdapter(FactoryAdapter):
    factory = CreationConditionObject


class StartConditionObject(object):
    implements(IStartConditionSchema)

    condition = FieldProperty(IStartConditionSchema['condition'])
    operator = FieldProperty(IStartConditionSchema['operator'])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''


class StartConditionAdapter(FactoryAdapter):
    factory = StartConditionObject


class EndConditionObject(object):
    implements(IEndConditionSchema)

    condition = FieldProperty(IEndConditionSchema['condition'])
    operator = FieldProperty(IEndConditionSchema['operator'])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''


class EndConditionAdapter(FactoryAdapter):
    factory = EndConditionObject


class MacroCreationConditionObject(object):
    implements(IMacroCreationConditionSchema)

    condition = FieldProperty(IMacroCreationConditionSchema['condition'])
    operator = FieldProperty(IMacroCreationConditionSchema['operator'])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''


class MacroCreationConditionAdapter(FactoryAdapter):
    factory = MacroCreationConditionObject


class MacroStartConditionObject(object):
    implements(IMacroStartConditionSchema)

    condition = FieldProperty(IMacroStartConditionSchema['condition'])
    operator = FieldProperty(IMacroStartConditionSchema['operator'])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''


class MacroStartConditionAdapter(FactoryAdapter):
    factory = MacroStartConditionObject


class MacroEndConditionObject(object):
    implements(IMacroEndConditionSchema)

    condition = FieldProperty(IMacroEndConditionSchema['condition'])
    operator = FieldProperty(IMacroEndConditionSchema['operator'])

    __name__ = ''
    __parent__ = None

    def getId(self):
        return self.__name__ or ''


class MacroEndConditionAdapter(FactoryAdapter):
    factory = MacroEndConditionObject

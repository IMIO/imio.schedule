# -*- coding: utf-8 -*-

from z3c.form.object import FactoryAdapter
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from imio.schedule.content.task_config import ICreationConditionSchema
from imio.schedule.content.task_config import IStartConditionSchema
from imio.schedule.content.task_config import IEndConditionSchema


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

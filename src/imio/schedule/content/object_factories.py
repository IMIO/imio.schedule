# -*- coding: utf-8 -*-

from z3c.form.object import FactoryAdapter
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

from imio.schedule.content.task_config import ICreationConditionSchema
from imio.schedule.content.task_config import IEndConditionSchema
from imio.schedule.content.task_config import IMacroCreationConditionSchema
from imio.schedule.content.task_config import IMacroEndConditionSchema
from imio.schedule.content.task_config import IMacroRecurrenceConditionSchema
from imio.schedule.content.task_config import IMacroStartConditionSchema
from imio.schedule.content.task_config import IRecurrenceConditionSchema
from imio.schedule.content.task_config import IStartConditionSchema


class BaseConditionObject(object):
    """
    Base class for condition objects.
    """

    __name__ = ''
    __parent__ = None

    def __init__(self, condition=None, operator=None, display_status=True):
        if condition is not None:
            self.__dict__['condition'] = condition
        if operator is not None:
            self.__dict__['operator'] = operator
        self.__dict__['display_status'] = display_status

    def getId(self):
        return self.__name__ or ''


class CreationConditionObject(BaseConditionObject):
    implements(ICreationConditionSchema)

    condition = FieldProperty(ICreationConditionSchema['condition'])
    operator = FieldProperty(ICreationConditionSchema['operator'])
    display_status = FieldProperty(ICreationConditionSchema['display_status'])


class CreationConditionAdapter(FactoryAdapter):
    factory = CreationConditionObject


class StartConditionObject(BaseConditionObject):
    implements(IStartConditionSchema)

    condition = FieldProperty(IStartConditionSchema['condition'])
    operator = FieldProperty(IStartConditionSchema['operator'])
    display_status = FieldProperty(IStartConditionSchema['display_status'])


class StartConditionAdapter(FactoryAdapter):
    factory = StartConditionObject


class EndConditionObject(BaseConditionObject):
    implements(IEndConditionSchema)

    condition = FieldProperty(IEndConditionSchema['condition'])
    operator = FieldProperty(IEndConditionSchema['operator'])
    display_status = FieldProperty(IEndConditionSchema['display_status'])


class EndConditionAdapter(FactoryAdapter):
    factory = EndConditionObject


class MacroCreationConditionObject(BaseConditionObject):
    implements(IMacroCreationConditionSchema)

    condition = FieldProperty(IMacroCreationConditionSchema['condition'])
    operator = FieldProperty(IMacroCreationConditionSchema['operator'])
    display_status = FieldProperty(IMacroCreationConditionSchema['display_status'])


class MacroCreationConditionAdapter(FactoryAdapter):
    factory = MacroCreationConditionObject


class MacroStartConditionObject(BaseConditionObject):
    implements(IMacroStartConditionSchema)

    condition = FieldProperty(IMacroStartConditionSchema['condition'])
    operator = FieldProperty(IMacroStartConditionSchema['operator'])
    display_status = FieldProperty(IMacroStartConditionSchema['display_status'])


class MacroStartConditionAdapter(FactoryAdapter):
    factory = MacroStartConditionObject


class MacroEndConditionObject(BaseConditionObject):
    implements(IMacroEndConditionSchema)

    condition = FieldProperty(IMacroEndConditionSchema['condition'])
    operator = FieldProperty(IMacroEndConditionSchema['operator'])
    display_status = FieldProperty(IMacroEndConditionSchema['display_status'])


class MacroEndConditionAdapter(FactoryAdapter):
    factory = MacroEndConditionObject


class RecurrenceConditionObject(BaseConditionObject):
    implements(IRecurrenceConditionSchema)

    condition = FieldProperty(IRecurrenceConditionSchema['condition'])
    operator = FieldProperty(IRecurrenceConditionSchema['operator'])
    display_status = FieldProperty(IRecurrenceConditionSchema['display_status'])


class RecurrenceConditionAdapter(FactoryAdapter):
    factory = RecurrenceConditionObject


class MacroRecurrenceConditionObject(BaseConditionObject):
    implements(IMacroRecurrenceConditionSchema)

    condition = FieldProperty(IMacroRecurrenceConditionSchema['condition'])
    operator = FieldProperty(IMacroRecurrenceConditionSchema['operator'])
    display_status = FieldProperty(IMacroRecurrenceConditionSchema['display_status'])


class MacroRecurrenceConditionAdapter(FactoryAdapter):
    factory = MacroRecurrenceConditionObject

# encoding: utf-8

from Products.urban.browser.table.interfaces import ITitleColumn

from collective.eeafaceted.z3ctable.columns import BaseColumn

from zope.interface import implements


class DueDateColumn(BaseColumn):
    """ TitleColumn for imio.dashboard listings."""
    implements(ITitleColumn)

    def renderCell(self, item):
        return item.due_date

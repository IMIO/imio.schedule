# encoding: utf-8

from collective.eeafaceted.z3ctable.columns import BaseColumn


class DueDateColumn(BaseColumn):
    """ TitleColumn for imio.dashboard listings."""

    def renderCell(self, item):
        return item.due_date

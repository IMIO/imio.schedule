# encoding: utf-8

from collective.eeafaceted.z3ctable.columns import BaseColumn

from plone import api

from urban.schedule.dashboard.interfaces import IDisplayTaskStatus

from zope.component import queryMultiAdapter
from zope.interface import implements


class DueDateColumn(BaseColumn):
    """ TitleColumn for imio.dashboard listings."""

    def renderCell(self, item):
        return item.due_date


class StatusColum(BaseColumn):
    """
    Column displaying the status of the tasks and its subtasks if it has any.
    """

    sort_index = -1

    def renderCell(self, item):
        """
        """
        status = ''
        task = item.getObject()

        adapter = queryMultiAdapter(
            (self, task, api.portal.getRequest()),
            IDisplayTaskStatus
        )
        if adapter:
            status = adapter.render()
        return status


class TaskStatusDisplay(object):
    """
    Adpater, adapting a task and returning some html
    table cell displaying its status.
    """

    implements(IDisplayTaskStatus)

    def __init__(self, column, task, request):
        self.task = task
        self.request = request


class MacroTaskStatusDisplay(TaskStatusDisplay):
    """
    Adapts a macro task and return some html table cell
    displaying the status of all its subtasks.
    """

    def render(self):
        """
        """
        subtasks = self.task.get_subtasks()
        rows = []
        for task in subtasks:
            title = task.Title()
            due_date = '<span style="float: right">{}</span>'.format(task.due_date)
            css_class = 'schedule_{}'.format(api.content.get_state(task))
            row = u'<span class="{css_class}">&nbsp&nbsp&nbsp</span> {title} {due_date}'.format(
                css_class=css_class,
                title=title.decode('utf-8'),
                due_date=str(due_date)
            )
            rows.append(row)

        status_display = u'<br />'.join(rows)
        return status_display

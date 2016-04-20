# encoding: utf-8

from collective.eeafaceted.z3ctable.columns import BaseColumn

from plone import api

from urban.schedule.config import CREATION
from urban.schedule.config import STARTED
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

    def renderHeadCell(self):
        """Override rendering of head of the cell to include jQuery
           call to initialize annexes menu and to show the 'more/less details' if we are listing items."""
        # activate necessary javascripts
        if not self.header_js:
            # avoid problems while concataining None and unicode
            self.header_js = u''
        self.header_js += u'<script type="text/javascript">' + \
            u'$("#task_status a").prepOverlay({subtype: "ajax"});' + \
            '</script>'
        return super(StatusColum, self).renderHeadCell()

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

    def render(self):
        """
        By default just put a code colour of the state of the task.
        """
        task = self.task
        css_class = 'schedule_{}'.format(api.content.get_state(task))
        status = u'<span class="{css_class}">&nbsp&nbsp&nbsp</span>'.format(
            css_class=css_class,
        )
        if task.get_status() in [CREATION, STARTED]:
            status = '<a class="link-overlay" href="{task_url}/@@{view}">{status}</a>'.format(
                task_url=self.task.absolute_url(),
                view=task.get_status() is CREATION and 'start_status' or 'end_status',
                status=status
            )
        status = '<span id="task_status">{}</span>'.format(status)
        return status


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

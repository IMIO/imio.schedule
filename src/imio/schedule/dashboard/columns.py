# encoding: utf-8

from collective.eeafaceted.z3ctable.columns import BaseColumn

from plone import api

from imio.schedule import _
from imio.schedule.config import CREATION
from imio.schedule.config import STARTED
from imio.schedule.content.task import IAutomatedMacroTask
from imio.schedule.dashboard.interfaces import IDisplayTaskStatus
from imio.schedule.dashboard.interfaces import IStatusColumn

from zope.component import queryMultiAdapter
from zope.interface import implements


class DueDateColumn(BaseColumn):
    """ Due date column for schedule listings."""

    def renderCell(self, item):
        due_date = item.due_date
        if due_date.year == 9999:
            return u'\u221E'

        return due_date.strftime('%d/%m/%Y')


class AssignedUserColumn(BaseColumn):
    """ display licence address in SearchResultTable """

    def renderCell(self, item):
        user = item.assigned_user
        group = item.assigned_group

        assigned = user
        if group:
            assigned = '{user} ({group})'.format(
                user=api.user.get(user).getProperty('fullname'),
                group=group
            )

        return assigned


class StatusColum(BaseColumn):
    """
    Column displaying the status of the tasks and its subtasks if it has any.
    """
    implements(IStatusColumn)

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
        task = self.task
        return self.display_task_status(task)

    def display_task_status(self, task, with_subtasks=False):
        """
        By default just put a code colour of the state of the task.
        """
        css_class = 'schedule_{}'.format(api.content.get_state(task))
        status = u'<span class="{css_class}">&nbsp&nbsp&nbsp</span>'.format(
            css_class=css_class,
        )
        if task.get_status() in [CREATION, STARTED]:
            viewname = '{}{}_status'.format(
                (not with_subtasks) and 'simple_' or '',
                task.get_status() is CREATION and 'start' or 'end',
            )
            status = '<a class="link-overlay" href="{task_url}/@@{view}">{status}</a>'.format(
                task_url=task.absolute_url(),
                view=viewname,
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
        subtasks = self.task.get_last_subtasks()
        if not subtasks:
            return self.display_task_status(self.task)

        rows = [
            u'<tr><th class="subtask_status_icon">{icon}</th>\
            <th i18n:translate="">{subtask}</th>\
            <th i18n:translate="">{due_date}</th></tr>'.format(
            icon=self.display_task_status(self.task),
            subtask=_('Subtask'),
            due_date=_('Due date'),
        ),
        ]
        for task in subtasks:
            title = task.Title()
            status_icon = u'<td class="subtask_status_icon">{status}</td>'.format(
                status=self.display_task_status(task, with_subtasks=IAutomatedMacroTask.providedBy(task)),
            )
            status_title = u'<td class="subtask_status_title">{title}</td>'.format(
                title=title.decode('utf-8'),
            )
            date = task.due_date
            due_date = date.year == 9999 and u'\u221E' or date.strftime('%d/%m/%Y')
            due_date = u'<td class="subtask_status_date">{}</td>'.format(due_date)
            row = u'<tr>{icon}{title}{due_date}</tr>'.format(
                icon=status_icon,
                title=status_title,
                due_date=due_date
            )
            rows.append(row)

        status_display = u'<table class=subtask_status_table>{}</table>'.format(''.join(rows))
        return status_display

# -*- coding: utf-8 -*-

from DateTime import DateTime

from urban.schedule.interfaces import IMacroTaskStartDate
from urban.schedule.testing import MacroTaskScheduleIntegrationTestCase

from zope.component import queryMultiAdapter
from zope.component import getMultiAdapter


class TestMacroTaskLogicIntegration(MacroTaskScheduleIntegrationTestCase):
    """
    Test MacroTaskConfig methods.
    """

    def test_subtask_highest_due_date_registration(self):
        """
        Content types voc factory should be registered as a named utility.
        """
        logic_name = 'schedule.start_date.subtask_highest_due_date'

        duedate_adapter = queryMultiAdapter(
            (self.task_container, self.macro_task),
            IMacroTaskStartDate,
            name=logic_name
        )
        self.assertTrue(duedate_adapter)

    def test_subtask_highest_due_date_logic(self):
        """
        Check if the SubtaskHighestDueDate adapter return the highest
        due date amongst all the subtasks of a AutomatedMacroTask.
        """
        logic_name = 'schedule.start_date.subtask_highest_due_date'

        duedate_adapter = getMultiAdapter(
            (self.task_container, self.macro_task),
            IMacroTaskStartDate,
            name=logic_name
        )

        highest_due_date = duedate_adapter.start_date()
        expected_date = DateTime(str(self.sub_task.due_date))
        self.assertEquals(highest_due_date, expected_date)
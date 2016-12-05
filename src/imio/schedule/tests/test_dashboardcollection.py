# -*- coding: utf-8 -*-

from imio.schedule.testing import ExampleScheduleFunctionalTestCase

from plone import api


class TestTaskConfigMethodsFunctional(ExampleScheduleFunctionalTestCase):
    """
    Test TaskConfig methods.
    """

    def test_end_task(self):
        """
        Default implementation is to put the task on the state 'closed'.
        """
        task_config = self.task_config
        task = self.task

        task_state = api.content.get_state(task)
        self.assertNotEquals(task_state, 'closed')

        task_config.end_task(task)
        task_state = api.content.get_state(task)
        msg = "Task should be on state 'closed'"
        self.assertEquals(task_state, 'closed', msg)

# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.testing import ExampleScheduleIntegrationTestCase


class TestIndexes(ExampleScheduleIntegrationTestCase):
    """
    Test custom indexes.
    """

    def test_schedule_config_UID_index(self):
        """
        Content types voc factory should be registered as a named utility.
        """
        schedule_config = self.schedule_config
        task = self.task
        catalog = api.portal.get_tool('portal_catalog')

        task_brains = catalog(schedule_config_UID=schedule_config.UID())
        msg = "should have found at least one indexed task"
        self.assertEquals(len(task_brains), 1, msg)
        self.assertEquals(task_brains[0].getObject(), task)

    def test_task_config_UID_index(self):
        """
        Content types voc factory should be registered as a named utility.
        """
        task_config = self.task_config
        task = self.task
        catalog = api.portal.get_tool('portal_catalog')

        task_brains = catalog(task_config_UID=task_config.UID())
        msg = "should have found at least one indexed task"
        self.assertEquals(len(task_brains), 1, msg)
        self.assertEquals(task_brains[0].getObject(), task)

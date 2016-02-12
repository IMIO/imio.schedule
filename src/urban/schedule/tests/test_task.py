# -*- coding: utf-8 -*-

from urban.schedule.testing import ExampleScheduleIntegrationTestCase
from urban.schedule.testing import MacroTaskScheduleIntegrationTestCase
from urban.schedule.testing import TEST_INSTALL_INTEGRATION

from plone import api

import unittest


class TestScheduleTask(unittest.TestCase):
    """
    Test ScheduleTask content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_ScheduleTask_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('ScheduleTask' in registered_types)


class TestScheduleTaskFields(ExampleScheduleIntegrationTestCase):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        """
        Check if the class of the content type ScheduleTask is the
        correct one.
        """
        from urban.schedule.content.task import ScheduleTask
        self.assertTrue(self.task.__class__ == ScheduleTask)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type ScheduleTask is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.task.portal_type)
        self.assertTrue('IScheduleTask' in taskconfig_type.schema)


class TestScheduleTaskIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test ScheduleTask methods.
    """

    def test_get_task_config(self):
        """
        Should return the associated TaskConfig.
        """
        config = self.task.get_task_config()
        expected_config = self.task_config
        self.assertEquals(config, expected_config)


class TestScheduleMacroTask(unittest.TestCase):
    """
    Test ScheduleMacroTask content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_ScheduleMacroTask_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('ScheduleMacroTask' in registered_types)


class TestScheduleMacroTaskFields(MacroTaskScheduleIntegrationTestCase):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        """
        Check if the class of the content type ScheduleMacroTask is the
        correct one.
        """
        from urban.schedule.content.task import ScheduleMacroTask
        self.assertTrue(self.macro_task.__class__ == ScheduleMacroTask)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type ScheduleMacroTask is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.macro_task.portal_type)
        self.assertTrue('IScheduleTask' in taskconfig_type.schema)


class TestScheduleMacroTaskIntegration(MacroTaskScheduleIntegrationTestCase):
    """
    Test ScheduleMacroTask methods.
    """

    def test_get_task_config(self):
        """
        Should return the associated MacroTaskConfig.
        """
        config = self.macro_task.get_task_config()
        expected_config = self.macrotask_config
        self.assertEquals(config, expected_config)

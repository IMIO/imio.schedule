# -*- coding: utf-8 -*-

from urban.schedule.testing import ExampleScheduleIntegrationTestCase
from urban.schedule.testing import MacroTaskScheduleIntegrationTestCase
from urban.schedule.testing import TEST_INSTALL_INTEGRATION

from plone import api

import unittest


class TestAutomatedTask(unittest.TestCase):
    """
    Test AutomatedTask content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_AutomatedTask_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('AutomatedTask' in registered_types)


class TestAutomatedTaskFields(ExampleScheduleIntegrationTestCase):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        """
        Check if the class of the content type AutomatedTask is the
        correct one.
        """
        from urban.schedule.content.task import AutomatedTask
        self.assertTrue(self.task.__class__ == AutomatedTask)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type AutomatedTask is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.task.portal_type)
        self.assertTrue('IAutomatedTask' in taskconfig_type.schema)


class TestAutomatedTaskIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test AutomatedTask methods.
    """

    def test_get_task_config(self):
        """
        Should return the associated TaskConfig.
        """
        config = self.task.get_task_config()
        expected_config = self.task_config
        self.assertEquals(config, expected_config)


class TestAutomatedMacroTask(unittest.TestCase):
    """
    Test AutomatedMacroTask content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_AutomatedMacroTask_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('AutomatedMacroTask' in registered_types)


class TestAutomatedMacroTaskFields(MacroTaskScheduleIntegrationTestCase):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        """
        Check if the class of the content type AutomatedMacroTask is the
        correct one.
        """
        from urban.schedule.content.task import AutomatedMacroTask
        self.assertTrue(self.macro_task.__class__ == AutomatedMacroTask)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type AutomatedMacroTask is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.macro_task.portal_type)
        self.assertTrue('IAutomatedTask' in taskconfig_type.schema)


class TestAutomatedMacroTaskIntegration(MacroTaskScheduleIntegrationTestCase):
    """
    Test AutomatedMacroTask methods.
    """

    def test_get_task_config(self):
        """
        Should return the associated MacroTaskConfig.
        """
        config = self.macro_task.get_task_config()
        expected_config = self.macrotask_config
        self.assertEquals(config, expected_config)

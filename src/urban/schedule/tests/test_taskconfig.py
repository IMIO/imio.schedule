# -*- coding: utf-8 -*-

from Acquisition import aq_base

from urban.schedule.testing import ExampleScheduleIntegrationTestCase
from urban.schedule.testing import TEST_INSTALL_INTEGRATION

from plone import api

import unittest


class TestTaskConfig(unittest.TestCase):
    """
    Test TaskConfig content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_TaskConfig_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('TaskConfig' in registered_types)


class TestTaskConfigFields(ExampleScheduleIntegrationTestCase):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        from urban.schedule.content.task_config import TaskConfig
        self.assertTrue(self.test_taskconfig.__class__ == TaskConfig)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.test_taskconfig.portal_type)
        self.assertTrue('ITaskConfig' in taskconfig_type.schema)

    def test_task_container_attribute(self):
        test_taskconfig = aq_base(self.test_taskconfig)
        self.assertTrue(hasattr(test_taskconfig, 'task_container'))

    def test_task_container_field_display(self):
        self.browser.open(self.test_taskconfig.absolute_url())
        contents = self.browser.contents
        msg = "field 'task_container' is not displayed"
        self.assertTrue('id="form-widgets-task_container"' in contents, msg)
        msg = "field 'task_container' is not translated"
        self.assertTrue('Récipient de la tâche' in contents, msg)

    def test_task_container_field_edit(self):
        self.browser.open(self.test_taskconfig.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'task_container' is not editable"
        self.assertTrue('Récipient de la tâche' in contents, msg)

    def test_start_conditions_attribute(self):
        test_taskconfig = aq_base(self.test_taskconfig)
        self.assertTrue(hasattr(test_taskconfig, 'start_conditions'))

    def test_start_conditions_field_display(self):
        self.browser.open(self.test_taskconfig.absolute_url())
        contents = self.browser.contents
        msg = "field 'start_conditions' is not displayed"
        self.assertTrue('id="form-widgets-start_conditions"' in contents, msg)
        msg = "field 'start_conditions' is not translated"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_start_conditions_field_edit(self):
        self.browser.open(self.test_taskconfig.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'start_conditions' is not editable"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_starting_state_attribute(self):
        test_taskconfig = aq_base(self.test_taskconfig)
        self.assertTrue(hasattr(test_taskconfig, 'starting_state'))

    def test_starting_state_field_display(self):
        self.browser.open(self.test_taskconfig.absolute_url())
        contents = self.browser.contents
        msg = "field 'starting_state' is not displayed"
        self.assertTrue('id="form-widgets-starting_state"' in contents, msg)
        msg = "field 'starting_state' is not translated"
        self.assertTrue('État de création de la tâche' in contents, msg)

    def test_starting_state_field_edit(self):
        self.browser.open(self.test_taskconfig.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'starting_state' is not editable"
        self.assertTrue('État de création de la tâche' in contents, msg)

    def test_end_conditions_attribute(self):
        test_taskconfig = aq_base(self.test_taskconfig)
        self.assertTrue(hasattr(test_taskconfig, 'end_conditions'))

    def test_end_conditions_field_display(self):
        self.browser.open(self.test_taskconfig.absolute_url())
        contents = self.browser.contents
        msg = "field 'end_conditions' is not displayed"
        self.assertTrue('id="form-widgets-end_conditions"' in contents, msg)
        msg = "field 'end_conditions' is not translated"
        self.assertTrue('Conditions de clôture' in contents, msg)

    def test_end_conditions_field_edit(self):
        self.browser.open(self.test_taskconfig.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'end_conditions' is not editable"
        self.assertTrue('Conditions de clôture' in contents, msg)

    def test_ending_states_attribute(self):
        test_taskconfig = aq_base(self.test_taskconfig)
        self.assertTrue(hasattr(test_taskconfig, 'ending_states'))

    def test_ending_states_field_display(self):
        self.browser.open(self.test_taskconfig.absolute_url())
        contents = self.browser.contents
        msg = "field 'ending_states' is not displayed"
        self.assertTrue('id="form-widgets-ending_states"' in contents, msg)
        msg = "field 'ending_states' is not translated"
        self.assertTrue('État(s) de clôture de la tâche' in contents, msg)

    def test_ending_states_field_edit(self):
        self.browser.open(self.test_taskconfig.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'ending_states' is not editable"
        self.assertTrue('État(s) de clôture de la tâche' in contents, msg)


class TestTaskConfigIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test TaskConfig methods.
    """

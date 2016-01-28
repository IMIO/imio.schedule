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
        """
        Check if the class of the content type TaskConfig is the
        correct one.
        """
        from urban.schedule.content.task_config import TaskConfig
        self.assertTrue(self.task_config.__class__ == TaskConfig)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type TaskConfig is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.task_config.portal_type)
        self.assertTrue('ITaskConfig' in taskconfig_type.schema)

    def test_start_conditions_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'start_conditions'))

    def test_start_conditions_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'start_conditions' is not displayed"
        self.assertTrue('id="form-widgets-start_conditions"' in contents, msg)
        msg = "field 'start_conditions' is not translated"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_start_conditions_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'start_conditions' is not editable"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_starting_state_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'starting_state'))

    def test_starting_state_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'starting_state' is not displayed"
        self.assertTrue('id="form-widgets-starting_state"' in contents, msg)
        msg = "field 'starting_state' is not translated"
        self.assertTrue('État de création de la tâche' in contents, msg)

    def test_starting_state_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'starting_state' is not editable"
        self.assertTrue('État de création de la tâche' in contents, msg)

    def test_end_conditions_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'end_conditions'))

    def test_end_conditions_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'end_conditions' is not displayed"
        self.assertTrue('id="form-widgets-end_conditions"' in contents, msg)
        msg = "field 'end_conditions' is not translated"
        self.assertTrue('Conditions de clôture' in contents, msg)

    def test_end_conditions_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'end_conditions' is not editable"
        self.assertTrue('Conditions de clôture' in contents, msg)

    def test_ending_states_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'ending_states'))

    def test_ending_states_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'ending_states' is not displayed"
        self.assertTrue('id="form-widgets-ending_states"' in contents, msg)
        msg = "field 'ending_states' is not translated"
        self.assertTrue('État(s) de clôture de la tâche' in contents, msg)

    def test_ending_states_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'ending_states' is not editable"
        self.assertTrue('État(s) de clôture de la tâche' in contents, msg)


class TestTaskConfigIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test TaskConfig methods.
    """

    def test_get_task_type(self):
        """
        Should return 'ScheduleTask'
        """
        task_type = self.task_config.get_task_type()
        expected_type = 'ScheduleTask'
        self.assertEquals(task_type, expected_type)

    def test_get_schedule_config(self):
        """
        Should return the parent schedule config.
        """
        config = self.task_config.get_schedule_config()
        expected_config = self.schedule_config
        self.assertEquals(config, expected_config)

    def test_get_scheduled_portal_type(self):
        """
        Sould return the portal_type of the content type selected on the field
        'scheduled_contenttype' of the parent ScheduleConfig.
        """
        portal_type = self.task_config.get_scheduled_portal_type()
        expected_type = 'Folder'
        self.assertEquals(portal_type, expected_type)

    def test_get_scheduled_interface(self):
        """
        Sould return the Interface (or a class) of the content type selected
        on the field 'scheduled_contenttype' of the parent ScheduleConfig.
        """
        from Products.ATContentTypes.interfaces import IATFolder

        type_interface = self.task_config.get_scheduled_interface()
        expected_interface = IATFolder
        self.assertEquals(type_interface, expected_interface)

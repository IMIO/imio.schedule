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

    def test_content_type_attribute(self):
        test_taskconfig = aq_base(self.test_taskconfig)
        self.assertTrue(hasattr(test_taskconfig, 'content_type'))

    def test_content_type_field_display(self):
        self.browser.open(self.test_taskconfig.absolute_url())
        contents = self.browser.contents
        msg = "field 'content_type' is not displayed"
        self.assertTrue('id="form-widgets-content_type"' in contents, msg)
        msg = "field 'content_type' is not translated"
        self.assertTrue('Type de contenu où créer la tâche' in contents, msg)

    def test_content_type_field_edit(self):
        self.browser.open(self.test_taskconfig.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'content_type' is not editable"
        self.assertTrue('Type de contenu où créer la tâche' in contents, msg)


class TestTaskConfigIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test TaskConfig methods.
    """

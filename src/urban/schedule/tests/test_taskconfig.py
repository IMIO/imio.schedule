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
        from urban.schedule.content.pod_template import TaskConfig
        self.assertTrue(self.test_podtemplate.__class__ == TaskConfig)

    def test_schema_registration(self):
        portal_types = api.portal.get_tool('portal_types')
        podtemplate_type = portal_types.get(self.test_podtemplate.portal_type)
        self.assertTrue('ITaskConfig' in podtemplate_type.schema)

    def test_pod_portal_types_attribute(self):
        test_podtemplate = aq_base(self.test_podtemplate)
        self.assertTrue(hasattr(test_podtemplate, 'pod_portal_types'))

    def test_pod_portal_types_field_display(self):
        self.browser.open(self.test_podtemplate.absolute_url())
        contents = self.browser.contents
        msg = "field 'pod_portal_types' is not displayed"
        self.assertTrue('id="form-widgets-pod_portal_types"' in contents, msg)
        msg = "field 'pod_portal_types' is not translated"
        self.assertTrue('Types de contenu autorisés' in contents, msg)

    def test_pod_portal_types_field_edit(self):
        self.browser.open(self.test_podtemplate.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'pod_portal_types' is not editable"
        self.assertTrue('Types de contenu autorisés' in contents, msg)


class TestTaskConfigIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test TaskConfig methods.
    """

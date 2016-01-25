# -*- coding: utf-8 -*-

from Acquisition import aq_base

from urban.schedule.testing import ExampleScheduleIntegrationTestCase
from urban.schedule.testing import TEST_INSTALL_INTEGRATION

from plone import api

import unittest


class TestScheduleConfig(unittest.TestCase):
    """
    Test ScheduleConfig content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_ScheduleConfig_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('ScheduleConfig' in registered_types)


class TestScheduleConfigFields(ExampleScheduleIntegrationTestCase):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        """
        Check if the class of the content type ScheduleConfig is the
        correct one.
        """
        from urban.schedule.content.schedule_config import ScheduleConfig
        self.assertTrue(self.test_scheduleconfig.__class__ == ScheduleConfig)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type ScheduleConfig is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        scheduleconfig_type = portal_types.get(self.test_scheduleconfig.portal_type)
        self.assertTrue('IScheduleConfig' in scheduleconfig_type.schema)

    def test_scheduled_contenttype_attribute(self):
        test_scheduleconfig = aq_base(self.test_scheduleconfig)
        self.assertTrue(hasattr(test_scheduleconfig, 'scheduled_contenttype'))

    def test_scheduled_contenttype_field_display(self):
        self.browser.open(self.test_scheduleconfig.absolute_url())
        contents = self.browser.contents
        msg = "field 'scheduled_contenttype' is not displayed"
        self.assertTrue('id="form-widgets-scheduled_contenttype"' in contents, msg)
        msg = "field 'scheduled_contenttype' is not translated"
        self.assertTrue('Type de contenu associé' in contents, msg)

    def test_scheduled_contenttype_field_edit(self):
        self.browser.open(self.test_scheduleconfig.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'scheduled_contenttype' is not editable"
        self.assertTrue('Type de contenu associé' in contents, msg)


class TestScheduleConfigIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test ScheduleConfig methods.
    """

    def test_get_scheduled_portal_type(self):
        """
        Sould return the portal_type of the content type selected on the field
        'scheduled_contenttype'.
        """
        portal_type = self.test_scheduleconfig.get_scheduled_portal_type()
        expected_type = 'Folder'
        self.assertTrue(portal_type == expected_type)

    def test_get_scheduled_interface(self):
        """
        Sould return the Interface (or a class) of the content type selected
        on the field 'scheduled_contenttype'.
        """
        from Products.ATContentTypes.interfaces import IATFolder

        type_interface = self.test_scheduleconfig.get_scheduled_interface()
        expected_interface = IATFolder
        self.assertTrue(type_interface == expected_interface)

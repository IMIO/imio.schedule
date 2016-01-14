# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from urban.schedule.testing import URBAN_SCHEDULE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that urban.schedule is properly installed."""

    layer = URBAN_SCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if urban.schedule is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'urban.schedule'))

    def test_browserlayer(self):
        """Test that IUrbanScheduleLayer is registered."""
        from urban.schedule.interfaces import (
            IUrbanScheduleLayer)
        from plone.browserlayer import utils
        self.assertIn(IUrbanScheduleLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = URBAN_SCHEDULE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['urban.schedule'])

    def test_product_uninstalled(self):
        """Test if urban.schedule is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'urban.schedule'))

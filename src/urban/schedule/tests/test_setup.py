# -*- coding: utf-8 -*-

from urban.schedule.testing import NAKED_PLONE_INTEGRATION
from urban.schedule.testing import TEST_INSTALL_INTEGRATION  # noqa

from plone import api
from plone.app.testing import applyProfile

import unittest


class TestInstallDependencies(unittest.TestCase):

    layer = NAKED_PLONE_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_dexterity_is_dependency_of_urban_schedule(self):
        """
        dexterity should be installed when we install urban.schedule
        """
        self.assertTrue(not self.installer.isProductInstalled('plone.app.dexterity'))
        applyProfile(self.portal, 'urban.schedule:default')
        self.assertTrue(self.installer.isProductInstalled('plone.app.dexterity'))

    def test_z3cformdatagridfield_is_dependency_of_urban_schedule(self):
        """
        z3cform.datagridfield should be installed when we install urban.schedule
        """
        self.assertTrue(not self.installer.isProductInstalled('collective.z3cform.datagridfield'))
        applyProfile(self.portal, 'urban.schedule:default')
        self.assertTrue(self.installer.isProductInstalled('collective.z3cform.datagridfield'))

    def test_collectivetask_is_dependency_of_urban_schedule(self):
        """
        collective.task should be installed when we install urban.schedule
        """
        self.assertTrue(not self.installer.isProductInstalled('collective.task'))
        applyProfile(self.portal, 'urban.schedule:default')
        self.assertTrue(self.installer.isProductInstalled('collective.task'))


class TestSetup(unittest.TestCase):
    """
    Test that urban.schedule is properly installed.
    """

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """
        Test if urban.schedule is installed.
        """
        self.assertTrue(self.installer.isProductInstalled('urban.schedule'))

    def test_browserlayer(self):
        """
        Test that IUrbanScheduleLayer is registered.
        """
        from urban.schedule.interfaces import IUrbanScheduleLayer
        from plone.browserlayer import utils
        self.assertIn(IUrbanScheduleLayer, utils.registered_layers())

    def test_testing_profile_is_registered(self):
        """
        Test testing profile is registered.
        """
        portal_setup = api.portal.get_tool(name='portal_setup')
        demo_profile_name = u'urban.schedule:testing'
        profile_ids = [info['id'] for info in portal_setup.listProfileInfo()]
        msg = 'testing profile is not registered'
        self.assertTrue(demo_profile_name in profile_ids, msg)


class TestUninstall(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['urban.schedule'])

    def test_product_uninstalled(self):
        """Test if urban.schedule is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'urban.schedule'))

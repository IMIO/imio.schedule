# -*- coding: utf-8 -*-

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import transaction

import unittest

import urban.schedule


class NakedPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=urban.schedule,
                      name='testing.zcml')
        z2.installProduct(app, 'urban.schedule')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'urban.schedule')

NAKED_PLONE_FIXTURE = NakedPloneLayer(
    name='NAKED_PLONE_FIXTURE'
)

NAKED_PLONE_INTEGRATION = IntegrationTesting(
    bases=(NAKED_PLONE_FIXTURE,),
    name='NAKED_PLONE_INTEGRATION'
)


class ScheduleLayer(NakedPloneLayer):

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'urban.schedule:default')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # Commit so that the test browser sees these objects
        transaction.commit()


TEST_INSTALL_FIXTURE = ScheduleLayer(
    name='TEST_INSTALL_FIXTURE'
)

TEST_INSTALL_INTEGRATION = IntegrationTesting(
    bases=(TEST_INSTALL_FIXTURE,),
    name='TEST_INSTALL_INTEGRATION'
)


TEST_INSTALL_FUNCTIONAL = FunctionalTesting(
    bases=(TEST_INSTALL_FIXTURE,),
    name='TEST_INSTALL_FUNCTIONAL'
)


class ExampleScheduleLayer(ScheduleLayer):

    def setUpPloneSite(self, portal):
        super(ExampleScheduleLayer, self).setUpPloneSite(portal)

        applyProfile(portal, 'urban.schedule:testing')

        # Commit so that the test browser sees these objects
        transaction.commit()


EXAMPLE_SCHEDULE_FIXTURE = ExampleScheduleLayer(
    name='EXAMPLE_SCHEDULE_FIXTURE'
)

EXAMPLE_SCHEDULE_INTEGRATION = IntegrationTesting(
    bases=(EXAMPLE_SCHEDULE_FIXTURE,),
    name='EXAMPLE_SCHEDULE_INTEGRATION'
)


EXAMPLE_SCHEDULE_FUNCTIONAL = FunctionalTesting(
    bases=(EXAMPLE_SCHEDULE_FIXTURE,),
    name='EXAMPLE_SCHEDULE_FUNCTIONAL'
)


class ExampleScheduleIntegrationTestCase(unittest.TestCase):

    layer = EXAMPLE_SCHEDULE_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

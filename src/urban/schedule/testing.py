# -*- coding: utf-8 -*-

from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import z2

from urban.schedule.events.zope_registration import unsubscribe_task_configs_for_content_type

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
        z2.installProduct(app, 'imio.dashboard')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'urban.schedule')
        z2.uninstallProduct(app, 'imio.dashboard')

NAKED_PLONE_FIXTURE = NakedPloneLayer(
    name='NAKED_PLONE_FIXTURE'
)

NAKED_PLONE_INTEGRATION = IntegrationTesting(
    bases=(NAKED_PLONE_FIXTURE,),
    name='NAKED_PLONE_INTEGRATION'
)


class ScheduleLayer(NakedPloneLayer):

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.CMFPlone:plone')
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


class BaseTest(unittest.TestCase):
    """
    Helper class for tests.
    """

    def setUp(self):
        self.portal = self.layer['portal']


class BrowserTest(BaseTest):
    """
    Helper class for Browser tests.
    """

    def setUp(self):
        super(BrowserTest, self).setUp()
        self.browser = z2.Browser(self.portal)
        self.browser.handleErrors = False

    def browser_login(self, user, password):
        login(self.portal, user)
        self.browser.open(self.portal.absolute_url() + '/logout')
        self.browser.open(self.portal.absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()


class ExampleScheduleTestBase(BrowserTest):

    def setUp(self):
        super(ExampleScheduleTestBase, self).setUp()

        self.portal.portal_workflow.setDefaultChain("simple_publication_workflow")

        self.schedule_config = self.portal.config.test_scheduleconfig
        self.task_config = self.schedule_config.test_taskconfig
        self.empty_task_container = self.portal.test_empty_taskcontainer
        self.task_container = self.portal.test_taskcontainer
        self.task = self.task_container.objectValues()[0]

        # commit to save the setup in the tests.
        transaction.commit()

        self.browser_login(TEST_USER_NAME, TEST_USER_PASSWORD)


class ExampleScheduleIntegrationTestCase(ExampleScheduleTestBase):

    layer = EXAMPLE_SCHEDULE_INTEGRATION


class ExampleScheduleFunctionalTestCase(ExampleScheduleTestBase):

    layer = EXAMPLE_SCHEDULE_FUNCTIONAL

    def tearDown(self):
        """
        Unregister the adapters here since the zope instance never shut downs.
        """
        unsubscribe_task_configs_for_content_type(self.task_config, None)

        api.content.delete(self.task)
        api.content.delete(self.task_container)
        api.content.delete(self.empty_task_container)
        api.content.delete(self.task_config)
        api.content.delete(self.schedule_config)

        transaction.commit()

        super(ExampleScheduleTestBase, self).tearDown()

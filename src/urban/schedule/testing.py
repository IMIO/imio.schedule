# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import urban.schedule


class UrbanScheduleLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=urban.schedule)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'urban.schedule:default')


URBAN_SCHEDULE_FIXTURE = UrbanScheduleLayer()


URBAN_SCHEDULE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(URBAN_SCHEDULE_FIXTURE,),
    name='UrbanScheduleLayer:IntegrationTesting'
)


URBAN_SCHEDULE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(URBAN_SCHEDULE_FIXTURE,),
    name='UrbanScheduleLayer:FunctionalTesting'
)


URBAN_SCHEDULE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        URBAN_SCHEDULE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='UrbanScheduleLayer:AcceptanceTesting'
)

# -*- coding: utf-8 -*-

from plone import api

from Products.ATContentTypes.interfaces import IATDocument

from urban.schedule.interfaces import IToTaskConfig
from urban.schedule.testing import ExampleScheduleFunctionalTestCase
from urban.schedule.utils import interface_to_tuple

from zope.component import getAdapter
from zope.component import queryAdapter
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class TestAdaptersRegistration(ExampleScheduleFunctionalTestCase):
    """
    Test the automated IToTaskConfig adapters registration.
    """

    def test_registration_at_instance_start(self):
        """
        Sice we can not simulate a instance restart in the tests
        Just check that we when through the event handler by checking
        the var  '_registered_sites'.
        """
        from urban.schedule.events import zope_registration

        self.assertTrue(len(zope_registration._registered_sites) > 0)

    def test_registration_on_TaskConfig_creation(self):
        """
        When creating a new TaskConfig,
        a new adapter should be registered with:
            for: ATFolder (type selected on the ScheduleConfig of this TaskConfig)
            provides: IToTaskConfig
            name: this TaskConfig UID
        """

        task_config = api.content.create(
            type='TaskConfig',
            id='task_config_2',
            container=self.schedule_config
        )

        folder = self.portal.config
        adapter = queryAdapter(folder, IToTaskConfig, task_config.UID())
        msg = "an adapter should have been registered when creating a new TaskConfig"
        self.assertTrue(adapter is not None, msg)

        # delete the task config and unregister its adapter manually since tests layer
        # tearDown cannot take care of this
        api.content.delete(task_config)

    def test_unregistration_on_TaskConfig_deletion(self):
        """
        When deleting a TaskConfig, its IToTaskConfig adapter should be unregistered
        """

        task_config = api.content.create(
            type='TaskConfig',
            id='task_config_2',
            container=self.schedule_config
        )

        # to test unregistration, we have to be sure something was registered
        folder = self.portal.config
        adapter = getAdapter(folder, IToTaskConfig, task_config.UID())
        msg = "an adapter providing IToTaskConfig should have been registered for IATFolder"
        self.assertTrue(adapter is not None, msg)

        api.content.delete(task_config)
        adapter = queryAdapter(folder, IToTaskConfig, task_config.UID())
        msg = "the adapter should have been unregistered when deleting the TaskConfig"
        self.assertTrue(adapter is None, msg)

    def test_adapters_update_on_LicenceSchedule_modification(self):
        """
        When an other content type is selected on the field 'scheduled_contenttype'
        of a ScheduleConfig, we have to unregister all the IToTaskConfig adapter of
        each TaskConfig of this ScheduleConfig and register them back for the new
        portal_type.
        """
        schedule_config = self.schedule_config
        task_config = self.task_config
        folder = self.portal.config
        document = api.content.create(type='Document', id='doc', container=self.portal)

        # the adapter should be registered for IATFolder
        adapter = getAdapter(folder, IToTaskConfig, task_config.UID())
        msg = "an adapter providing IToTaskConfig should have been registered for IATFolder"
        self.assertTrue(adapter is not None, msg)

        #... but not for IATDocument
        adapter = queryAdapter(document, IToTaskConfig, task_config.UID())
        msg = "not adapter should have been registered for IATDocument yet..."
        self.assertTrue(adapter is None, msg)

        # modify 'scheduled_contenttype' then manually trigger the modification event
        schedule_config.scheduled_contenttype = ('Document', interface_to_tuple(IATDocument))
        notify(ObjectModifiedEvent(schedule_config))

        # old IToTaskConfig adapter should be unregistered for IATFolder
        adapter = queryAdapter(folder, IToTaskConfig, task_config.UID())
        msg = "the adapter should have been unregistered when modifying the ScheduleConfig"
        self.assertTrue(adapter is None, msg)

        # new IToTaskConfig adapter should be registered for IATDocument
        adapter = queryAdapter(document, IToTaskConfig, task_config.UID())
        msg = "an adapter providing IToTaskConfig should have been registered for IATDocument"
        self.assertTrue(adapter is not None, msg)

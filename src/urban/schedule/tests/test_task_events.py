# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.content.task import IScheduleTask
from urban.schedule.testing import ExampleScheduleFunctionalTestCase

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class TestTaskCreation(ExampleScheduleFunctionalTestCase):
    """
    Test the automated IToTaskConfig adapters registration.
    """

    def test_task_creation_on_container_modification(self):
        """
        When modifying a contentype scheduled with a ScheduleConfig
        Task should created automatically depending on start conditions
        and starting_state.
        """
        empty_task_container = self.empty_task_container
        msg = "so far, no task should have been created"
        self.assertEquals(len(empty_task_container.objectValues()), 0, msg)

        # simulate modification
        notify(ObjectModifiedEvent(empty_task_container))

        created = empty_task_container.objectValues()
        created = created and created[0]

        # a task should have been created
        msg = "A task should have been created"
        self.assertTrue(created, msg)

        msg = "The object created should have been a Task but is {}".format(
            created.portal_type
        )
        self.assertTrue(IScheduleTask.providedBy(created), msg)

    def test_task_creation_on_container_creation(self):
        """
        When creating a contentype scheduled with a ScheduleConfig
        Task should created automatically depending on start conditions
        and starting_state.
        """
        new_task_container = api.content.create(
            type='Folder',
            id='new_task_container',
            container=self.portal
        )

        created = new_task_container.objectValues()
        created = created and created[0]

        # a task should have been created
        msg = "A task should have been created"
        self.assertTrue(created, msg)

        msg = "The object created should have been a Task but is {}".format(
            created.portal_type
        )
        self.assertTrue(IScheduleTask.providedBy(created), msg)

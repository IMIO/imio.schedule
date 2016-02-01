# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.content.task import IScheduleTask
from urban.schedule.testing import ExampleScheduleFunctionalTestCase

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class TestTaskCreation(ExampleScheduleFunctionalTestCase):
    """
    Test task creation with different changes of TaskContainer.
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

    def test_task_creation_on_container_workflow_modification(self):
        """
        When changing state of a contentype scheduled with a ScheduleConfig
        Task should created automatically depending on start conditions
        and starting_state.
        """
        empty_task_container = self.empty_task_container
        msg = "so far, no task should have been created"
        self.assertEquals(len(empty_task_container.objectValues()), 0, msg)

        # do workflow change
        api.content.transition(empty_task_container, transition='submit')
        api.content.transition(empty_task_container, transition='retract')

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


class TestTaskEnding(ExampleScheduleFunctionalTestCase):
    """
    Test task ending with different changes of TaskContainer.
    """

    def test_task_ending_on_container_modification(self):
        """
        When modifying a contentype scheduled with a ScheduleConfig
        Task should ended automatically depending on end conditions
        and ending_states.
        """
        task_container = self.task_container
        task = self.task

        # put the task container on 'pending' state to match 'ending states'
        api.content.transition(task_container, transition='submit')
        # reopen the task to be sure it was not closed before the container
        # modification
        api.content.transition(task, 'back_in_realized')
        msg = "The task should not be closed yet ! (for the sake of the test)"
        self.assertNotEquals(api.content.get_state(task), 'closed', msg)

        # simulate modification
        notify(ObjectModifiedEvent(task_container))

        # the task should have been ended
        msg = "The task should have been ended"
        self.assertEquals(api.content.get_state(task), 'closed', msg)

    def test_task_ending_on_container_workflow_modification(self):
        """
        When changing state a contentype scheduled with a ScheduleConfig
        Task should ended automatically depending on end conditions
        and ending_states.
        """
        task_container = self.task_container
        task = self.task

        msg = "The task should not be closed yet ! (for the sake of the test)"
        self.assertNotEquals(api.content.get_state(task), 'closed', msg)

        # do workflow change
        api.content.transition(task_container, transition='submit')

        # the task should have been ended
        msg = "The task should have been ended"
        self.assertEquals(api.content.get_state(task), 'closed', msg)

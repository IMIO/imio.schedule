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

    def test_assigned_user_is_set_on_created_task(self):
        """
        Check that the assigned user is set on an
        automatically created task.
        """
        msg = 'default assigned user should have been admin'
        self.assertEquals(self.task.assigned_user, 'admin', msg)

    def test_due_date_is_set_on_created_task(self):
        """
        Check that the computed due date is set on an
        automatically created task.
        """
        msg = 'default du date should have been today + 10 days'
        due_date = self.task.due_date
        expected_date = self.task_container.creation_date + 10
        expected_date = expected_date.asdatetime().date()
        self.assertEquals(due_date, expected_date, msg)


class TestTaskUpdate(ExampleScheduleFunctionalTestCase):
    """
    Test task update with different changes of TaskContainer.
    """

    def test_update_due_date_on_container_modification(self):
        """
        When modifying a contentype scheduled with a ScheduleConfig
        Task due date should be updated.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task
        old_due_date = task.due_date

        # set an additional delay of 42 days on the task config
        task_config.additional_delay = 42
        msg = "The task due date should not have changed"
        self.assertEquals(task.due_date, old_due_date)

        # simulate modification
        notify(ObjectModifiedEvent(task_container))

        msg = "The task due date should have been updated"
        self.assertNotEquals(task.due_date, old_due_date, msg)

    def test_reindex_due_date_on_container_modification(self):
        """
        When modifying a contentype scheduled with a ScheduleConfig
        Task due date should be updated and reindexed.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task
        old_due_date = task.due_date

        # set an additional delay of 42 days on the task config
        task_config.additional_delay = 42
        msg = "The task due date should not have changed"
        self.assertEquals(task.due_date, old_due_date)

        # simulate modification
        notify(ObjectModifiedEvent(task_container))

        catalog = api.portal.get_tool('portal_catalog')
        msg = 'catalog should not find anything with old due date'
        task_brain = catalog(due_date=old_due_date, UID=task.UID())
        self.assertFalse(task_brain, msg)
        msg = 'new due date should have been reindexed'
        task_brain = catalog(due_date=task.due_date, UID=task.UID())
        self.assertTrue(task_brain, msg)

    def test_task_ending_on_container_workflow_modification(self):
        """
        When changing state a contentype scheduled with a ScheduleConfig
        Task should end automatically depending on end conditions
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

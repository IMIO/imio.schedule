# -*- coding: utf-8 -*-

from Acquisition import aq_base

from urban.schedule.testing import ExampleScheduleIntegrationTestCase
from urban.schedule.testing import TEST_INSTALL_INTEGRATION

from plone import api

import unittest


class TestTaskConfig(unittest.TestCase):
    """
    Test TaskConfig content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_TaskConfig_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('TaskConfig' in registered_types)


class TestTaskConfigFields(ExampleScheduleIntegrationTestCase):
    """
    Test schema fields declaration.
    """

    def test_class_registration(self):
        """
        Check if the class of the content type TaskConfig is the
        correct one.
        """
        from urban.schedule.content.task_config import TaskConfig
        self.assertTrue(self.task_config.__class__ == TaskConfig)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type TaskConfig is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.task_config.portal_type)
        self.assertTrue('ITaskConfig' in taskconfig_type.schema)

    def test_default_assigned_user_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'default_assigned_user'))

    def test_default_assigned_user_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'default_assigned_user' is not displayed"
        self.assertTrue('id="form-widgets-default_assigned_user"' in contents, msg)
        msg = "field 'default_assigned_user' is not translated"
        self.assertTrue('Responsable de la tâche' in contents, msg)

    def test_default_assigned_user_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'default_assigned_user' is not editable"
        self.assertTrue('Responsable de la tâche' in contents, msg)

    def test_start_conditions_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'start_conditions'))

    def test_start_conditions_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'start_conditions' is not displayed"
        self.assertTrue('id="form-widgets-start_conditions"' in contents, msg)
        msg = "field 'start_conditions' is not translated"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_start_conditions_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'start_conditions' is not editable"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_starting_state_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'starting_state'))

    def test_starting_state_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'starting_state' is not displayed"
        self.assertTrue('id="form-widgets-starting_state"' in contents, msg)
        msg = "field 'starting_state' is not translated"
        self.assertTrue('État de création de la tâche' in contents, msg)

    def test_starting_state_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'starting_state' is not editable"
        self.assertTrue('État de création de la tâche' in contents, msg)

    def test_end_conditions_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'end_conditions'))

    def test_end_conditions_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'end_conditions' is not displayed"
        self.assertTrue('id="form-widgets-end_conditions"' in contents, msg)
        msg = "field 'end_conditions' is not translated"
        self.assertTrue('Conditions de clôture' in contents, msg)

    def test_end_conditions_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'end_conditions' is not editable"
        self.assertTrue('Conditions de clôture' in contents, msg)

    def test_ending_states_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'ending_states'))

    def test_ending_states_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'ending_states' is not displayed"
        self.assertTrue('id="form-widgets-ending_states"' in contents, msg)
        msg = "field 'ending_states' is not translated"
        self.assertTrue('État(s) de clôture de la tâche' in contents, msg)

    def test_ending_states_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'ending_states' is not editable"
        self.assertTrue('État(s) de clôture de la tâche' in contents, msg)

    def test_start_date_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'start_date'))

    def test_start_date_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'start_date' is not displayed"
        self.assertTrue('id="form-widgets-start_date"' in contents, msg)
        msg = "field 'start_date' is not translated"
        self.assertTrue('Date de départ' in contents, msg)

    def test_start_date_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'start_date' is not editable"
        self.assertTrue('Date de départ' in contents, msg)

    def test_additional_delay_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'additional_delay'))

    def test_additional_delay_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'additional_delay' is not displayed"
        self.assertTrue('id="form-widgets-additional_delay"' in contents, msg)
        msg = "field 'additional_delay' is not translated"
        self.assertTrue('Délai supplémentaire' in contents, msg)

    def test_additional_delay_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'additional_delay' is not editable"
        self.assertTrue('Délai supplémentaire' in contents, msg)


class TestTaskConfigIntegration(ExampleScheduleIntegrationTestCase):
    """
    Test TaskConfig methods.
    """

    def test_get_task_type(self):
        """
        Should return 'ScheduleTask'
        """
        task_type = self.task_config.get_task_type()
        expected_type = 'ScheduleTask'
        self.assertEquals(task_type, expected_type)

    def test_get_schedule_config(self):
        """
        Should return the parent schedule config.
        """
        config = self.task_config.get_schedule_config()
        expected_config = self.schedule_config
        self.assertEquals(config, expected_config)

    def test_get_scheduled_portal_type(self):
        """
        Sould return the portal_type of the content type selected on the field
        'scheduled_contenttype' of the parent ScheduleConfig.
        """
        portal_type = self.task_config.get_scheduled_portal_type()
        expected_type = 'Folder'
        self.assertEquals(portal_type, expected_type)

    def test_get_scheduled_interface(self):
        """
        Should return the Interface (or a class) of the content type selected
        on the field 'scheduled_contenttype' of the parent ScheduleConfig.
        """
        from Products.ATContentTypes.interfaces import IATFolder

        type_interface = self.task_config.get_scheduled_interface()
        expected_interface = IATFolder
        self.assertEquals(type_interface, expected_interface)

    def test_query_task_instances(self):
        """
        Should return ScheduleTask brains in a container created from a given TaskConfig.
        """
        task_config = self.task_config

        root = self.portal
        tasks = task_config.query_task_instances(root, the_objects=True)
        msg = "Should have found at least one ScheduleTask"
        self.assertEquals(tasks, [self.task], msg)

        root = self.empty_task_container
        tasks = task_config.query_task_instances(root, the_objects=True)
        msg = "Should not have found any ScheduleTask"
        self.assertEquals(tasks, [], msg)

    def test_get_task(self):
        """
        Should return the unique Task of task_container created from
        this TaskConfig.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        task_found = task_config.get_task(task_container)
        self.assertEquals(task_found, task)
        # round trip test
        msg = "The TaskConfig of the task found should be the original one"
        self.assertEquals(task_found.get_task_config(), task_config, msg)

    def test_get_open_task(self):
        """
        Should return the unique Task of task_container created from
        this TaskConfig only if it is still open.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        # normal case
        task_found = task_config.get_open_task(task_container)
        self.assertEquals(task_found, task)
        msg = "Task found should not be on 'closed' state"
        task_state = api.content.get_state(task_found)
        self.assertNotEquals(task_state, 'closed', msg)

        # round trip test
        msg = "The TaskConfig of the task found should be the original one"
        self.assertEquals(task_found.get_task_config(), task_config, msg)

        # close the task, get_open_task should not find it
        task_config.end_task(task)
        task_state = api.content.get_state(task)
        self.assertEquals(task_state, 'closed')
        task_found = task_config.get_open_task(task_container)
        msg = 'No task should have been found'
        self.assertEquals(task_found, None, msg)

    def test_get_closed_task(self):
        """
        Should return the unique Task of task_container created from
        this TaskConfig only if it is closed.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        # the task is not closed, nothing should be found yet
        task_state = api.content.get_state(task)
        self.assertNotEquals(task_state, 'closed')
        task_found = task_config.get_closed_task(task_container)
        msg = 'No task should have been found'
        self.assertEquals(task_found, None, msg)

        # close the task
        task_config.end_task(task)
        # normal case
        task_found = task_config.get_closed_task(task_container)
        self.assertEquals(task_found, task)
        msg = "Task found should be on 'closed' state"
        task_state = api.content.get_state(task_found)
        self.assertEquals(task_state, 'closed', msg)

        # round trip test
        msg = "The TaskConfig of the task found should be the original one"
        self.assertEquals(task_found.get_task_config(), task_config, msg)

    def test_task_already_exists(self):
        """
        Should tell wheter the task container already have a task from
        this TaskConfig.
        """
        task_config = self.task_config

        task_container = self.task_container
        msg = "TaskConfig of the existing task found should be the original task_config"
        self.assertTrue(task_config.task_already_exists(task_container), msg)

        empty_task_container = self.empty_task_container
        msg = "no existing task should have been found on empty container"
        self.assertFalse(task_config.task_already_exists(empty_task_container), msg)

    def test_should_start_task(self):
        """
        Test different cases for the 'should_start_task' method.
        """
        task_config = self.task_config
        task_container = self.task_container
        empty_task_container = self.empty_task_container

        # case of task already existing
        msg = "Task should not be started because it already exists"
        self.assertFalse(task_config.should_start_task(task_container), msg)

        # normal case
        msg = "Task should be started"
        start = task_config.should_start_task(empty_task_container)
        self.assertTrue(start, msg)

        # set the task_config field 'start_conditions' with a negative condition
        # => task should not start
        task_config.start_conditions = ('urban.schedule.negative_start_condition',)
        msg = "Task should not be started because the start condition is not matched"
        self.assertFalse(task_config.should_start_task(empty_task_container), msg)

        # set the task_config starting_state field to a state different from
        # the task_container state => task should not start
        task_config.starting_state = 'pending'
        msg = "Task should not be started because the starting state does not match container state"
        self.assertFalse(task_config.should_start_task(empty_task_container), msg)

    def test_should_end_task(self):
        """
        Test different cases for the 'should_end_task' method.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        # task container state is different from the states selected on
        # task_config 'ending_states' => task should not end
        msg = "Task should not be ended because the ending state does not match container state"
        self.assertFalse(task_config.should_end_task(task_container, task), msg)

        # normal case
        api.content.transition(obj=task_container, transition='submit')
        msg = "Task should be ended"
        end = task_config.should_end_task(task_container, task)
        self.assertTrue(end, msg)

        # set the task_config field 'end_conditions' with a negative condition
        # => task should not end
        task_config.end_conditions = ('urban.schedule.negative_end_condition',)
        msg = "Task should not be ended because the end condition is not matched"
        self.assertFalse(task_config.should_end_task(task_container, task), msg)

        # set the task_config ending_states field to a state different from
        # the task_container state => task should not end
        task_config.ending_states = ('pending',)
        msg = "Task should not be ended because the ending state does not match container state"
        self.assertFalse(task_config.should_end_task(task_container, task), msg)

    def test_end_task(self):
        """
        Default implementation is to put the task on the state 'closed'.
        """
        task_config = self.task_config
        task = self.task

        task_state = api.content.get_state(task)
        self.assertNotEquals(task_state, 'closed')

        task_config.end_task(task)
        task_state = api.content.get_state(task)
        msg = "Task should be on state 'closed'"
        self.assertEquals(task_state, 'closed', msg)

    def test_compute_due_date(self):
        """
        Due date should be the date computed by the adapter of
        start_date field + the value in additional_delay.
        """
        task_config = self.task_config
        task_container = self.task_container

        expected_date = task_container.creation_date + task_config.additional_delay
        expected_date = expected_date.asdatetime().date()

        due_date = task_config.compute_due_date(task_container)
        self.assertEquals(due_date, expected_date)

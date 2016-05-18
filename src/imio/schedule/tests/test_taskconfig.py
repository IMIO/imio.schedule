# -*- coding: utf-8 -*-

from Acquisition import aq_base

from imio.schedule.config import DONE
from imio.schedule.content.task import AutomatedMacroTask
from imio.schedule.content.task import AutomatedTask
from imio.schedule.testing import ExampleScheduleFunctionalTestCase
from imio.schedule.testing import ExampleScheduleIntegrationTestCase
from imio.schedule.testing import MacroTaskScheduleIntegrationTestCase
from imio.schedule.testing import TEST_INSTALL_INTEGRATION

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
        from imio.schedule.content.task_config import TaskConfig
        self.assertTrue(self.task_config.__class__ == TaskConfig)

    def test_schema_registration(self):
        """
        Check if the schema Interface of the content type TaskConfig is the
        correct one.
        """
        portal_types = api.portal.get_tool('portal_types')
        taskconfig_type = portal_types.get(self.task_config.portal_type)
        self.assertTrue('ITaskConfig' in taskconfig_type.schema)

    def test_enabled_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'enabled'))

    def test_enabled_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'enabled' is not displayed"
        self.assertTrue('id="form-widgets-enabled"' in contents, msg)
        msg = "field 'enabled' is not translated"
        self.assertTrue('Activé' in contents, msg)

    def test_enabled_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'enabled' is not editable"
        self.assertTrue('Activé' in contents, msg)

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

    def test_creation_conditions_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'creation_conditions'))

    def test_creation_conditions_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'creation_conditions' is not displayed"
        self.assertTrue('id="form-widgets-creation_conditions"' in contents, msg)
        msg = "field 'creation_conditions' is not translated"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_creation_conditions_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'creation_conditions' is not editable"
        self.assertTrue('Conditions de création' in contents, msg)

    def test_creation_state_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'creation_state'))

    def test_creation_state_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'creation_state' is not displayed"
        self.assertTrue('id="form-widgets-creation_state"' in contents, msg)
        msg = "field 'creation_state' is not translated"
        self.assertTrue('État de création de la tâche' in contents, msg)

    def test_creation_state_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'creation_state' is not editable"
        self.assertTrue('État de création de la tâche' in contents, msg)

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

    def test_starting_states_attribute(self):
        task_config = aq_base(self.task_config)
        self.assertTrue(hasattr(task_config, 'starting_states'))

    def test_starting_states_field_display(self):
        self.browser.open(self.task_config.absolute_url())
        contents = self.browser.contents
        msg = "field 'starting_states' is not displayed"
        self.assertTrue('id="form-widgets-starting_states"' in contents, msg)
        msg = "field 'starting_states' is not translated"
        self.assertTrue('État(s) de démarrage de la tâche' in contents, msg)

    def test_starting_states_field_edit(self):
        self.browser.open(self.task_config.absolute_url() + '/edit')
        contents = self.browser.contents
        msg = "field 'starting_states' is not editable"
        self.assertTrue('État(s) de démarrage de la tâche' in contents, msg)

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


class TestTaskConfigMethodsIntegration (ExampleScheduleIntegrationTestCase):
    """
    Test TaskConfig methods.
    """

    def test_get_task_type(self):
        """
        Should return 'AutomatedTask'
        """
        task_type = self.task_config.get_task_type()
        expected_type = 'AutomatedTask'
        self.assertEquals(task_type, expected_type)

    def test_is_main_taskconfig(self):
        """
        Tells wheter a task config is a subtaskconfig or not
        """
        msg = "this simple task config should be considered as a main task config"
        self.assertTrue(self.task_config.is_main_taskconfig(), msg)

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

    def test_user_to_assign(self):
        """
        Should return a user to assign on a task.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        user = task_config.user_to_assign(task_container, task)
        expected_user = 'test-user'
        msg = "should have return '{}' user id".format(expected_user)
        self.assertEquals(user, expected_user, msg)

    def test_query_task_instances(self):
        """
        Should return AutomatedTask brains in a container created from a given TaskConfig.
        """
        task_config = self.task_config

        root = self.portal
        tasks = task_config.query_task_instances(root, the_objects=True)
        msg = "Should have found at least one AutomatedTask"
        self.assertEquals(tasks, [self.task], msg)

        root = self.empty_task_container
        tasks = task_config.query_task_instances(root, the_objects=True)
        msg = "Should not have found any AutomatedTask"
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

    def test_get_created_task(self):
        """
        Should return the unique Task of task_container created from
        this TaskConfig if it is in the state 'created'.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        task_found = task_config.get_created_task(task_container)
        self.assertEquals(task_found, task)

    def test_get_started_task(self):
        """
        Should return the unique Task of task_container created from
        this TaskConfig if it is in the state 'created'.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        # so far nothing should be found
        task_found = task_config.get_started_task(task_container)
        self.assertFalse(task_found)

        # start the task
        api.content.transition(obj=task, transition='do_to_assign')

        task_found = task_config.get_started_task(task_container)
        msg = "should have found the started task"
        self.assertEquals(task_found, task, msg)

    def test_get_open_task(self):
        """
        Should return the unique Task of task_container created from
        this TaskConfig if it is in the state 'created' or 'to_do'.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        task_found = task_config.get_open_task(task_container)
        msg = "should have found the created task"
        self.assertEquals(task_found, task, msg)

        # start the task
        api.content.transition(obj=task, transition='do_to_assign')

        task_found = task_config.get_open_task(task_container)
        msg = "should have found the started task"
        self.assertEquals(task_found, task, msg)

        # close the task
        task_config.end_task(task)

        task_found = task_config.get_open_task(task_container)
        msg = "should not have found the closed task"
        self.assertFalse(task_found, msg)

    def test_get_closed_task(self):
        """
        Should return the unique Task of task_container created from
        this TaskConfig if it is in the state 'closed'.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        # so far nothing should be found
        task_found = task_config.get_closed_task(task_container)
        self.assertFalse(task_found)

        # close the task
        task_config.end_task(task)

        task_found = task_config.get_closed_task(task_container)
        msg = "should have found the closed task"
        self.assertEquals(task_found, task, msg)

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

    def test_should_create_task(self):
        """
        Test different cases for the 'should_create_task' method.
        """
        task_config = self.task_config
        task_container = self.task_container
        empty_task_container = self.empty_task_container

        # case of task already existing
        msg = "Task should not be created because it already exists"
        self.assertFalse(task_config.should_create_task(task_container), msg)

        # normal case
        msg = "Task should be created"
        create = task_config.should_create_task(empty_task_container)
        self.assertTrue(create, msg)

        # disable the task config => task should not be created
        task_config.enabled = False
        msg = "Task should not be created because the creation condition is not matched"
        self.assertFalse(task_config.should_create_task(empty_task_container), msg)

        # set the task_config field 'creation_conditions' with a negative condition
        # => task should not be created
        task_config.enabled = True
        task_config.creation_conditions = [type('condition', (object, ), {
            'condition': 'schedule.negative_creation_condition',
            'operator': 'AND',
        })()]
        msg = "Task should not be created because the creation condition is not matched"
        self.assertFalse(task_config.should_create_task(empty_task_container), msg)

        # set the task_config starting_states field to a state different from
        # the task_container state => task should not be created
        task_config.creation_conditions = [type('condition', (object, ), {
            'condition': 'schedule.test_creation_condition',
            'operator': 'AND',
        })()]
        task_config.creation_state = 'pending'
        msg = "Task should not be created because the creation state does not match container state"
        self.assertFalse(task_config.should_create_task(empty_task_container), msg)

    def test_should_start_task(self):
        """
        Test different cases for the 'should_start_task' method.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        # task container state is different from the states selected on
        # task_config 'starting_states' => task should not start
        msg = "Task should not be started because the starting state does not match container state"
        self.assertFalse(task_config.should_start_task(task_container, task), msg)

        # normal case
        api.content.transition(obj=task_container, transition='submit')
        msg = "Task should be started"
        start = task_config.should_start_task(task_container, task)
        self.assertTrue(start, msg)

        # set the task_config field 'start_conditions' with a negative condition
        # => task should not start
        task.assigned_user = None
        msg = "Task should not be started because no user is defined on the task"
        self.assertFalse(task_config.should_start_task(task_container, task), msg)

        # set the task_config field 'start_conditions' with a negative condition
        # => task should not start
        task.assigned_user = 'user'
        task_config.start_conditions = [type('condition', (object, ), {
            'condition': 'schedule.negative_start_condition',
            'operator': 'AND',
        })()]
        msg = "Task should not be started because the start condition is not matched"
        self.assertFalse(task_config.should_start_task(task_container, task), msg)

        # set the task_config starting_states field to a state different from
        # the task_container state => task should not start
        task_config.start_conditions = [type('condition', (object, ), {
            'condition': 'schedule.test_start_condition',
            'operator': 'AND',
        })()]
        task_config.starting_states = ('published',)
        msg = "Task should not be started because the starting state does not match container state"
        self.assertFalse(task_config.should_start_task(task_container, task), msg)

    def test_start_conditions_status(self):
        """
        Test different cases for the 'start_conditions_status' method.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        matched_conditions, unmatched_conditions = task_config.start_conditions_status(task_container, task)
        self.assertTrue(matched_conditions == [('schedule.test_start_condition', True)])
        self.assertTrue(unmatched_conditions == [])

        task_config.start_conditions = [type('condition', (object, ), {
            'condition': 'schedule.negative_start_condition',
            'operator': 'AND',
        })()]
        matched_conditions, unmatched_conditions = task_config.start_conditions_status(task_container, task)
        self.assertTrue(matched_conditions == [])
        self.assertTrue(unmatched_conditions == [('schedule.negative_start_condition', False)])

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
        api.content.transition(obj=task_container, transition='publish')
        msg = "Task should be ended"
        end = task_config.should_end_task(task_container, task)
        self.assertTrue(end, msg)

        # set the task_config field 'end_conditions' with a negative condition
        # => task should not end
        task_config.end_conditions = [type('object', (object, ), {
            'condition': 'schedule.negative_end_condition',
            'operator': 'AND',
        })()]
        msg = "Task should not be ended because the end condition is not matched"
        self.assertFalse(task_config.should_end_task(task_container, task), msg)

        # set the task_config ending_states field to a state different from
        # the task_container state => task should not end
        task_config.ending_states = ('pending',)
        msg = "Task should not be ended because the ending state does not match container state"
        self.assertFalse(task_config.should_end_task(task_container, task), msg)

    def test_end_conditions_status(self):
        """
        Test different cases for the 'end_conditions_status' method.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        matched_conditions, unmatched_conditions = task_config.end_conditions_status(task_container, task)
        self.assertTrue(matched_conditions == [('schedule.test_end_condition', True)])
        self.assertTrue(unmatched_conditions == [])

        task_config.end_conditions = [type('condition', (object, ), {
            'condition': 'schedule.negative_end_condition',
            'operator': 'AND',
        })()]
        matched_conditions, unmatched_conditions = task_config.end_conditions_status(task_container, task)
        self.assertTrue(matched_conditions == [])
        self.assertTrue(unmatched_conditions == [('schedule.negative_end_condition', False)])

    def test_create_task(self):
        """
        Should create a task.
        """
        task_container = self.empty_task_container
        task_config = self.task_config

        created_task = task_config.create_task(task_container)

        self.assertTrue(isinstance(created_task, AutomatedTask))

    def test_start_task(self):
        """
        Should start a task.
        """
        task_config = self.task_config
        task = self.task

        msg = "task should not be started yet (for the sake of the test..)"
        self.assertEquals(api.content.get_state(task), 'created', msg)

        task_config.start_task(task)

        msg = "task should have been started"
        self.assertEquals(api.content.get_state(task), 'to_do', msg)

    def test_end_task(self):
        """
        Should end a task.
        """
        task_config = self.task_config
        task = self.task

        msg = "task should not be ended yet (for the sake of the test..)"
        self.assertEquals(api.content.get_state(task), 'created', msg)

        task_config.end_task(task)

        msg = "task should have been ended"
        self.assertEquals(api.content.get_state(task), 'closed', msg)

    def test_compute_due_date(self):
        """
        Due date should be the date computed by the adapter of
        start_date field + the value in additional_delay.
        """
        task_config = self.task_config
        task_container = self.task_container
        task = self.task

        expected_date = task_container.creation_date + task_config.additional_delay
        expected_date = expected_date.asdatetime().date()

        due_date = task_config.compute_due_date(task_container, task)
        self.assertEquals(due_date, expected_date)


class TestTaskConfigMethodsFunctional(ExampleScheduleFunctionalTestCase):
    """
    Test TaskConfig methods.
    """

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


class TestMacroTaskConfig(unittest.TestCase):
    """
    Test MacroTaskConfig content type.
    """

    layer = TEST_INSTALL_INTEGRATION

    def test_MacroTaskConfig_portal_type_is_registered(self):
        portal_types = api.portal.get_tool('portal_types')
        registered_types = portal_types.listContentTypes()
        self.assertTrue('MacroTaskConfig' in registered_types)


class TestMacroTaskConfigMethodsIntegration(MacroTaskScheduleIntegrationTestCase):
    """
    Test MacroTaskConfig methods.
    """

    def test_MacroTasConfigk_inherits_from_TaskConfig(self):
        """
        MacroTaskConfig implements ITaskConfig and should implements all
        the methods defined in TaskConfig.
        As long MacroTaskConfig inherits from BaseTaskConfig, we test the inherited
        methods only in TaskConfig test cases to avoid test code duplication.
        """
        from imio.schedule.content.task_config import MacroTaskConfig
        from imio.schedule.content.task_config import BaseTaskConfig
        msg = "MacroTaskConfig should inherits BaseTaskConfig"
        self.assertTrue(issubclass(MacroTaskConfig, BaseTaskConfig), msg)

    def test_get_task_type(self):
        """
        Should return 'AutomatedMacroTask'
        """
        task_type = self.macrotask_config.get_task_type()
        expected_type = 'AutomatedMacroTask'
        self.assertEquals(task_type, expected_type)

    def test_get_subtask_configs(self):
        """
        Should return all the subtasks configs of a macro task.
        """
        subtasks_configs = self.macrotask_config.get_subtask_configs()
        msg = "sould have return the subtask config"
        self.assertTrue(len(subtasks_configs) == 1, msg)
        self.assertTrue(subtasks_configs[0] == self.subtask_config, msg)

    def test_is_main_taskconfig(self):
        """
        Tells wheter a task config is a subtaskconfig or not
        """
        msg = "this macrotask config should be considered as a main task config"
        self.assertTrue(self.macrotask_config.is_main_taskconfig(), msg)
        msg = "this subtask config should not be considered as a main task config"
        self.assertFalse(self.subtask_config.is_main_taskconfig(), msg)

    def test_create_task(self):
        """
        Should create a macro task and all its subtasks.
        """
        task_container = self.empty_task_container
        task_config = self.macrotask_config

        created_macrotask = task_config.create_task(task_container)
        self.assertTrue(isinstance(created_macrotask, AutomatedMacroTask))

        created_subtask = created_macrotask.objectValues()[0]
        self.assertTrue(isinstance(created_subtask, AutomatedTask))

    def test_should_end_task(self):
        """
        Test different cases for the 'should_end_task' method.
        """
        macrotask_config = self.macrotask_config
        subtask_config = self.subtask_config
        task_container = self.task_container
        macrotask = self.macro_task
        subtask = self.sub_task

        # normal case
        api.content.transition(obj=task_container, transition='publish')

        msg = "SubTask should be ended"
        end = subtask_config.should_end_task(task_container, macrotask)
        self.assertTrue(end, msg)

        msg = "MacroTask should be ended"
        end = macrotask_config.should_end_task(task_container, subtask)
        self.assertTrue(end, msg)

        # re open the subtask => the macro task should not be ended as long
        # the subtask is open

        api.content.transition(obj=subtask, transition='back_in_realized')
        self.assertFalse(subtask.get_status() == DONE)

        msg = "MacroTask should not be ended as long its subtask is open"
        end = macrotask_config.should_end_task(task_container, subtask)
        self.assertFalse(end, msg)

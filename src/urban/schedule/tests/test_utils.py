# -*- coding: utf-8 -*-


from Products.ATContentTypes.interfaces import IATFolder

from urban.schedule.testing import ExampleScheduleIntegrationTestCase


class TestUtils(ExampleScheduleIntegrationTestCase):
    """
    Test all methods of utils.py module.
    """

    def test_get_all_schedule_configs(self):
        """
        Test the method get_all_schedule_configs.
        """
        from urban.schedule.utils import get_all_schedule_configs

        self.assertEquals([self.schedule_config], get_all_schedule_configs())

    def test_get_task_configs(self):
        """
        Test the method get_task_configs.
        """
        from urban.schedule.utils import get_task_configs

        folder = self.portal.config
        expected_UIDS = [task_config.UID() for task_config in self.schedule_config.objectValues()]
        task_config_UIDS = [task_config.UID() for task_config in get_task_configs(folder)]
        self.assertEqual(set(task_config_UIDS), set(expected_UIDS))

    def test_tuple_to_interface(self):
        """
        Should turn a tuple ('interface.module.path', 'Interface') into
        Interface class.
        """
        from urban.schedule.utils import tuple_to_interface

        expected_interface = IATFolder
        interface_tuple = ('Products.ATContentTypes.interfaces.folder', 'IATFolder')
        interface = tuple_to_interface(interface_tuple)
        self.assertEqual(interface, expected_interface)

    def test_interface_to_tuple(self):
        """
        Should turn an Interface class into a tuple:
        ('interface.module.path', 'Interface')
        """
        from urban.schedule.utils import interface_to_tuple

        expected_tuple = ('Products.ATContentTypes.interfaces.folder', 'IATFolder')
        interface_tuple = interface_to_tuple(IATFolder)
        self.assertEqual(interface_tuple, expected_tuple)

    def test_create_tasks_collection(self):
        """
        Test the method create_tasks_collection.
        """
        from urban.schedule.utils import create_tasks_collection
        task = self.task

        collection = create_tasks_collection(
            self.schedule_config,
            container=self.portal,
            id='my_collection'
        )

        collected = [brain.getObject() for brain in collection.queryCatalog()]
        msg = "collection should have returned all the tasks created from the test ScheduleConfig"
        self.assertEquals([task], collected, msg)

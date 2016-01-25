# -*- coding: utf-8 -*-

from plone import api


def schedule_example_install(context):
    """
    Example schedule install script.
    """
    if context.readDataFile('urbanschedule_testing.txt') is None:
        return

    # Monkey patch the default vocabulary for the field 'task_container'
    # to be able to select 'Folder' content type so we can test methods of this
    # field.
    from Products.ATContentTypes.interfaces import IATFolder
    from urban.schedule.content.vocabulary import ScheduledContentTypeVocabulary

    def monkey_allowed_types(self):
        return{'Folder': IATFolder}
    ScheduledContentTypeVocabulary.content_types = monkey_allowed_types
    # Monkey patch end.

    site = api.portal.get()

    cfg_folder = api.content.create(
        container=site,
        type='Folder',
        id='config',
        title='Task configs'
    )

    test_scheduleconfig = api.content.create(
        container=cfg_folder,
        type='ScheduleConfig',
        id='test_scheduleconfig',
        title='Test ScheduleConfig',
    )

    test_taskconfig = api.content.create(
        container=test_scheduleconfig,
        type='TaskConfig',
        id='test_taskconfig',
        title='Test TaskConfig',
    )

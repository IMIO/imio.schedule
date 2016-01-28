# -*- coding: utf-8 -*-

from plone import api

from Products.ATContentTypes.interfaces import IATFolder

from urban.schedule.utils import interface_to_tuple


def schedule_example_install(context):
    """
    Example schedule install script.
    """
    if context.readDataFile('urbanschedule_testing.txt') is None:
        return

    monkey_patch_scheduled_conttentype_vocabulary(context)
    add_schedule_config(context)


def monkey_patch_scheduled_conttentype_vocabulary(context):
    """
    Monkey patch the default vocabulary for the field 'scheduled_contenttype'
    to be able to select 'Folder' content type so we can test methods of this
    field.
    """
    from urban.schedule.content.vocabulary import ScheduledContentTypeVocabulary

    def monkey_allowed_types(self):
        return{'Folder': IATFolder}
    ScheduledContentTypeVocabulary.content_types = monkey_allowed_types


def add_schedule_config(context):
    """
    Add dummy ScheduleConfig, TaskConfig.
    """
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
        scheduled_contenttype=('Folder', interface_to_tuple(IATFolder)),
    )

    api.content.create(
        container=test_scheduleconfig,
        type='TaskConfig',
        id='test_taskconfig',
        title='Test TaskConfig',
    )

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
    add_empty_task_container(context)
    add_schedule_config(context)
    add_task(context)


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


def add_empty_task_container(context):
    """
    Add dummy empty task container (ATFolder)
    """
    site = api.portal.get()

    api.content.create(
        container=site,
        type='Folder',
        id='test_empty_taskcontainer',
        title='Empty Task container'
    )


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

    schedule_config = api.content.create(
        container=cfg_folder,
        type='ScheduleConfig',
        id='test_scheduleconfig',
        title='Test ScheduleConfig',
        scheduled_contenttype=('Folder', interface_to_tuple(IATFolder)),
    )

    api.content.create(
        container=schedule_config,
        type='TaskConfig',
        id='test_taskconfig',
        title='Test TaskConfig',
        default_assigned_user='urban.schedule.assign_current_user',
        start_conditions=('urban.schedule.test_start_condition',),
        end_conditions=('urban.schedule.test_end_condition',),
        starting_state='private',
        ending_states=('pending',),
        due_date_computation='urban.schedule.due_date.creation_date',
        additional_delay=10,
    )


def add_task(context):
    """
    Add dummy task container (ATFolder) and create
    a ScheduleTask in it
    """
    site = api.portal.get()

    task_container = api.content.create(
        container=site,
        type='Folder',
        id='test_taskcontainer',
        title='Task container'
    )

    # If no task was created automatically, create the task manually
    # to keep ScheduleTask tests alive
    if not task_container.objectIds():
        portal_types = api.portal.get_tool('portal_types')
        type_info = portal_types.getTypeInfo('ScheduleTask')
        task_config = site.config.test_scheduleconfig.test_taskconfig

        type_info._constructInstance(
            container=task_container,
            id='test_task',
            title=task_config.Title(),
            task_config_UID=task_config.UID()
        )

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

    folder_id = 'test_empty_taskcontainer'
    if folder_id not in site.objectIds():
        api.content.create(
            container=site,
            type='Folder',
            id=folder_id,
            title='Empty Task container'
        )


def add_schedule_config(context):
    """
    Add dummy ScheduleConfig, TaskConfig.
    """
    site = api.portal.get()

    # create config folder for schedule config
    folder_id = 'config'
    if folder_id not in site.objectIds():
        api.content.create(
            container=site,
            type='Folder',
            id=folder_id,
            title='Task configs'
        )
    cfg_folder = getattr(site, folder_id)

    # create schedule config
    schedule_cfg_id = 'test_scheduleconfig'
    if schedule_cfg_id not in cfg_folder.objectIds():
        api.content.create(
            container=cfg_folder,
            type='ScheduleConfig',
            id=schedule_cfg_id,
            title='Test ScheduleConfig',
            scheduled_contenttype=('Folder', interface_to_tuple(IATFolder)),
        )
    schedule_config = getattr(cfg_folder, schedule_cfg_id)

    # create task config
    task_cfg_id = 'test_taskconfig'
    if task_cfg_id not in schedule_config.objectIds():
        api.content.create(
            container=schedule_config,
            type='TaskConfig',
            id=task_cfg_id,
            title='Test TaskConfig',
            default_assigned_user='schedule.assign_current_user',
            creation_conditions=('schedule.test_creation_condition',),
            start_conditions=('schedule.test_start_condition',),
            end_conditions=('schedule.test_end_condition',),
            creation_state='private',
            starting_states=('pending',),
            ending_states=('published',),
            start_date='schedule.start_date.creation_date',
            additional_delay=10,
        )

    # create macro task config
    macrotask_cfg_id = 'test_macrotaskconfig'
    if macrotask_cfg_id not in schedule_config.objectIds():
        api.content.create(
            container=schedule_config,
            type='MacroTaskConfig',
            id=macrotask_cfg_id,
            title='Test MacroTaskConfig',
            default_assigned_user='schedule.assign_current_user',
            creation_conditions=('schedule.test_creation_condition',),
            start_conditions=('schedule.test_start_condition',),
            end_conditions=('schedule.test_end_condition',),
            creation_state='private',
            starting_states=('pending',),
            ending_states=('published',),
            start_date='schedule.start_date.creation_date',
            additional_delay=17,
        )
    macrotask_config = getattr(schedule_config, macrotask_cfg_id)

    # create sub task config
    subtask_cfg_id = 'test_subtaskconfig'
    if subtask_cfg_id not in macrotask_config.objectIds():
        api.content.create(
            container=macrotask_config,
            type='TaskConfig',
            id=subtask_cfg_id,
            title='Test SubTaskConfig',
            default_assigned_user='schedule.assign_current_user',
            creation_conditions=('schedule.test_creation_condition',),
            start_conditions=('schedule.test_start_condition',),
            end_conditions=('schedule.test_end_condition',),
            creation_state='private',
            starting_states=('pending',),
            ending_states=('published',),
            start_date='schedule.start_date.creation_date',
            additional_delay=13,
        )


def add_task(context):
    """
    Add dummy task container (ATFolder) and create
    a ScheduleTask in it
    """
    site = api.portal.get()

    task_container_id = 'test_taskcontainer'
    if task_container_id not in site.objectIds():
        api.content.create(
            container=site,
            type='Folder',
            id=task_container_id,
            title='Task container'
        )
    task_container = getattr(site, task_container_id)

    # If no task was created automatically, create the task manually
    # to keep ScheduleTask tests alive
    task_id = 'TASK_test_taskconfig'
    if task_id not in task_container.objectIds():
        portal_types = api.portal.get_tool('portal_types')
        type_info = portal_types.getTypeInfo('ScheduleTask')
        schedule_config = site.config.test_scheduleconfig
        task_config = schedule_config.test_taskconfig

        type_info._constructInstance(
            container=task_container,
            id=task_id,
            title=task_config.Title(),
            schedule_config_UID=schedule_config.UID(),
            task_config_UID=task_config.UID()
        )

    # If no task was created automatically, create the task manually
    # to keep ScheduleMacroTask tests alive
    macrotask_id = 'TASK_test_macrotaskconfig'
    if macrotask_id not in task_container.objectIds():
        portal_types = api.portal.get_tool('portal_types')
        type_info = portal_types.getTypeInfo('ScheduleMacroTask')
        schedule_config = site.config.test_scheduleconfig
        task_config = schedule_config.test_macrotaskconfig

        type_info._constructInstance(
            container=task_container,
            id=macrotask_id,
            title=task_config.Title(),
            schedule_config_UID=schedule_config.UID(),
            task_config_UID=task_config.UID()
        )

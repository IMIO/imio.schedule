# -*- coding: utf-8 -*-

from plone.indexer import indexer

from urban.schedule.content.task import IScheduleTask


@indexer(IScheduleTask)
def schedule_config_UID(task):
    """
    Return the ScheduleConfig UID of this task.
    """
    return task.schedule_config_UID


@indexer(IScheduleTask)
def task_config_UID(task):
    """
    Return the TaskConfig UID of this task.
    """
    return task.task_config_UID

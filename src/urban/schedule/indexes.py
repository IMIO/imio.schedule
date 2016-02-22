# -*- coding: utf-8 -*-

from plone.indexer import indexer

from urban.schedule.content.task import IAutomatedTask


@indexer(IAutomatedTask)
def schedule_config_UID(task):
    """
    Return the ScheduleConfig UID of this task.
    """
    return task.schedule_config_UID


@indexer(IAutomatedTask)
def task_config_UID(task):
    """
    Return the TaskConfig UID of this task.
    """
    return task.task_config_UID

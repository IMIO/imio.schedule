# -*- coding: utf-8 -*-

from plone.indexer import indexer

from urban.schedule.content.task import IScheduleTask


@indexer(IScheduleTask)
def task_config_UID(task):
    """
    Return the TaskConfig UID of this task.
    """
    return task.get_task_config().UID()

# -*- coding: utf-8 -*-

from Acquisition import aq_base

from urban.schedule.utils import get_task_configs


def create_new_tasks(task_container, event):
    """
    For each task config associated to this task container content type
    check the task config creations conditions and create the task if
    we can.
    """

    # This handler can be triggered for archetypes containers by the
    # workflow modification event but we want to create tasks only if
    # the container really exists (more than just created in portal_factory...)
    if hasattr(aq_base(task_container), 'checkCreationFlag'):
        if task_container.checkCreationFlag():
            return

    task_configs = get_task_configs(task_container)

    if not task_configs:
        return

    for config in task_configs:
        if config.is_main_taskconfig():
            if config.should_create_task(task_container):
                config.create_task(task_container)

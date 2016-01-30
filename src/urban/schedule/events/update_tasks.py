# -*- coding: utf-8 -*-

from urban.schedule.utils import get_task_configs


def end_tasks(task_container, event):
    """
    Automatically end tasks matching end conditions of a given
    task container.
    """

    task_configs = get_task_configs(task_container)

    if not task_configs:
        return

    for config in task_configs:
        task = config.get_open_task(task_container)

        if task and config.should_end_task(task_container, task):
            # delegate the closure action to the config so different behaviors
            # can be easily configured
            config.end_task(task)

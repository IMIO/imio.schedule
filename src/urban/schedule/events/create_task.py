# -*- coding: utf-8 -*-

from Acquisition import aq_base

from plone import api

from urban.schedule.utils import get_task_configs


def create_new_tasks(task_container, event):
    """
    For each task config associated to this task container content type
    check the task config start conditions:
        - if the task has to start, check if the task already exists
        - if the task doesnt exist, create the task
    """

    # This handler can be triggered for archetypes containers by the
    # workflow modification event but we do not want to create tasks
    # as long the container doesnt really exists...
    if hasattr(aq_base(task_container), 'checkCreationFlag'):
        if task_container.checkCreationFlag():
            return

    task_configs = get_task_configs(task_container)

    if not task_configs:
        return

    for config in task_configs:
        if config.should_start_task(task_container):

            task_id = 'TASK-{}'.format(config.id)

            if not hasattr(task_container, task_id):
                task_portal_type = config.get_task_type()
                portal_types = api.portal.get_tool('portal_types')
                type_info = portal_types.getTypeInfo(task_portal_type)

                type_info._constructInstance(
                    container=task_container,
                    id=task_id,
                    title=config.Title(),
                    task_config_UID=config.UID(),
                    assigned_user=config.user_to_assign(task_container),
                    due_date=config.compute_due_date(task_container)
                )

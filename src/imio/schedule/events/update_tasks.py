# -*- coding: utf-8 -*-

from Acquisition import aq_base

from plone import api

from imio.schedule.interfaces import TaskAlreadyExists
from imio.schedule.utils import get_task_configs


class TaskEventHandler(object):

    def __init__(self, task_container, event):
        self.container = task_container
        self.event = event

        if self.is_created is False:
            return

        self.task_configs = get_task_configs(self.container)
        if not self.task_configs:
            return

        with api.env.adopt_roles(['Manager']):
            self.handle()

    @property
    def is_created(self):
        """
        This event can be triggered for archetype containers after a workflow
        modification so we need to ensured that the container really exists
        (more than just created in portal_factory).
        """
        if hasattr(aq_base(self.container), 'checkCreationFlag'):
            if self.container.checkCreationFlag():
                return False
        return True

    def handle(self):
        """
        """
        raise NotImplementedError


def start_tasks(task_container, event):
    """
    Automatically start tasks matching start conditions of a given
    task container.
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

    with api.env.adopt_roles(['Manager']):
        for config in task_configs:
            task = config.get_created_task(task_container)
            if task and config.should_start_task(task_container, task):
                # delegate the starting action to the config so different behaviors
                # can be easily configured
                config.start_task(task)


def end_tasks(task_container, event):
    """
    Automatically end tasks matching end conditions of a given
    task container.
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

    with api.env.adopt_roles(['Manager']):
        for config in task_configs:
            task = config.get_task(task_container)
            if task and config.should_end_task(task_container, task):
                # delegate the closure action to the config so different behaviors
                # can be easily configured
                config.end_task(task)


def update_due_date(task_container, event):
    """
    If the task_container has been modified, compute
    the due date again and update it on the task.
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

    with api.env.adopt_roles(['Manager']):
        for config in task_configs:
            task = config.get_open_task(task_container)
            if task:
                task.due_date = config.compute_due_date(task_container, task)
                task.reindexObject(idxs=('due_date',))


class UpdateRecurrenceHandler(TaskEventHandler):

    def handle(self):
        for config in self.task_configs:
            if config.is_main_taskconfig():
                task = config.get_open_task(self.container)
                if not task and config.should_recurred(self.container):
                    try:
                        config.create_recurring_task(self.container)
                    except TaskAlreadyExists:
                        continue
            # case of a sub-task creation, the parent should have been created first
            else:
                macro_config = config.getParentNode()
                parent_task = macro_config.get_open_task(self.container)
                if parent_task and config.should_recurred(self.container):
                    if config.get_open_task(parent_task) is not None:
                        continue
                    config.create_recurring_task(
                        self.container,
                        creation_place=parent_task,
                    )

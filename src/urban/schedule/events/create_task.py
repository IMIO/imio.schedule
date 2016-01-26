# -*- coding: utf-8 -*-


def create_new_tasks(task_container, event):
    """
    For each task config associated to this task container content type
    check the task config start conditions:
        - if the task has to start, check if the task already exists
        - if the task doesnt exist, create the task
    """


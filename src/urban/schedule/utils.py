# -*- coding: utf-8 -*-

from urban.schedule.interfaces import IToTaskConfig

from zope.component import getAdapters

import importlib


def get_task_configs(task_container):
    """
    Return all the task configs to check for the given context
    providing ITaskContainer.
    """
    config_adapters = getAdapters((task_container,), IToTaskConfig)
    task_configs = [adapter.task_config for name, adapter in config_adapters]

    return task_configs


def tuple_to_interface(interface_tuple):
    """
    Turn a tuple of strings:
    ('interface.module.path', 'Interface')
    into an Interface class.
    """
    module_path, interface_name = interface_tuple
    interface_module = importlib.import_module(module_path)
    interface_class = getattr(interface_module, interface_name)

    return interface_class


def interface_to_tuple(interface):
    """
    Turn an Interface class into a tuple:
    ('interface.module.path', 'Interface')
    """
    return (interface.__module__, interface.__name__)

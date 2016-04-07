# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.interfaces import IToTaskConfig

from zope.component import getAdapters

import importlib


def get_all_schedule_configs():
    """
    Return all the ScheduleConfig of the site.
    """
    # nested import to avoid recursive imports
    from urban.schedule.content.schedule_config import IScheduleConfig

    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(object_provides=IScheduleConfig.__identifier__)
    configs = [brain.getObject() for brain in brains]

    return configs


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


def create_tasks_collection(schedule_config, container, id, **kwargs):
    """
    Create a DashboardCollection in container with a base
    query returning all the AutomatedTask instances from
    schedule_config.
    """

    factory_args = {
        'id': id,
        'query': [
            {
                'i': 'CompoundCriterion',
                'o': 'plone.app.querystring.operation.compound.is',
                'v': schedule_config.UID()
            }
        ],
        'customViewFields': ('due_date', 'Creator'),
        'sort_on': u'due_date',
        'sort_reversed': True,
        'b_size': 30
    }

    additional_queries = kwargs.pop('query', [])
    for query in additional_queries:
        factory_args['query'].append(query)
    factory_args.update(kwargs)

    collection_id = container.invokeFactory('DashboardCollection', **factory_args)
    collection = getattr(container, collection_id)

    return collection

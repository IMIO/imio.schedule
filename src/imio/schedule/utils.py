# -*- coding: utf-8 -*-

from eea.facetednavigation.layout.interfaces import IFacetedLayout

from imio.dashboard.browser.facetedcollectionportlet import Assignment
from imio.dashboard.utils import _updateDefaultCollectionFor

from imio.schedule.config import CREATION
from imio.schedule.config import STARTED
from imio.schedule.config import states_by_status
from imio.schedule.content.task import IAutomatedTask
from imio.schedule.interfaces import IToTaskConfig

from plone import api
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.constants import CONTEXT_CATEGORY

from zope.annotation import IAnnotations
from zope.component import getAdapters
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary

import datetime
import importlib


def get_all_schedule_configs():
    """
    Return all the ScheduleConfig of the site.
    """
    # nested import to avoid recursive imports
    from imio.schedule.content.schedule_config import IScheduleConfig

    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(object_provides=IScheduleConfig.__identifier__)
    configs = [brain.getObject() for brain in brains]

    return configs


def get_task_configs(task_container, descending=False):
    """
    Return all the task configs to check for the given context
    providing ITaskContainer.
    """
    config_adapters = getAdapters((task_container,), IToTaskConfig)
    task_configs = [adapter.task_config for name, adapter in config_adapters]
    ordering = descending and 1 or -1
    task_configs = sorted(task_configs, key=lambda cfg: ordering * cfg.level())

    return task_configs


def query_container_open_tasks(task_container, the_objects=False):
    """
    Return all the open tasks of a container.
    """
    states = states_by_status[CREATION] + states_by_status[STARTED]
    tasks = query_container_tasks(
        task_container,
        the_objects,
        query={'review_state': states},
    )
    return tasks


def query_container_tasks(task_container, the_objects=False, query={}):
    """
    Return all the tasks of a container.
    """
    catalog = api.portal.get_tool('portal_catalog')

    full_query = {
        'object_provides': IAutomatedTask.__identifier__,
        'path': {'query': '/'.join(task_container.getPhysicalPath())},
    }
    full_query.update(query)

    task_brains = catalog.unrestrictedSearchResults(**full_query)

    if the_objects:
        return [brain.getObject() for brain in task_brains]

    return task_brains


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
    Turn an Interface class into a tuple of strings:
    ('interface.module.path', 'Interface')
    """
    return (interface.__module__, interface.__name__)


def set_schedule_view(folder, faceted_config_path, schedule_configs, default_collection=None):
    """
    Boilerplate code to set up the schedule view on a folderish context.
    """

    if type(schedule_configs) not in [list, tuple]:
        schedule_configs = [schedule_configs]

    _set_faceted_view(folder, faceted_config_path, schedule_configs, default_collection)
    _set_collection_portlet(folder)


def _set_faceted_view(folder, faceted_config_path, schedule_configs, default_collection=None):
    """
    """
    annotations = IAnnotations(folder)
    key = 'imio.schedule.schedule_configs'
    annotations[key] = [cfg.UID() for cfg in schedule_configs]

    subtyper = folder.restrictedTraverse('@@faceted_subtyper')
    if not subtyper.is_faceted:
        subtyper.enable()
        folder.restrictedTraverse('@@faceted_settings').toggle_left_column()
        IFacetedLayout(folder).update_layout('faceted-table-items')
        folder.unrestrictedTraverse('@@faceted_exportimport').import_xml(
            import_file=open(faceted_config_path)
        )

    default_collection = default_collection or schedule_configs[0].dashboard_collection
    _updateDefaultCollectionFor(folder, default_collection.UID())


def _set_collection_portlet(folder):
    """
    """
    # block parent portlets
    manager = getUtility(IPortletManager, name='plone.leftcolumn')
    blacklist = getMultiAdapter((folder, manager), ILocalPortletAssignmentManager)
    blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # assign collection portlet
    manager = getUtility(IPortletManager, name='plone.leftcolumn', context=folder)
    mapping = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    if 'schedules' not in mapping.keys():
        mapping['schedules'] = Assignment('schedules')


def dict_list_2_vocabulary(dict_list):
    """dict_list_2_vocabulary
    Converts a dictionary list to a SimpleVocabulary

    :param dict_list: dictionary list
    """
    terms = []
    for item in dict_list:
        for key in sorted([k for k in item]):
            terms.append(SimpleVocabulary.createTerm(
                key, str(key), item[key]))
    return SimpleVocabulary(terms)


def round_to_weekday(date, weekday):
    direction = weekday / abs(weekday)  # -1 => past, +1 => future
    weekday = abs(weekday) - 1
    days_delta = weekday - date.weekday()
    if days_delta * direction < 0:
        days_delta += 7 * direction
    return date + datetime.timedelta(days_delta)

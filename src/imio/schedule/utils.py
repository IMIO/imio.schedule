# -*- coding: utf-8 -*-

from eea.facetednavigation.layout.interfaces import IFacetedLayout

from imio.dashboard.browser.facetedcollectionportlet import Assignment
from imio.dashboard.utils import _updateDefaultCollectionFor

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


def get_task_configs(task_container, ascending=False):
    """
    Return all the task configs to check for the given context
    providing ITaskContainer.
    """
    config_adapters = getAdapters((task_container,), IToTaskConfig)
    task_configs = [adapter.task_config for name, adapter in config_adapters]
    ordering = ascending and 1 or -1
    task_configs = sorted(task_configs, key=lambda cfg: ordering * cfg.level())

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


def set_schedule_view(folder, faceted_config_path, schedule_configs, default_collection=None):
    """
    Boilerplate code to set up the schedule view on a folderish context.
    """

    if type(schedule_configs) not in [list, tuple]:
        schedule_configs = [schedule_configs]

    annotations = IAnnotations(folder)
    key = 'imio.schedule.schedule_configs'
    annotations[key] = [cfg.UID() for cfg in schedule_configs]

    # block parent portlets
    manager = getUtility(IPortletManager, name='plone.leftcolumn')
    blacklist = getMultiAdapter((folder, manager), ILocalPortletAssignmentManager)
    blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

    # assign collection portlet
    manager = getUtility(IPortletManager, name='plone.leftcolumn', context=folder)
    mapping = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    if 'schedules' not in mapping.keys():
        mapping['schedules'] = Assignment('schedules')

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

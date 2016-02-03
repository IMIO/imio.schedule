# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.content.task_config import ITaskConfig
from urban.schedule.interfaces import IToTaskConfig
from urban.schedule.interfaces import TaskConfigNotFound
from urban.schedule.utils import interface_to_tuple
from urban.schedule.utils import tuple_to_interface

from zope.component import getGlobalSiteManager
from zope.interface import implements

import logging

logger = logging.getLogger('schedule')


def subscribe_task_configs_for_content_type(task_config, event):
    """
    Register adapter returning 'task_config' to the interface
    of the content_type selected in the field 'task_container'.
    """

    gsm = getGlobalSiteManager()

    class TaskConfigSubscriber(object):
        """ """
        implements(IToTaskConfig)

        def __init__(self, context):
            """ """
            self.context = context
            self.task_config_UID = task_config.UID()

        @property
        def task_config(self):
            catalog = api.portal.get_tool('portal_catalog')
            brains = catalog(UID=self.task_config_UID)
            if brains:
                task_config = brains[0].getObject()
                return task_config
            else:
                raise TaskConfigNotFound

    registration_interface = task_config.get_scheduled_interface()

    gsm.registerAdapter(
        factory=TaskConfigSubscriber,
        required=(registration_interface,),
        provided=IToTaskConfig,
        name=task_config.UID()
    )
    msg = "Registered IToTaskConfig adapter '{}' for {}".format(
        task_config.Title(),
        registration_interface
    )
    logger.info(msg)


def unsubscribe_task_configs_for_content_type(task_config, event):
    """
    Unregister adapter returning 'task_config' to the interface
    of the content_type selected in the field 'task_container'.
    """

    gsm = getGlobalSiteManager()
    schedule_config = task_config.get_schedule_config()

    previous_interface = getattr(schedule_config, '_scheduled_interface_', None)
    previous_interface = tuple_to_interface(previous_interface)

    removed = gsm.unregisterAdapter(
        required=(previous_interface,),
        provided=IToTaskConfig,
        name=task_config.UID()
    )
    if removed:
        msg = "Unregistered IToTaskConfig adapter '{}' for {}".format(
            task_config.Title(),
            previous_interface
        )
        logger.info(msg)


def update_task_configs_subscriptions(schedule_config, event):
    """
    When the scheduled_contenttype value of a ScheduleConfig is changed,
    we have to unregister all the adapters providing IToTaskConfig
    and register them again for the new selected content type.
    """

    previous_interface = getattr(schedule_config, '_scheduled_interface_', None)
    new_interface = schedule_config.get_scheduled_interface()
    new_interface = interface_to_tuple(new_interface)

    # if there were no previous values, just save it and return
    if not previous_interface:
        setattr(schedule_config, '_scheduled_interface_', new_interface)
        return

    # if the walue did not change, do nothing
    if previous_interface == new_interface:
        return

    for task_config in schedule_config.get_all_task_configs():
        # unregister the IToTaskConfig adapter for the previous interface
        unsubscribe_task_configs_for_content_type(task_config, event)
        # register the new IToTaskConfig adapter for the new interface
        subscribe_task_configs_for_content_type(task_config, event)

    # replace the _schedule_interface_ attribute with the new value
    setattr(schedule_config, '_scheduled_interface_', new_interface)


_registered_sites = set()


def subscribe_task_configs_at_instance_startup(site, event):
    """
    Re-subscribe all the TaskConfig adapters when zope instance
    is started.
    """
    if site not in _registered_sites:

        catalog = api.portal.get_tool('portal_catalog')
        task_brains = catalog.unrestrictedSearchResults(object_provides=ITaskConfig.__identifier__)
        all_task_configs = [site.unrestrictedTraverse(brain.getPath()) for brain in task_brains]

        for task_config in all_task_configs:
            subscribe_task_configs_for_content_type(task_config, event)

        _registered_sites.add(site)

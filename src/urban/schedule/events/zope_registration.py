# -*- coding: utf-8 -*-

from collective.compoundcriterion.interfaces import ICompoundCriterionFilter

from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer

from urban.schedule.content.schedule_config import IScheduleConfig
from urban.schedule.content.task_config import ITaskConfig
from urban.schedule.interfaces import IToTaskConfig
from urban.schedule.interfaces import TaskConfigNotFound
from urban.schedule.utils import interface_to_tuple
from urban.schedule.utils import tuple_to_interface

from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


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
                raise TaskConfigNotFound(
                    'UID {}'.format(self.task_config_UID)
                )

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


def register_schedule_collection_criterion(schedule_config, event):
    """
    Register adapter turning a schedule config into a collection
    criterion filtering all task from this schedule config.
    """

    gsm = getGlobalSiteManager()
    schedule_config_UID = schedule_config.UID()

    class FilterTasksCriterion(object):

        def __init__(self, context):
            self.context = context

        @property
        def query(self):
            return {'schedule_config_UID': {'query': schedule_config_UID}}

    gsm.registerAdapter(
        factory=FilterTasksCriterion,
        required=(Interface,),
        provided=ICompoundCriterionFilter,
        name=schedule_config.UID()
    )
    msg = "Registered CollectionCriterion adapter '{}'".format(
        schedule_config.Title()
    )
    logger.info(msg)


def unregister_schedule_collection_criterion(schedule_config, event):
    """
    Unregister adapter turning a schedule config into a collection
    criterion.
    """

    gsm = getGlobalSiteManager()

    removed = gsm.unregisterAdapter(
        required=(Interface,),
        provided=ICompoundCriterionFilter,
        name=schedule_config.UID()
    )
    if removed:
        msg = "Unregistered CollectionCriterion adapter '{}'".format(
            schedule_config.Title()
        )
        logger.info(msg)


_vocabularies = {}


def register_tasks_vocabulary(schedule_config, event):
    """
    Register adapter turning a schedule config into a collection
    criterion filtering all task from this schedule config.
    """

    gsm = getGlobalSiteManager()
    normalizer = getUtility(IIDNormalizer)

    class TaskConfigsVocabulary(object):

        implements(IVocabularyFactory)

        schedule_config_UID = schedule_config.UID()
        name = normalizer.normalize(schedule_config.Title())

        def __call__(self, context):
            catalog = api.portal.get_tool('portal_catalog')
            schedule_config = catalog(UID=self.schedule_config_UID)[0].getObject()
            collection_brains = schedule_config.query_task_configs()
            vocabulary = SimpleVocabulary(
                [SimpleTerm(b.UID, b.UID, b.Title) for b in collection_brains]
            )
            return vocabulary

    voc_factory = TaskConfigsVocabulary()
    gsm.registerUtility(voc_factory, name=voc_factory.name)
    _vocabularies[schedule_config.UID()] = voc_factory

    msg = "Registered schedule tasks vocabulary '{}'".format(
        voc_factory.name
    )
    logger.info(msg)


def unregister_tasks_vocabulary(schedule_config, event):
    """
    Unregister adapter turning a schedule config into a collection
    criterion.
    """

    gsm = getGlobalSiteManager()

    voc_factory = _vocabularies[schedule_config.UID()]
    removed = gsm.unregisterUtility(voc_factory, name=voc_factory.name)

    if removed:
        _vocabularies.pop(schedule_config.UID())
        msg = "Unregistered schedule tasks vocabulary '{}'".format(
            voc_factory.name
        )
        logger.info(msg)


_registered_sites = set()


def register_at_instance_startup(site, event):
    """
    Re-register:
        - all the TaskConfig adapters
        - collections criterions
        - tasks vocabulary of each ScheduleConfig
    when zope instanceis started.
    """
    if site not in _registered_sites:

        # register task configs subscribers
        catalog = api.portal.get_tool('portal_catalog')
        task_brains = catalog.unrestrictedSearchResults(object_provides=ITaskConfig.__identifier__)
        all_task_configs = [site.unrestrictedTraverse(brain.getPath()) for brain in task_brains]

        for task_config in all_task_configs:
            subscribe_task_configs_for_content_type(task_config, event)

        # register schedule configs criterion and tasks vocabulary
        schedule_brains = catalog.unrestrictedSearchResults(object_provides=IScheduleConfig.__identifier__)
        all_schedule_configs = [site.unrestrictedTraverse(brain.getPath()) for brain in schedule_brains]

        for schedule_config in all_schedule_configs:
            register_schedule_collection_criterion(schedule_config, event)
            register_tasks_vocabulary(schedule_config, event)

        _registered_sites.add(site)

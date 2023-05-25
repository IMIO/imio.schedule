# -*- coding: utf-8 -*-

from plone import api
from zope.interface import alsoProvides


def upgrade_2_fix_schedule_collection(context):
    from collective.eeafaceted.collectionwidget.interfaces import IDashboardCollection
    from imio.schedule.interfaces import IScheduleCollection

    brains = api.content.find(
        object_provides=IDashboardCollection.__identifier__,
        id="dashboard_collection",
    )
    for brain in brains:
        if "schedule" not in brain.getPath():
            continue
        collection = brain.getObject()
        alsoProvides(collection, IScheduleCollection)


def upgrade_3_set_showNumberOfItems(context):
    from collective.eeafaceted.collectionwidget.interfaces import IDashboardCollection
    brains = api.content.find(
        object_provides=IDashboardCollection.__identifier__,
        id="dashboard_collection",
    )
    for brain in brains:
        if "schedule" not in brain.getPath():
            continue
        collection = brain.getObject()
        collection.showNumberOfItems = True

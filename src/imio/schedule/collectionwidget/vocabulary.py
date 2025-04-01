# -*- coding: utf-8 -*-

from collective.eeafaceted.collectionwidget.vocabulary import CollectionVocabulary
from imio.schedule.utils import MultiLevelOrdering

from plone import api

from zope.annotation import IAnnotations


class ScheduleCollectionVocabulary(CollectionVocabulary):
    """
    Return vocabulary of base searchs for schedule faceted view.
    """

    def _brains(self, context):
        """
        Return all the DashboardCollections in the 'schedule' folder.
        """
        configs_UID = IAnnotations(context).get("imio.schedule.schedule_configs", [])
        catalog = api.portal.get_tool("portal_catalog")
        config_brains = catalog(UID=configs_UID)
        collections_brains = []
        for brain in config_brains:
            config = brain.getObject()
            config_collection_brains = catalog(
                path={
                    "query": "/".join(config.getPhysicalPath()),
                },
                object_provides="plone.app.contenttypes.interfaces.ICollection",
            )

            # sort the collections in the same way as in schedule config
            mlo = MultiLevelOrdering(config)
            config_collection_brains = sorted(
                config_collection_brains,
                key=lambda brain: mlo.get_order(brain.getPath().split("/")),
            )

            collections_brains.extend(config_collection_brains)
        collections_brains = [
            b for b in collections_brains if b.getObject().aq_parent.enabled
        ]
        return collections_brains


ScheduleCollectionVocabularyFactory = ScheduleCollectionVocabulary()

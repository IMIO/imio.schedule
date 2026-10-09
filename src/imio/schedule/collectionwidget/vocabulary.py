# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.eeafaceted.collectionwidget.vocabulary import CollectionVocabulary

from plone import api

from zope.annotation import IAnnotations


class ScheduleCollectionVocabulary(CollectionVocabulary):
    """
    Return vocabulary of base searchs for schedule faceted view.
    """

    @staticmethod
    def _position_key(collection, config):
        """
        Build a sort key from the positions of the containers between
        the schedule config and the collection (the collection itself excluded).
        The config collection ('Tous') gets an empty key and comes first,
        subtasks come right after their parent task.
        """
        config_path = config.getPhysicalPath()
        key = []
        current = aq_parent(aq_inner(collection))
        while current.getPhysicalPath() != config_path:
            parent = aq_parent(aq_inner(current))
            key.insert(0, parent.getObjectPosition(current.getId()))
            current = parent
        return tuple(key)

    def _brains(self, context):
        """
        Return all the DashboardCollections in the 'schedule' folder,
        ordered like the task configs in their folder.
        """
        configs_UID = IAnnotations(context).get("imio.schedule.schedule_configs", [])
        catalog = api.portal.get_tool("portal_catalog")
        # keep the order of the annotation (catalog(UID=[...]) does not)
        config_brains = sorted(
            catalog(UID=configs_UID),
            key=lambda b: configs_UID.index(b.UID),
        )
        collections_brains = []
        for config_brain in config_brains:
            config = config_brain.getObject()
            brains = catalog(
                path={"query": "/".join(config.getPhysicalPath())},
                object_provides="plone.app.contenttypes.interfaces.ICollection",
            )
            keyed = []
            for brain in brains:
                collection = brain.getObject()
                if not aq_parent(collection).enabled:
                    continue
                keyed.append((self._position_key(collection, config), brain))
            keyed.sort(key=lambda item: item[0])
            collections_brains.extend([brain for key, brain in keyed])
        return collections_brains


ScheduleCollectionVocabularyFactory = ScheduleCollectionVocabulary()

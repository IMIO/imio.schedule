# encoding: utf-8

from plone import api

from urban.schedule.content.task_config import ITaskConfig

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class MacroTasksVocabulary(object):
    """
    Vocabulary factory listing macros tasks to display in schedule.
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        collection_brains = catalog(object_provides=ITaskConfig.__identifier__)
        vocabulary = SimpleVocabulary(
            [SimpleTerm(b.UID, b.UID, b.Title) for b in collection_brains]
        )
        return vocabulary

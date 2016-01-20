# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.testing import ExampleScheduleIntegrationTestCase

from zope.component import queryAdapter
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


class TestVocabularies(ExampleScheduleIntegrationTestCase):
    """
    Test field vocabularies registration and values.
    """

    def _get_fti(self, portal_type):
        """
        Helper method to return the fti of a content type.
        """
        portal_types = api.portal.get_tool('portal_types')
        fti = portal_types.getTypeInfo(portal_type)
        return fti

    def test_content_types_vocabulary_factory_registration(self):
        """
        Content types voc factory should be registered as a named utility.
        """
        factory_name = 'urban.schedule.content_types'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_content_types_default_vocabulary_registration(self):
        """
        Voc values should be registered as a named adapter on the task
        config fti and name should be the fti portal_type.
        """
        from urban.schedule.interfaces import IContentTypesVocabulary

        portal_type = self.taskconfig_1.portal_type

        voc_adapter = queryAdapter(
            self._get_fti(portal_type),
            IContentTypesVocabulary,
            portal_type
        )
        self.assertTrue(voc_adapter)

    def test_content_types_vocabulary_values(self):
        """
        Test some content_types values.
        """

        voc_name = 'urban.schedule.content_types'
        voc_factory = queryUtility(IVocabularyFactory, voc_name)
        vocabulary = voc_factory(self.taskconfig_1)
        self.assertTrue('--NOVALUE--' in vocabulary)

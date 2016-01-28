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
        factory_name = 'urban.schedule.scheduled_contenttype'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_content_types_default_vocabulary_registration(self):
        """
        Voc values should be registered as a named adapter on the task
        config fti and name should be the fti portal_type.
        """
        from urban.schedule.interfaces import IScheduledContentTypeVocabulary

        portal_type = self.test_scheduleconfig.portal_type

        voc_adapter = queryAdapter(
            self._get_fti(portal_type),
            IScheduledContentTypeVocabulary,
            portal_type
        )
        self.assertTrue(voc_adapter)

    def test_content_types_vocabulary_values(self):
        """
        Test some content_types values.
        """

        voc_name = 'urban.schedule.scheduled_contenttype'
        voc_factory = queryUtility(IVocabularyFactory, voc_name)
        vocabulary = voc_factory(self.test_scheduleconfig)
        expected_key = "('Folder', ('Products.ATContentTypes.interfaces.folder', 'IATFolder'))"
        msg = 'expected key:\n{expected}\nwas not found in voc_keys:\n{voc}'.format(
            expected=expected_key,
            voc=vocabulary.by_token.keys()
        )
        self.assertTrue(expected_key in vocabulary.by_token.keys(), msg)

    def test_start_conditions_vocabulary_factory_registration(self):
        """
        Content types voc factory should be registered as a named utility.
        """
        factory_name = 'urban.schedule.start_conditions'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_start_conditions_vocabulary_values(self):
        """
        Test some start_conditions values.
        """
        voc_name = 'urban.schedule.start_conditions'
        voc_factory = queryUtility(IVocabularyFactory, voc_name)
        vocabulary = voc_factory(self.test_taskconfig)
        self.assertTrue('urban.schedule.test_start_condition' in vocabulary)

    def test_end_conditions_vocabulary_factory_registration(self):
        """
        Content types voc factory should be registered as a named utility.
        """
        factory_name = 'urban.schedule.end_conditions'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_end_conditions_vocabulary_values(self):
        """
        Test some end_conditions values.
        """
        voc_name = 'urban.schedule.end_conditions'
        voc_factory = queryUtility(IVocabularyFactory, voc_name)
        vocabulary = voc_factory(self.test_taskconfig)
        self.assertTrue('urban.schedule.test_end_condition' in vocabulary)

# -*- coding: utf-8 -*-

from urban.schedule.testing import ExampleScheduleIntegrationTestCase

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory


class TestVocabularies(ExampleScheduleIntegrationTestCase):
    """
    Test field vocabularies registration and values.
    """

    def test_content_types_vocabulary_factory_registration(self):
        """
        Content types voc factory should be registered as a named utility.
        """
        factory_name = 'urban.schedule.content_types'
        self.assertTrue(queryUtility(IVocabularyFactory, factory_name))

    def test_content_types_vocabulary_values(self):
        """
        Test some content_types values.
        """

        voc_name = 'urban.schedule.content_types'
        voc_factory = queryUtility(IVocabularyFactory, voc_name)
        vocabulary = voc_factory(self.taskconfig_1)
        self.assertTrue('--NOVALUE--' in vocabulary)

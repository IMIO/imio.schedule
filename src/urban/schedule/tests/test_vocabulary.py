# -*- coding: utf-8 -*-

from urban.schedule.testing import TEST_INSTALL_INTEGRATION

from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestVocabularies(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

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
        # turn Folder content type into a 'taskable' by implementing
        # ITaskContainer on it.

        voc_name = 'urban.schedule.content_types'
        voc_factory = queryUtility(IVocabularyFactory, voc_name)
        vocabulary = voc_factory(self.portal)
        self.assertTrue('--NOVALUE--' in vocabulary)

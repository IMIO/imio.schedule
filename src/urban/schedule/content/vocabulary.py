# -*- coding: utf-8 -*-

from z3c.form.i18n import MessageFactory as _

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ContentTypesVocabularyFactory(object):
    """
    Vocabulary factory for 'content_types' field.
    Return all the content types that can be associated
    to a task config and therefore should implements ITaskContainer

    - The key of a voc term is the class of the content type
      eg:
    - The display value is the translation of the content type

    !!!
    This vocabulary has to be defined in the product using urban.schedule
    and have to be registered for a subclass of TaskConfig
    !!!
    """

    def __call__(self, context):

        voc_terms = [SimpleTerm('--NOVALUE--', '--NOVALUE--', _('No value'))]

        vocabulary = SimpleVocabulary(voc_terms)

        return vocabulary

# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.interfaces import IContentTypesVocabulary
from urban.schedule.interfaces import IEndConditionsVocabulary
from urban.schedule.interfaces import IStartConditionsVocabulary

from z3c.form.i18n import MessageFactory as _

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from zope.component import getAdapter

from zope.interface import implements


class BaseVocabularyFactory(object):
    """
    Base class for vocabulary factories.
    """

    def get_portal_type(self, context):
        """
        Return the portal_type of the (future?) context.
        """
        try:
            add_view = context.REQUEST['PUBLISHED']
            form = hasattr(add_view, 'form_instance') and add_view.form_instance or add_view.context.form_instance
            portal_type = form.portal_type
        except:
            portal_type = context.portal_type

        return portal_type

    def get_fti(self, context):
        """
        Return the fti of the (future?) context.
        """
        portal_type = self.get_portal_type(context)
        portal_types = api.portal.get_tool('portal_types')
        fti = portal_types.getTypeInfo(portal_type)
        return fti


class ContentTypesVocabularyFactory(BaseVocabularyFactory):
    """
    Vocabulary factory for 'content_types' field.
    Return all the content types that can be associated
    to a task config and therefore should implements ITaskContainer
    """

    def __call__(self, context):
        """
        Call the adapter vocabulary for the 'content_types' field
        and returns it.
        """
        portal_type = self.get_portal_type(context)
        fti = self.get_fti(context)
        voc_adapter = getAdapter(fti, IContentTypesVocabulary, portal_type)
        vocabulary = voc_adapter()

        return vocabulary


class TaskConfigContentTypesVocabulary(object):
    """
    !!! To register for more specific TaskConfig subclasses !!!
    !!! The name of this adapter should be the portal_type  !!!
    eg: here it's TaskConfig

    Adapts a TaskConfig fti to return a specific
    vocabulary for the 'content_types' field.
    """

    implements(IContentTypesVocabulary)

    def __init__(self, fti):
        """ """

    def __call__(self):
        """
        - The key of a voc term is the class of the content type
        - The display value is the translation of the content type
        """

        voc_terms = [SimpleTerm('--NOVALUE--', '--NOVALUE--', _('No value'))]
        vocabulary = SimpleVocabulary(voc_terms)

        return vocabulary


class StartConditionVocabularyFactory(BaseVocabularyFactory):
    """
    Vocabulary factory for 'start_conditions' field.
    Return all the start conditions that can be associated
    to a task config.
    """

    def __call__(self, context):
        """
        Call the adapter vocabulary for the 'start_conditions' field
        and returns it.
        """
        portal_type = self.get_portal_type(context)
        fti = self.get_fti(context)
        voc_adapter = getAdapter(fti, IContentTypesVocabulary, portal_type)
        vocabulary = voc_adapter()

        return vocabulary


class TaskConfigStartConditionsVocabulary(object):
    """
    !!! To register for more specific TaskConfig subclasses !!!
    !!! The name of this adapter should be the portal_type  !!!
    eg: here it's TaskConfig

    Adapts a TaskConfig fti to return a specific
    vocabulary for the 'start_conditions' field.
    """

    implements(IStartConditionsVocabulary)

    def __init__(self, fti):
        """ """

    def __call__(self):
        """
        - The key of a voc term is the regsitration name of the condition
          (utility).
        - The display value is the title of the condition.
        """

        voc_terms = [SimpleTerm('--NOVALUE--', '--NOVALUE--', _('No value'))]
        vocabulary = SimpleVocabulary(voc_terms)

        return vocabulary


class EndConditionVocabularyFactory(BaseVocabularyFactory):
    """
    Vocabulary factory for 'end_conditions' field.
    Return all the end conditions that can be associated
    to a task config.
    """

    def __call__(self, context):
        """
        Call the adapter vocabulary for the 'end_conditions' field
        and returns it.
        """
        portal_type = self.get_portal_type(context)
        fti = self.get_fti(context)
        voc_adapter = getAdapter(fti, IContentTypesVocabulary, portal_type)
        vocabulary = voc_adapter()

        return vocabulary


class TaskConfigEndConditionsVocabulary(object):
    """
    !!! To register for more specific TaskConfig subclasses !!!
    !!! The name of this adapter should be the portal_type  !!!
    eg: here it's TaskConfig

    Adapts a TaskConfig fti to return a specific
    vocabulary for the 'end_conditions' field.
    """

    implements(IEndConditionsVocabulary)

    def __init__(self, fti):
        """ """

    def __call__(self):
        """
        - The key of a voc term is the regsitration name of the condition
          (utility).
        - The display value is the title of the condition.
        """

        voc_terms = [SimpleTerm('--NOVALUE--', '--NOVALUE--', _('No value'))]
        vocabulary = SimpleVocabulary(voc_terms)

        return vocabulary

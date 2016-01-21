# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.content.task_config import ITaskConfig
from urban.schedule.interfaces import IEndConditionsVocabulary
from urban.schedule.interfaces import ITaskContainerVocabulary
from urban.schedule.interfaces import IStartConditionsVocabulary

from z3c.form.i18n import MessageFactory as _

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getAdapter
from zope.i18n import translate
from zope.interface import implements


class BaseVocabularyFactory(object):
    """
    Base class for vocabulary factories.
    """

    def get_portal_type(self, context):
        """
        Return the portal_type of the (future?) context.
        """
        request = context.REQUEST
        try:
            add_view = request.get('PUBLISHED', request['PARENTS'][-1])
            if hasattr(add_view, 'form_instance'):
                form = add_view.form_instance
                portal_type = form.portal_type
            else:
                form = add_view.context.form_instance
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


class TaskContainerVocabularyFactory(BaseVocabularyFactory):
    """
    Vocabulary factory for 'task_container' field.
    Return all the content types that can be associated
    to a task config (=> should implements ITaskContainer).
    """

    def __call__(self, context):
        """
        Call the adapter vocabulary for the 'task_container' field
        and returns it.
        """
        portal_type = self.get_portal_type(context)
        fti = self.get_fti(context)
        voc_adapter = getAdapter(fti, ITaskContainerVocabulary, portal_type)
        vocabulary = voc_adapter()

        return vocabulary


class TaskContainerVocabulary(object):
    """
    Adapts a TaskConfig fti to return a specific
    vocabulary for the 'task_container' field.

    Subclass and override __call__ in products using urban.schedule.
    """

    implements(ITaskContainerVocabulary)

    def __init__(self, fti):
        """ """

    def __call__(self):
        """
        """

        voc_terms = [SimpleTerm('--NOVALUE--', '--NOVALUE--', _('No value'))]
        vocabulary = SimpleVocabulary(voc_terms)

        return vocabulary

    def to_vocabulary_key(self, portal_type, interface):
        """
        Return the module path of a class.
        """
        return (portal_type, interface.__module__, interface.__name__)


def get_states_vocabulary(portal_type):
    """
    Return states of the default workflow of the given portal_type as
    a vocabulary.
    """
    if not portal_type:
        return SimpleVocabulary([])

    wf_tool = api.portal.get_tool('portal_workflow')
    request = api.portal.get().REQUEST

    workfow = wf_tool.get(wf_tool.getChainForPortalType(portal_type)[0])
    voc_terms = [
        SimpleTerm(state_id, state_id, translate(state.title, 'plone', context=request))
        for state_id, state in workfow.states.items()
    ]

    vocabulary = SimpleVocabulary(voc_terms)

    return vocabulary


class ContainerStateVocabularyFactory(BaseVocabularyFactory):
    """
    Vocabulary factory for 'container_state' field.
    """

    def __call__(self, context):
        """
        Call the adapter vocabulary for the 'container_state' field
        and returns it.
        """
        # case of TaskConfig creation, we have no TaskConfig object yet
        if not ITaskConfig.providedBy(context):
            voc_terms = [SimpleTerm('--NOVALUE--', '--NOVALUE--', _('No value'))]
            vocabulary = SimpleVocabulary(voc_terms)
            return  vocabulary

        portal_type = context.get_container_portal_type()
        vocabulary = get_states_vocabulary(portal_type)

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
        voc_adapter = getAdapter(fti, IStartConditionsVocabulary, portal_type)
        vocabulary = voc_adapter()

        return vocabulary


class StartConditionsVocabulary(object):
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
        voc_adapter = getAdapter(fti, IEndConditionsVocabulary, portal_type)
        vocabulary = voc_adapter()

        return vocabulary


class EndConditionsVocabulary(object):
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

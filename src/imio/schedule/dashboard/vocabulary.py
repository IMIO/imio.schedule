# -*- coding: utf-8 -*-

from zope.i18n import translate as _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class TaskWorkflowStates(object):
    """
    List all states of urban licence workflow.
    """

    def __call__(self, context):

        states = ['created', 'to_do', 'closed']

        vocabulary_terms = []
        for state in states:
            vocabulary_terms.append(
                SimpleTerm(
                    state,
                    state,
                    _(state, 'collective.task', context.REQUEST)
                )
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary

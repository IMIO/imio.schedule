# -*- coding: utf-8 -*-

from imio.schedule.interfaces import IScheduleCollection

from plone import api

from zope.interface import alsoProvides


def create(schedule_container, event):
    """
    """
    collection_id = 'dashboard_collection'

    if collection_id not in schedule_container.objectIds():
        factory_args = {
            'id': 'dashboard_collection',
            'title': schedule_container.Title(),
            'query': [
                {
                    'i': 'CompoundCriterion',
                    'o': 'plone.app.querystring.operation.compound.is',
                    'v': schedule_container.UID()
                },
                {
                    'i': 'review_state',
                    'o': 'plone.app.querystring.operation.selection.is',
                    'v': ['to_do']
                }
            ],
            'customViewFields': (
                u'assigned_user_column',
                u'status',
                u'due_date'
            ),
            'sort_on': u'due_date',
            'sort_reversed': True,
            'b_size': 30
        }

        kwargs = {}
        additional_queries = kwargs.pop('query', [])
        for query in additional_queries:
            factory_args['query'].append(query)
        factory_args.update(kwargs)

        portal_types = api.portal.get_tool('portal_types')
        type_info = portal_types.getTypeInfo('DashboardCollection')
        collection = type_info._constructInstance(schedule_container, **factory_args)
        # mark the collection with an interface to to customize the render
        # term view of collection widget
        alsoProvides(collection, IScheduleCollection)

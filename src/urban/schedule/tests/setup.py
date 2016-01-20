# -*- coding: utf-8 -*-

from plone import api


def schedule_example_install(context):
    """
    Example schedule install script.
    """
    if context.readDataFile('urbanschedule_testing.txt') is None:
        return

    site = api.portal.get()

    cfg_folder = api.content.create(
        container=site,
        type='Folder',
        id='config',
        Title='Task configs'
    )

    api.content.create(
        container=site,
        type='Folder',
        id='config',
        Title='Task configs'
    )

# -*- coding: utf-8 -*-


def post_install(context):
    """Post install script"""
    if context.readDataFile('urbanschedule_default.txt') is None:
        return
    # Do something during the installation of this package

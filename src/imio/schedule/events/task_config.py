# -*- coding: utf-8 -*-

from imio.schedule.content.task import IAutomatedTask
from imio.schedule.content.task_config import ITaskConfig

from plone import api

from zope.component import getUtility
from zope.component.interface import getInterface
from zope.interface import alsoProvides
from zope.interface import noLongerProvides
from zope.schema.interfaces import IVocabularyFactory


def update_marker_interfaces(task_config, event):
    """
    When the 'marker_interfaces' field is updated, update the interface
    provided on all the tasks of this task config as well.
    """
    catalog = api.portal.get_tool('portal_catalog')
    task_brains = catalog(
        object_provides=IAutomatedTask.__identifier__,
        task_config_UID=task_config.UID()
    )
    sample_task = task_brains and task_brains[0].getObject() or None

    # verify if the update is needed
    do_update = False
    if sample_task:
        for interface_name in task_config.marker_interfaces:
            marker_interface = getInterface('', interface_name)
            if not marker_interface.providedBy(sample_task):
                do_update = True
                break

    if do_update:
        vocname = ITaskConfig.get('marker_interfaces').value_type.vocabularyName
        interfaces_voc = getUtility(IVocabularyFactory, vocname)(task_config)
        marker_interfaces = dict([(i, getInterface('', i)) for i in interfaces_voc.by_value])

        for task_brain in task_brains:
            task = task_brain.getObject()

            for marker_interface_name, marker_interface in marker_interfaces.iteritems():
                if marker_interface_name in task_config.marker_interfaces:
                    alsoProvides(task, marker_interface)
                else:
                    noLongerProvides(task, marker_interface)

            task.reindexObject(idxs=['object_provides'])

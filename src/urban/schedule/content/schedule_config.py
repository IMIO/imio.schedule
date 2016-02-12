# -*- coding: utf-8 -*-

from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model

from urban.schedule import _
from urban.schedule.content.task_config import ITaskConfig
from urban.schedule.utils import tuple_to_interface

from zope import schema
from zope.interface import implements


class IScheduleConfig(model.Schema):
    """
    ScheduleConfig dexterity schema.
    """

    enabled = schema.Bool(
        title=_(u'Enabled'),
        default=True,
        required=False,
    )

    scheduled_contenttype = schema.Choice(
        title=_(u'Scheduled content type'),
        description=_(u'Select the content type to apply schedule.'),
        vocabulary='schedule.scheduled_contenttype',
        required=True,
    )


class ScheduleConfig(Container):
    """
    ScheduleConfig dexterity class.
    """

    implements(IScheduleConfig)

    def query_task_configs(self):
        """
        Query the TaskConfig of this ScheduleConfig.
        """
        catalog = api.portal.get_tool('portal_catalog')
        config_path = '/'.join(self.getPhysicalPath())

        config_brains = catalog(
            object_provides=ITaskConfig.__identifier__,
            path={'query': config_path},
            sort_on='getObjPositionInParent',
        )

        return config_brains

    def get_all_task_configs(self):
        """
        Return all the TaskConfig of this ScheduleConfig.
        """
        config_brains = self.query_task_configs()
        task_configs = [brain.getObject() for brain in config_brains]

        return task_configs

    def get_scheduled_portal_type(self):
        """
        Return the portal_type of the selected scheduled_contenttype.
        """
        return self.scheduled_contenttype and self.scheduled_contenttype[0] or ''

    def get_scheduled_interface(self):
        """
        Return the registration interface of the selected scheduled_contenttype.
        """
        portal_type, interface_tuple = self.scheduled_contenttype
        interface_class = tuple_to_interface(interface_tuple)

        return interface_class

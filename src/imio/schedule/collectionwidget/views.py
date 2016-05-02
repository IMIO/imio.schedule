# -*- coding: utf-8 -*-

from collective.eeafaceted.collectionwidget.browser.views import RenderTermView

from imio.schedule.content.schedule_config import IScheduleConfig


class RenderScheduleTermView(RenderTermView):
    """
    """

    selected_term = ''

    @property
    def depth_level(self):
        """
        """
        level = -1
        context = self.context
        while not IScheduleConfig.providedBy(context):
            context = context.aq_parent
            level = level + 1
        return level

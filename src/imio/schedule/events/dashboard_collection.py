# -*- coding: utf-8 -*-

from imio.schedule import _
from imio.schedule.content.schedule_config import IScheduleConfig
from imio.schedule.utils import create_dashboard_collection


def create(schedule_container, event):
    """ """
    # do not automatically re-create the collection during upgrade steps
    if (
        "portal_setup/manage_importSteps" in schedule_container.REQUEST.URL
        or "portal_setup/manage_doUpgrades" in schedule_container.REQUEST.URL
    ):
        return

    create_dashboard_collection(schedule_container)


def update_title(schedule_container, event):
    """
    Dashboard Collection title should always be the title of the parent task.
    """
    # do not automatically re-create the collection during upgrade steps
    if "portal_setup" in schedule_container.REQUEST.URL:
        return

    collection = getattr(schedule_container, "dashboard_collection", None)
    if collection:
        title = (
            IScheduleConfig.providedBy(schedule_container)
            and _("All")
            or schedule_container.Title()
        )
        collection.title = title
        collection.reindexObject(idxs=("Title", "sortable_title"))

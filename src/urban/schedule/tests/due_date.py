# -*- coding: utf-8 -*-

from urban.schedule.content.due_date import StartDate


class ContainerCreationDate(StartDate):
    """
    Test StartDate returning the creation date of the task container.
    """

    def start_date(self, **kwargs):
        return self.task_container.creation_date

# -*- coding: utf-8 -*-

from urban.schedule.content.due_date import DueDate


class ContainerCreationDate(DueDate):
    """
    Test DueDate returning the creation date of the task container.
    """

    def due_date(self, **kwargs):
        return self.task_container.creation_date

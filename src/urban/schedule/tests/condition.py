# -*- coding: utf-8 -*-

from urban.schedule.content.condition import EndCondition
from urban.schedule.content.condition import StartCondition


class TestStartCondition(StartCondition):
    """
    Test start condition.
    """

    def evaluate(self, **kwargs):
        return True


class TestEndCondition(EndCondition):
    """
    Test start condition.
    """

    def evaluate(self, **kwargs):
        return True

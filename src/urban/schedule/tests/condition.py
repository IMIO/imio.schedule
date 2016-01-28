# -*- coding: utf-8 -*-

from urban.schedule.content.condition import EndCondition
from urban.schedule.content.condition import StartCondition


class TestStartCondition(StartCondition):
    """
    Test task start condition.
    """

    def evaluate(self, **kwargs):
        return 'Should start'


class TestNegativeStartCondition(StartCondition):
    """
    Test task start condition.
    """

    def evaluate(self, **kwargs):
        return False


class TestEndCondition(EndCondition):
    """
    Test task end condition.
    """

    def evaluate(self, **kwargs):
        return 'Should end'


class TestNegativeEndCondition(EndCondition):
    """
    Test task end condition.
    """

    def evaluate(self, **kwargs):
        return False

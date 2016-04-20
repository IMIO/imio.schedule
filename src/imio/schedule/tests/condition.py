# -*- coding: utf-8 -*-

from imio.schedule.content.condition import CreationCondition
from imio.schedule.content.condition import EndCondition
from imio.schedule.content.condition import StartCondition


class TestCreationCondition(CreationCondition):
    """
    Test task start condition.
    """

    def evaluate(self):
        return 'Should start'


class TestNegativeCreationCondition(CreationCondition):
    """
    Test task start condition.
    """

    def evaluate(self):
        return False


class TestStartCondition(StartCondition):
    """
    Test task start condition.
    """

    def evaluate(self):
        return 'Should start'


class TestNegativeStartCondition(StartCondition):
    """
    Test task start condition.
    """

    def evaluate(self):
        return False


class TestEndCondition(EndCondition):
    """
    Test task end condition.
    """

    def evaluate(self):
        return 'Should end'


class TestNegativeEndCondition(EndCondition):
    """
    Test task end condition.
    """

    def evaluate(self):
        return False

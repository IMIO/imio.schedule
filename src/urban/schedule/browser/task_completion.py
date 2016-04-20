# encoding: utf-8

from Products.Five import BrowserView


class TaskCompletionView(BrowserView):
    """
    View of the popup showing the completion details of a task.
    Display the status of each start/end condition of the task.
    Display if the starting/ending state is matched or not.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.task = context

    def get_conditions_status(self):
        """
        List all the tasks with conditions that are not yet matched (except for workflow state).
        """

    def get_state_status(self):
        """
        """


class TaskStartStatusView(TaskCompletionView):
    """
    View of the popup showing the start completion details of a created task.
    Display the status of each start condition of the task.
    Display if the starting state is matched or not.
    """

    def get_done_conditions(self):
        """
        List all the tasks with conditions that are not yet matched (except for workflow state).
        """
        matched, not_matched = self.task.start_conditions_status()
        return matched

    def get_conditions_todo(self):
        """
        List all the tasks with conditions that are not yet matched (except for workflow state).
        """
        matched, not_matched = self.task.start_conditions_status()
        return not_matched

    def get_state_status(self):
        """
        """
        return self.task.starting_states_status()


class TaskEndStatusView(TaskCompletionView):
    """
    View of the popup showing the end completion details of a started task.
    Display the status of each end condition of the task.
    Display if the ending state is matched or not.
    """

    def get_done_conditions(self):
        """
        List all the tasks with conditions that are not yet matched (except for workflow state).
        """
        matched, not_matched = self.task.end_conditions_status()
        return matched

    def get_conditions_todo(self):
        """
        List all the tasks with conditions that are not yet matched (except for workflow state).
        """
        matched, not_matched = self.task.end_conditions_status()
        return not_matched

    def get_state_status(self):
        """
        """
        return self.task.ending_states_status()

"""
machine.py

This python file stores the base state machine used for the
overall application.
"""

'''Imports'''


class StateMachine:
    """
    The base state machine for the application.

    Detailed flow chart to be added later.
    """

    def __init__(self, initial_state):
        """
        Initialize the state machine.
        """
        self.state = initial_state

    def run(self, gui):
        """
        Run through the states of the state machine.

        :param gui:
        :return:
        """

        while self.state is not None:
            self.state = self.state.run(gui)
"""
base.py

This python file contains the base classes used
by all State objects in the project.
"""


class BaseState:
    """
    The base state class for all of the states.
    """
    def __init__(self):
        """
        Initialize the state.
        """

    def run(self, gui):
        """
        Run the state.

        :return:
        """
        self._on_enter(gui)
        self._state_main(gui)
        return self._on_exit(gui)

    def _on_enter(self, gui):
        """
        Run at the beginning of the state.

        :return:
        """

    def _state_main(self, gui):
        """
        The main code block for the state.

        :return:
        """

    def _on_exit(self, gui):
        """
        Run at the end of the state.

        :return state:
        """
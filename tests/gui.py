"""
tests/gui.py

This Python file contains the tests for the gui.
"""

'''Imports'''
import tkinter as tk
from tkinter.font import Font
from fsm.states import BaseState
from fsm import StateMachine
import sys


def first_window_attempt():
    """
    The first attempt at creating a gui.

    :return None:
    """

    class InitialState(BaseState):
        """
        Initial state for the SimpleGUI.
        """

        def _on_enter(self, gui):
            """
            Construct the buttons upon entering the state.

            :return:
            """
            print("In initial state.")

            '''Create label'''
            self.label = tk.Label(gui.root, text="First GUI")
            self.label.pack()

            '''Create buttons'''
            gui.pack_button = tk.Button(gui.root,
                                          text="Buttons",
                                          command=self.adjust_buttons(gui),
                                          font=Font(size=50))
            gui.pack_button.pack()
            gui.greet_button = tk.Button(gui.root,
                                          text="Greet",
                                          command=self._greet,
                                          font=Font(size=50))
            gui.close_button = tk.Button(gui.root,
                                          text="Close",
                                          command=gui.root.quit,
                                          font=Font(size=50))
            gui.update()


        def adjust_buttons(self, gui):
            """
            Adjust the buttons.

            :return:
            """
            def _adjust_buttons():
                print("\tButton clicked.")
                if gui.buttons_on.get():
                    print("\t\tDetected buttons are on.")
                    self._remove_buttons(gui)
                else:
                    print("\t\tDetected buttons are off.")
                    self._add_buttons(gui)
            return _adjust_buttons

        def _add_buttons(self, gui):
            """
            Add buttons to the view.

            :return:
            """
            gui.greet_button.pack()
            gui.close_button.pack()
            gui.buttons_on.set(True)

        def _remove_buttons(self, gui):
            """
            Remove buttons from the view.

            :return:
            """
            gui.greet_button.pack_forget()
            gui.close_button.pack_forget()
            gui.buttons_on.set(False)

        def _greet(self, gui):
            """

            :param gui:
            :return:
            """

        def _on_exit(self, gui):
            """
            Return the next state.

            :param gui:
            :return:
            """
            gui.update()
            return ButtonsOff()

    class ButtonsOn(BaseState):
        """
        State for having buttons on.
        """
        def _on_enter(self, gui):
            """

            :param gui:
            :return:
            """
            print("In buttons on state.")

        def _state_main(self, gui):
            """
            The main code for the ButtonsOn state.

            :param gui:
            :return:
            """
            gui.pack_button.wait_variable(gui.buttons_on)

        def _on_exit(self, gui):
            if gui.program_running:
                gui.update()
                return ButtonsOff()
            else:
                return None

    class ButtonsOff(BaseState):
        """
        State for having buttons off.
        """

        def _on_enter(self, gui):
            """

            :param gui:
            :return:
            """
            print("In buttons off state.")

        def _state_main(self, gui):
            """
            The main code for the ButtonsOn state.

            :param gui:
            :return:
            """
            gui.pack_button.wait_variable(gui.buttons_on)

        def _on_exit(self, gui):
            if gui.program_running:
                gui.update()
                return ButtonsOn()
            else:
                return None

    class SimpleGUI:
        """
        Object for a simple gui.
        """

        def __init__(self, root):
            """
            Initializing the SimpleGUI object.
            """
            self.root = root
            w, h = root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.root.geometry("%dx%d+0+0" % (w, h))
            self.root.protocol("WM_DELETE_WINDOW", self.end_program)
            self.buttons_on = tk.BooleanVar()
            self.buttons_on.set(False)
            self.program_running = True

        def update(self):
            """
            Update the GUI.

            :return:
            """
            self.root.update_idletasks()
            self.root.update()
            return self.root

        def end_program(self):
            """
            Ends the program.

            :return:
            """
            self.buttons_on.set(not self.buttons_on.get())
            self.root.destroy()
            self.program_running = False


    '''Initialize and run GUI object'''
    root = tk.Tk()
    # Maximize window while maintaining title bar
    gui = SimpleGUI(root)
    state_machine = StateMachine(initial_state=InitialState())
    state_machine.run(gui)


first_window_attempt()
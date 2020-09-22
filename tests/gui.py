"""
tests/gui.py

This Python file contains the tests for the gui.
"""

'''Imports'''
import tkinter as tk
from tkinter.font import Font


def first_window_attempt():
    """
    The first attempt at creating a gui.

    :return:
    """

    class SimpleGUI:
        """
        Object for a simple gui.
        """

        def __init__(self, master):
            """
            Initializing the SimpleGUI object.
            """

            self.master = master
            master.title("Simple GUI")

            self.label = tk.Label(master, text="First GUI")
            self.label.pack()

            self.greet_button = tk.Button(master,
                                          text="Greet",
                                          command=self.greet,
                                          font=Font(size=50))
            self.close_button = tk.Button(master,
                                          text="Close",
                                          command=master.quit,
                                          font=Font(size=50))
            self.pack_button = tk.Button(master,
                                          text="Buttons",
                                          command=self.adjust_buttons,
                                          font=Font(size=50))
            self.pack_button.pack()
            self.buttons_on = False
            self.adjust_buttons()

        def adjust_buttons(self):
            """
            Checks to see if buttons should be added or removed.

            :return:
            """
            if self.buttons_on:
                self._remove_buttons()
            else:
                self._add_buttons()

        def _add_buttons(self):
            """
            Add buttons to the view.

            :return:
            """
            self.greet_button.pack()
            self.close_button.pack()
            self.buttons_on = True

        def _remove_buttons(self):
            """
            Remove buttons from the view.

            :return:
            """
            self.greet_button.pack_forget()
            self.close_button.pack_forget()
            self.buttons_on = False

        def greet(self):
            """
            Small greeting.

            :return:
            """

            print("Hello, world!")

    '''Initialize and run GUI object'''
    root = tk.Tk()
    # Maximize window while maintaining title bar
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    my_gui = SimpleGUI(root)
    root.mainloop()


first_window_attempt()
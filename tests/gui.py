"""
tests/gui.py

This Python file contains the tests for the gui.
"""

'''Imports'''
import tkinter as tk
import tkinterdnd2
from tkinterdnd2 import DND_FILES
from tkinter.font import Font
from fsm.states import BaseState
from fsm import StateMachine
import sys
from PIL import ImageTk, Image, ImageEnhance
from ast import literal_eval
import numpy as np
import matplotlib.pyplot as plot_functions
import rawpy
import cv2
import itertools
from sklearn.linear_model import LinearRegression


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

def drag_and_drop_attempt():
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

            '''Create drag and drop window'''
            gui.entry_sv = tk.StringVar()
            gui.drop_box_list = []
            gui.drop_box_items = tk.Listbox(master=gui.root, listvariable=gui.drop_box_list)
            gui.drop_box_text = tk.StringVar()
            gui.drop_box_text.set("Drop images here")
            gui.entry = tk.Entry(gui.root, textvar=gui.drop_box_text, justify='center')
            gui.entry.config(font=("Courier", 44))
            gui.entry.place(x = 200, y=200, width=800, height=800)
            #gui.entry.pack()
            gui.entry.drop_target_register(DND_FILES)
            gui.entry.dnd_bind('<<Drop>>', self.drop(gui))
            gui.update()

        def _on_exit(self, gui):
            """
            Return the next state.

            :param gui:
            :return:
            """
            gui.update()
            return WaitForDrop()

        def drop(self, gui):
            def _drop(event):
                files = root.tk.splitlist(event.data)
                gui.entry_sv.set(files)
            return _drop

    class WaitForDrop(BaseState):
        """
        State for having buttons on.
        """

        def _on_enter(self, gui):
            """

            :param gui:
            :return:
            """
            print("In wait for drop state.")

        def _state_main(self, gui):
            """
            The main code for the ButtonsOn state.

            :param gui:
            :return:
            """
            gui.entry.wait_variable(gui.entry_sv)

            '''Clean string'''
            files = literal_eval(gui.entry_sv.get())

            '''Remove previous images'''
            if hasattr(gui, "panel"):
                gui.panel.destroy()

            '''Load each image'''
            for file_name in files:
                file_name = file_name.replace("{", "").replace("}", "")
                # image = tk.PhotoImage(file=file_name)
                if ".CR2" in file_name:
                    '''Rawpy implementation'''
                    file_image = rawpy.imread(file_name)
                    file_image = file_image.postprocess()
                    '''Rawkit implementation'''
                    '''file_image = Raw(file_name)
                    file_image = np.array(file_image.to_buffer())'''
                    '''OpenCV implementation'''
                    '''file_image = cv2.imread(file_name)'''
                else:
                    file_image = Image.open(file_name)
                '''image = file_image.resize((500, 500), Image.ANTIALIAS)
                image = ImageTk.PhotoImage(image)
                gui.panel = tk.Label(gui.root, image=image)
                gui.panel.image = image
                gui.panel.pack()'''
                # panel.grid(row=2)

            image_data = np.array(file_image)
            image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2GRAY)
            '''print(image_data.shape)
            print(image_data)
            print(len(image_data))
            print(len(image_data[0]))'''
            returned_image = Image.fromarray(image_data)
            '''cv2.imshow("Gray", image_data)
            cv2.waitKey()
            cv2.destroyWindow("Gray")'''

            '''enhanced_contrast = ImageEnhance.Contrast(Image.fromarray(file_image))
            enhanced_image = enhanced_contrast.enhance(255)
            enhanced_data = np.array(enhanced_image)
            plot_functions.imshow(enhanced_image)
            plot_functions.show()'''

            # color_space = cv2.cvtColor(image_data, cv2.COLOR_RGB2HSV)
            # print(color_space)
            
            '''Create mask for white-ish pixels'''
            '''lower_background = np.array([150, 150, 150])
            upper_background = np.array([255, 255, 255])
            print(image_data)
            white_mask = cv2.inRange(image_data, lower_background, upper_background)
            white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
            white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
            white_mask = white_mask / 255'''

            '''Create mask for black-ish pixels'''
            '''lower_background = np.array([0, 0, 0])
            upper_background = np.array([25, 25, 25])
            black_mask = cv2.inRange(image_data, lower_background, upper_background)
            black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
            black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
            black_mask = black_mask / 255'''

            '''Add masks together'''
            '''background_mask = white_mask
            # Ensure no value is above 1
            background_mask = np.clip(background_mask, 0, 1)'''
            
            copied_image_data = np.asarray(returned_image).copy()
            # background_mask = np.logical_not(background_mask)
            '''for row_index, [mask_row, image_row] in enumerate(zip(background_mask, copied_image_data)):
                # place black pixel on corresponding masked pixels
                # copied_image_data[row_index] = np.array([image_row[pixel] * int(mask_row[pixel]) for pixel in range(len(mask_row))])
                # make pixel fully white on corresponding masked pixels
                copied_image_data[row_index] = np.array([np.array([255, 255, 255]) if int(mask_row[pixel]) else image_row[pixel] for pixel in range(len(mask_row))])'''

            '''Turn removed pixels red'''
            '''mask_image = Image.fromarray(copied_image_data)
            plot_functions.imshow(mask_image)
            plot_functions.show()'''
            trapezoid_data = copied_image_data.copy()

            enhanced_contrast = ImageEnhance.Contrast(Image.fromarray(trapezoid_data))
            enhanced_image = enhanced_contrast.enhance(255)
            trapezoid_data = np.array(enhanced_image)

            '''Detect lines'''
            edges = cv2.Canny(trapezoid_data, 75, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, maxLineGap=1000)
            # print(lines)
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if y1 == y2:
                    cv2.line(copied_image_data, (x1, y1), (x2, y2), (255, 255, 255), 1)

            '''Trapezoid attempt'''

            # filters image bilaterally and displays it
            bilatImg = cv2.bilateralFilter(trapezoid_data, 5, 175, 175)

            # finds edges of bilaterally filtered image and displays it
            edgeImg = cv2.Canny(bilatImg, 75, 200)

            # gets contours (outlines) for shapes and sorts from largest area to smallest area
            contours, hierarchy = cv2.findContours(edgeImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            # drawing red contours on the image
            for con in contours:
                cv2.drawContours(trapezoid_data, con, -1, (255, 255, 255), 3)

            '''Detect corners'''
            dst = cv2.cornerHarris(edges, 30, 31, 0.001)
            dst = cv2.dilate(dst, None)
            ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
            dst = np.uint8(dst)

            # find centroids
            ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
            # define the criteria to stop and refine the corners
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100,
                        0.001)
            corners = cv2.cornerSubPix(edges, np.float32(centroids), (5, 5),
                                       (-1, -1), criteria)

            good_corners = []
            for corner in corners:
                if (corner[1] < 1000) & (corner[1] > 650) & (corner[0] > 250) & (corner[0] < 2250):
                    good_corners.append(corner)
                    cv2.circle(edges, (corner[0], corner[1]), 10, (255, 255, 255))

            print(good_corners)
            if len(good_corners) >= 3:
                corner_combos = itertools.combinations(good_corners, 3)
            elif len(good_corners) > 1:
                corner_combos = itertools.combinations(good_corners, 2)

            best_corner_combo = None
            best_coef = np.inf
            for corner_combo in corner_combos:
                regression = LinearRegression().fit(np.array([corner[0] for corner in corner_combo]).reshape(-1, 1),
                                                    np.array([corner[1] for corner in corner_combo]))
                if np.abs(regression.coef_) < best_coef:
                    best_coef = np.abs(regression.coef_)
                    best_corner_combo = np.array([corner[1] for corner in corner_combo])

            y_edge = int(round(np.mean(best_corner_combo)))
            edges = edges[y_edge:3000, 200:2200]
            copied_image_data = copied_image_data[y_edge:2500, 200:2200]
            trapezoid_data = trapezoid_data[y_edge:2500, 200:2200]

            # and double-checking the outcome
            cv2.imshow("linesEdges", edges)
            cv2.imshow("linesDetected", copied_image_data)
            cv2.imshow("Contours check", trapezoid_data)
            cv2.waitKey()
            cv2.destroyWindow("Contours check")

            # find the perimeter of the first closed contour
            perim = cv2.arcLength(contours[0], True)
            # setting the precision
            epsilon = 0.02 * perim
            # approximating the contour with a polygon
            approxCorners = cv2.approxPolyDP(contours[0], epsilon, True)
            # check how many vertices has the approximate polygon
            approxCornersNumber = len(approxCorners)

            for corners in approxCorners:
                cv2.circle(trapezoid_data, (corners[0], corners[1]), radius=10, color=(255, 255, 255), thickness=-1)
            cv2.imshow("Vertex position", trapezoid_data)
            cv2.waitKey()
            cv2.destroyWindow("Vertex position")
            cv2.imshow("linesEdges", edges)
            cv2.imshow("linesDetected", copied_image_data)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        def _on_exit(self, gui):
            if gui.program_running:
                gui.update()
                return WaitForDrop()
            else:
                return None

    class DragAndDropGUI:
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
            if self.entry_sv.get() != " ":
                self.entry_sv.set(" ")
            else:
                self.entry_sv.set("!")
            self.root.destroy()
            self.program_running = False

    '''Initialize and run GUI object'''
    root = tkinterdnd2.Tk()
    # Maximize window while maintaining title bar
    gui = DragAndDropGUI(root)
    state_machine = StateMachine(initial_state=InitialState())
    state_machine.run(gui)


drag_and_drop_attempt()

'''root = tkinterdnd2.Tk()

img = tk.PhotoImage(file="/home/nczeak/Downloads/Simple Space Wallpaper (16_10).png")

label = tk.Label(root, image=img)
label.pack()

root.mainloop()'''
"""
Code adapted from: https://github.com/foobar167/junkyard/tree/master/manual_image_annotation1
"""

# Importing packages
import tkinter as tk
from PIL import Image, ImageTk

# Helper classes
# from auto_scrollbar import AutoScrollbar

# Class to display canvas widget on parent (MainWindow: tk.Frame)
class ImageCanvas:

    def __init__(self, master: tk.Tk, image_file: str):
        self.master = master
        self.image_file = image_file

        # Filter to apply when displaying image (NEAREST = original, LANCZOS = antialias)
        # self.__filter = Image.NEAREST 
        self.__filter = Image.LANCZOS

        self.__previous_state = 0 # Previous state of the key presses

        # Creating Canvas and binding keys to events
        self.canvas = tk.Canvas(self.master, background="gray12", cursor="spider")
        self.canvas.grid(row=0, column=0, sticky='nswe') # Displaying Canvas in grid of parent
        self.canvas.update() # Updating canvas
        self.__bind_events() # Calling function to bind keys to events

        # Loading image and storing relevant details
        self.pil_image = Image.open(self.image_file)
        self.img_width, self.img_height = self.pil_image.size # Image height/width
        self.__min_side = min(self.img_height, self.img_width) # Smallest side of image

        # Creating rectangle container to store/track image on Canvas
        self.img_container = self.canvas.create_rectangle(0, 0, self.img_width, self.img_height, width=0)

        self.__display_image() # Displaying image
        breakpoint()

    ### Event bindings and associated functions
    # Binds keys to events
    def __bind_events(self) -> None:
            self.canvas.bind('<Button-1>', self.button_1_test)
            self.canvas.bind('<MouseWheel>', self.zoom_wheel) # Mouse wheel for zooming

    # Function to test key bidnings
    def button_1_test(self, event) -> None:
        print(f"Button 1 (LMB) pressed at {event.x, event.y}") # Sanity check
        self.__old_event = event # Updating previous event

    # Zooms at current cursor location inside image
    def zoom_wheel(self, event):

        pass

    def outside_img_region(self, event_x, event_y):
        img_area = self.canvas.coords(self.container)
        pass

    # Displays image on canvas
    def __display_image(self):
        pass
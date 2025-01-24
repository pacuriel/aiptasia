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
        self.__filter = Image.NEAREST 
        # self.__filter = Image.LANCZOS

        self.__previous_state = 0 # Previous state of the key presses

        # Creating Canvas and binding keys to events
        self.canvas = tk.Canvas(self.master, background="black", cursor="spider")
        self.canvas.grid(row=0, column=0, sticky='nswe') # Displaying Canvas in grid of parent
        self.canvas.update() # Updating canvas

        self.__bind_events() # Calling function to bind keys to events

    # Binds keys to events
    def __bind_events(self) -> None:
            self.canvas.bind('<Button-1>', self.button_1_test)
    
    # Function to test key bidnings
    def button_1_test(self, event):
        print(f"Button 1 (LMB) pressed at {event.x, event.y}") # Sanity check
        self.__old_event = event # Updating previous event

    # Places ImageCanvas 
    def grid(self, **kwargs):
        pass
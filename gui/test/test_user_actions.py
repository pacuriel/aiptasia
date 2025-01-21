# import tkinter as tk
# import numpy as np
from PIL import Image#, ImageTk

from test_image_transformation import ImageTransformations

class UserActions:
    def __init__(self, master):
        self.master = master
        
        self.image_transformations = ImageTransformations()

    # Function to set PIL image
    def set_image(self, pil_image):
        self.pil_image = pil_image

    ### User actions
    # Function that triggers when ctrl+LMB pressed
    def ctrl_lmb_down(self, event):
        print(f"Control and LMB pressed at ({event.x}, {event.y})!")
        self.__old_event = event

    # Function to pan by pressing and holding ctrl+LMB
    def ctrl_lmb_pan(self, event):
        if (self.pil_image == None):
            return
        
        # Change in vertical and horizontal directions to pan to
        dx = event.x - self.__old_event.x
        dy = event.y - self.__old_event.y

        # Calling function to perform translation (panning)
        self.image_transformations.translate(offset_x=dx, offset_y=dy)
        # self.redraw_image()
        # self.__old_event = event
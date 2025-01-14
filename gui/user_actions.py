import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

from image_transformations import ImageTransformations

# Class to handle user actions (button presses, etc.)
class UserActions:

    def __init__(self, master):
        super().__init__()
        self.master = master
        self.image_transformations = ImageTransformations()
        self.pil_image = None

    # Create canvas and setting button bindings
    def create_widget(self):
        self.canvas = tk.Canvas(self.master, background="black", cursor="spider")
        self.canvas.pack(expand=True,  fill=tk.BOTH)
        
        # bindings
        # self.master.bind("<Button-1>", self.mouse_down_left) # MouseDown
        # self.master.bind("<B1-Motion>", self.mouse_move_lesft) # MouseDrag
        self.canvas.bind("<MouseWheel>", self.mouse_wheel) # MouseWheel
        # self.canvas.bind("<Button-3>", self.start_line) # Right mouse button for drawing lines
        # self.canvas.bind("<Button-2>", self.mouse_wheel_down) # Mouse wheel button pressed
        self.canvas.bind("<Control-Button-1>", self.ctrl_lmb_down) # Resets event when Control + LMB are pressed
        self.canvas.bind("<Control-B1-Motion>", self.ctrl_lmb_down_pan) # Control + LMB motion for panning


    ### User actions
    # Function that triggers new event once mouse wheel button is pressed
    def ctrl_lmb_down(self, event):
        self.__old_event = event

    # Function to pan by pressing down Control + LMB
    def ctrl_lmb_down_pan(self, event):
        if (self.pil_image == None):
            return
        self.image_transformations.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image()
        self.__old_event = event
    
    # Function to zoom based on mouse wheel action
    def mouse_wheel(self, event):
        if self.pil_image == None:
            return
        if (event.delta > 0): # Zoom in
            self.image_transformations.scale_at(1.25, event.x, event.y)
        else: # Zoom out
            self.image_transformations.scale_at(0.8, event.x, event.y)
        self.redraw_image()

    def redraw_image(self):
        if self.pil_image == None:
            return
        
        self.draw_image(self.pil_image)

    # Update display according to user actions
    def draw_image(self, pil_image):
        # self.canvas.delete('all') # remove previously drawn lines
        
        # IMAGE TRANSFORMATION
        if pil_image == None:
            return

        self.pil_image = pil_image

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        mat_inv = np.linalg.inv(self.image_transformations.mat_affine)

        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
            )

        dst = self.pil_image.transform((canvas_width, canvas_height), Image.AFFINE,affine_inv, Image.NEAREST)
        im = ImageTk.PhotoImage(image=dst)
        item = self.canvas.create_image(0, 0,anchor='nw', image=im)
        self.image = im

    # Function to set PIL image
    def set_image(self, pil_image):
        self.pil_image = pil_image

    def reset_transform(self):
        self.image_transformations.reset_transform()
"""
Code adapted from PythonImageViewer on GH: https://github.com/ImagingSolution/PythonImageViewer
"""
# Python packages
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import math
import numpy as np
import os
import matplotlib.pyplot as plt

# 
from user_actions import UserActions
from image_transformations import ImageTransformations

# line_coords = []

"""
Current setup idea/modifications: 
- Pan: hold mouse wheel and drag cursor
- Zoom: spin mouse wheel
- Positive point prompt: right click (Button-3)
- Negative point prompt: left click (Button-1)

Thought process for pos/neg prompt buttons: 
- Most prompts for our case will be the negative case, likely circling around each aiptasia oral disk
- Left click seems more stable (for me)
- The right click for positive point prompts will not have to be as accurate

Other possible features: 
- Look into adding a second layer for overlapping/touching aiptasia
- Set max zoom out such that entire image fits and is viewable (i.e. don't allow for infinite zoom out; seems pointless) 
"""

VERSION_NUMBER = 0.1 # Version number of current application

# Class representing image viewer application
class ImageViewer(tk.Frame):
    
    # Initializing and setting window properties 
    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry("600x400") 
        self.pil_image = None 
        self.line_start = None
        self.my_title = "PyPointCounter"

        self.user_actions = UserActions(master=self.master) # Object to control user actions
        
        self.create_menu()

        self.user_actions.create_widget()

        self.user_actions.reset_transform()
    
    # Menu bar at top of application
    def create_menu(self):
        self.menu_bar = tk.Menu(self) # Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff = tk.OFF)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu) # File option 
        self.file_menu.add_command(label="Open Image", command = self.menu_open_clicked)
        self.master.config(menu=self.menu_bar)

    # Menu bar options
    def menu_open_clicked(self, event=None):
        filename = tk.filedialog.askopenfilename(
            filetypes = [("Image file", ".bmp .png .jpg .tif"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ],
            initialdir = os.getcwd()
            )

        self.set_image(filename)
    
    # Load image file
    def set_image(self, filename):
        if not filename:
            return
        self.pil_image = Image.open(filename)
        self.user_actions.set_image = self.pil_image
        self.user_actions.draw_image(self.pil_image)
        os.chdir(os.path.dirname(filename))
    
    

    """
    # line drawing with two right mouse clicks - start and end points
    def start_line(self, event):
        if self.line_start is None:
            self.line_start = (event.x, event.y)
        else:
            end_point_x, end_point_y = event.x, event.y
            self.canvas.create_line(self.line_start[0], self.line_start[1], end_point_x, end_point_y, fill='red')
            line_start = tuple([self.line_start[0], self.line_start[1]])
            line_end = tuple([end_point_x, end_point_y])
            line_coords.append([line_start, line_end])
            self.line_start = None
  
        # LINE COORDINATE TRANSFORMATION
        def transform_line_coords(i):
            original_coords = line_coords[i] # original coordinates
            homogeneous_coords = np.column_stack((np.array(original_coords), np.ones(len(original_coords))))
            transformation_matrix = self.mat_affine.T
            transformed_coords = np.dot(homogeneous_coords, transformation_matrix)
            cartesian = transformed_coords[:, :2]
            start_point = tuple([cartesian[0,0], cartesian[0,1]])
            end_point = tuple([cartesian[1,0], cartesian[1,1]])
            return [start_point, end_point]
             
        # overwrite original line coordinates [[(x1_start,y1_start), (x1_end,y1_end)], [(x2_start,y2_start), (x2_end,y2_end)]...], 
        # with transformed cordinates.
        global line_coords
        line_coords = [transform_line_coords(i) for i in range(0, len(line_coords))]
        
        # re-draw the lines defined in the global list of lines
        def draw_line(i):
            x1 = line_coords[i][0][0]
            y1 = line_coords[i][0][1]
            x2 = line_coords[i][1][0]
            y2 = line_coords[i][1][1]
            self.canvas.create_line(x1,y1,x2,y2, fill='red')
        
        draw_lines = [draw_line(i) for i in range(0, len(line_coords))]
        """

def main():
    root = tk.Tk() # Top-level Tk widget (main window of application)
    root.state("zoomed") # Setting window to maximized
    root.title(f"Image Viewer/Prompter v{VERSION_NUMBER}")

    app = ImageViewer(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
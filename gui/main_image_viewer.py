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

# Dictionaries to store prompt image coords. Format = {'file_name': [(pixel_coords_tuple)]}
pos_prompt_coords = dict() 
neg_prompt_coords = dict()

"""
Current setup idea/modifications: 
- Pan: hold ctrl and LMB and drag cursor
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
        # self.my_title = "PyPointCounter"

        self.user_actions = UserActions(master=self.master) # Object to control user actions
        
        self.create_menu()

        self.user_actions.create_widget()

        self.user_actions.reset_transform()

        # Below two lines used for faster testing) 
        # test_file = "C:/Users/tcuri/Documents/_UC Merced Documents/research/insite/code/gui/CC7.265.1.2023.10.13.png"
        test_file = "C:/Users/tcuri/Documents/_UC Merced Documents/research/insite/code/gui/segmented_cat_5.png"

        self.set_image(filename=test_file)
    
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
        ### Do we need to store the pil_image in both the main class and user_actions class???
        self.pil_image = Image.open(filename)

        self.user_actions.set_image(self.pil_image)
        self.user_actions.draw_image(self.pil_image)
        os.chdir(os.path.dirname(filename))

def main():
    root = tk.Tk() # Top-level Tk widget (main window of application)
    root.state("zoomed") # Setting window to maximized
    root.title(f"Image Viewer/Prompter v{VERSION_NUMBER}")

    app = ImageViewer(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
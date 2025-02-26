"""Main application frame inside the main window (aka where the magic happens)."""
# Importing packages
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os

# Helper classes and functions
from menu_bar import MenuBar
from image_canvas import ImageCanvas
from utils import is_image

class MainFrame(ttk.Frame):
    """Class representing main frame inside main window."""
    def __init__(self, master) -> None:
        """Initialize the main application frame.
        
        Args:
            master: A Tkinter widget to be the parent of the MainFrame object.
        """
        super().__init__(master=master)

        self.master = master # Parent widget (likely tk.Tk)

        self.__img_frame = None # Frame to show image in
        
        self.__setup_main_window() # Setting up main window
        self.__create_widgets() # Creating application widgets

        ### Below is for testing purposes
        img_path = "C:\\Users\\tcuri\\Documents\\_UC Merced Documents\\research\\insite\\code\\gui\\CC7.265.1.2023.10.13.png"
        self.__set_image(img_path)

    def __setup_main_window(self):
        # Setting application/window title
        self.__application_title = "Aiptasia image viewer app"
        self.master.title(self.__application_title) 

    def __create_widgets(self):
        """Creates main window and frame widgets."""
        # Dictionary with links to helper functions for MenuBar
        self.menu_funcs = { 
            "open_image": self.__open_image
        }

        # Creating menu bar widget
        self.__menu_bar = MenuBar(master=self.master, helper_funcs=self.menu_funcs)
        self.master.configure(menu=self.__menu_bar)

    def __open_image(self) -> None:
        """Opens new image once selected from file menu."""

        # Dialog prompting user to open image file
        image_path = askopenfilename(
            title='Select an image',
            filetypes=[("Image file", ".bmp .png .jpg .tif"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ],
            initialdir = os.getcwd()
            )
        
        # Checking if selected file is an image
        if not is_image(image_path=image_path):
            # Outputting message to user
            messagebox.showinfo(title="Not an image file",
                                message=f"Selected file ({image_path}) is not an image.\nPlease select an image file.")

            # Trying to open image file again
            self.__open_image()
            return

        self.__set_image(image_path=image_path)

    def __set_image(self, image_path) -> None:
        """Sets a newly selected image and closes previously opened image.
        
        Args:
            image_path: path to image to set.
        """
        self.__close_image() # Closing previously opened image

        # Update window title
        self.master.title(self.__application_title + f" - Current file: {image_path}")

        # Creating and displaying image frame object
        self.__img_frame = ImageCanvas(master=self, image_file=image_path)
        self.__img_frame.grid() ### Sanity check
    
    def __close_image(self) -> None:
        """Closes previously opened image."""
        if self.__img_frame:
            self.__img_frame.destroy()

        # self.__img_frame = 
        pass
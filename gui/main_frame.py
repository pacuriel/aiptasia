"""Main application frame inside the main window (aka where the magic happens)."""
# Importing packages
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import sys
import logging

# Helper classes and functions
from menu_bar import MenuBar
from prompting import Prompting
# from image_canvas import ImageCanvas
from utils import is_image

class MainFrame(ttk.Frame):
    """Class representing main frame inside main window."""
    def __init__(self, master: tk.Tk) -> None:
        """Initialize the main application frame.
        
        Args:
            master: A Tkinter widget to be the parent of the MainFrame object.
        """
        super().__init__(master=master)

        self.master = master # Parent widget (likely tk.Tk)
        self.version_number = self.master.get_version_number() # Storing version number
        self.__img_frame = None # Frame to show image in
        
        self.__setup_main_window() # Setting up main window
        self.__create_widgets() # Creating application widgets
        self.__set_mode() # Ask user to set application mode
        self.__run_mode() # Running mode selected by user

    def __setup_main_window(self) -> None:
        # Setting application/window title
        self.__application_title = "Aiptasia image viewer app v" + str(self.master.get_version_number()) 
        self.master.title(self.__application_title) 

    def __create_widgets(self) -> None:
        """Creates main window and frame widgets."""
        # Dictionary with links to helper functions for MenuBar
        self.menu_funcs = { 
            "open_image": self.__open_image,
            "set_mode": self.__set_mode
        }

        # Creating menu bar widget
        self.__menu_bar = MenuBar(master=self.master, helper_funcs=self.menu_funcs)
        self.master.configure(menu=self.__menu_bar)

    def __set_mode(self) -> None:
        """Sets application mode. (Planned) Options: Prompting, Editing, Predicting."""
        self.mode = None # Initializing main window

        # Toplevel window for user to set 
        mode_window = tk.Toplevel(self.master)
        mode_window.title("Application Mode Selection")
        mode_window.geometry(f"400x200+{self.master.winfo_screenwidth() // 2}+{self.master.winfo_screenheight() // 2}")
        mode_window.transient(self.master) # Ensures toplevel stays above root
        mode_window.grab_set() # Directing application attention to toplevel window

        # Message label on Toplevel window
        message = "Please select an application mode"
        tk.Label(master=mode_window, text=message).pack(pady=10)

        # Buttons for each application mode
        prompting_button = tk.Button(master=mode_window, text="Prompting", command=lambda: self.__set_prompting_mode(mode_window))
        editing_button = tk.Button(master=mode_window, text="Editing", command=lambda: self.__set_editing_mode(mode_window))
        prediction_button = tk.Button(master=mode_window, text="Prediction", command=lambda: self.__set_prediction_mode(mode_window))
        prompting_button.pack(pady=5); editing_button.pack(pady=5); prediction_button.pack(pady=5); # Placing buttons
        
        self.master.wait_window(mode_window) # Main window waits until mode is selected
        
        # Checking if mode was set
        if self.mode is None:
            self.__set_mode()

        # Updating main window title
        self.__application_title += f" - Mode={self.mode}" 
        self.master.title(self.__application_title)

    def __set_prompting_mode(self, mode_window: tk.Toplevel) -> None:
        self.mode = "prompting"
        mode_window.destroy()

    def __set_editing_mode(self, mode_window: tk.Toplevel) -> None:
        self.mode = "editing"
        logging.error(f"{self.mode[0].upper() + self.mode[1:]} Mode under construction as of version {self.master.get_version_number()}. Goodbye.")
        mode_window.destroy()
        sys.exit(1)

    def __set_prediction_mode(self, mode_window: tk.Toplevel) -> None:
        self.mode = "prediction"
        logging.error(f"{self.mode[0].upper() + self.mode[1:]} Mode under construction as of version {self.master.get_version_number()}. Goodbye.")
        mode_window.destroy()
        sys.exit(1)

    def __run_mode(self) -> None:
        """Running selected application mode."""
        if self.mode == "prompting":
            self.__prompting_mode() # Running prompting mode
        elif self.mode == "editing":
            pass
        elif self.mode == "prediction":
            pass
        elif self.mode is None:
            pass

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

    def __prompting_mode(self) -> None:
        """Starts GUI's prompting mode."""
        ### Below is for testing purposes
        image_path = "C:\\Users\\tcuri\\Documents\\_UC Merced Documents\\research\\insite\\code\\gui\\CC7.265.1.2023.10.13.png"
        # self.__set_image(img_path)

        # Update window title
        self.master.title(self.__application_title + f" - Current file: {image_path}")

        self.__img_frame = Prompting(master=self, image_file=image_path)
        self.__img_frame.grid()

    def __set_image(self, image_path) -> None:
        """Sets a newly selected image and closes previously opened image.
        
        Args:
            image_path: path to image to set.
        """
        self.__close_image() # Closing previously opened image

        # Update window title
        self.master.title(self.__application_title + f" - Current file: {image_path}")

        # Creating and displaying image frame object
        # self.__img_frame = ImageCanvas(master=self, image_file=image_path)
        # self.__img_frame.grid()
    
    def __close_image(self) -> None:
        """Closes previously opened image."""
        if self.__img_frame:
            self.__img_frame.destroy()

        # self.__img_frame = 
        pass
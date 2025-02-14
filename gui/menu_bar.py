import tkinter as tk ### Import tkinter or tk.Menu???
from tkinter import filedialog
import sys # Used for exit
import os

class MenuBar(tk.Menu):
    """Class representing menu bar at top of window."""
    def __init__(self, master, helper_funcs: dict) -> None:
        """Initializes menu bar class.
        
        Args:
            master: parent widget of menu bar.
            helper_funcs: a dictionary with links to helper functions
            to use in the menu bar.
        """
        super().__init__(master=master) # For class inheritance

        self.master = master # Parent widget
        self.helper_funcs = helper_funcs # Helper functionss

        self.__create_menus() # Creating menu bar

    def __create_menus(self) -> None:
        """Creates menu bar and options."""
        # File button and dropdown options
        self.file = tk.Menu(master=self, tearoff=tk.OFF)
        self.add_cascade(label='File', menu=self.file, underline=0)
        self.file.add_command(label="Open Image", underline=0, command=self.helper_funcs["open_image"])
        
        self.file.add_command(label="Exit", underline=1, command=self.quit) # Exits application
        
        # View button
        self.view = tk.Menu(master=self, tearoff=tk.OFF)
        self.add_cascade(label="View", menu=self.view, underline=0)
        self.view.add_cascade(label="Fullscreen", )#, command=self.helper_funcs["fullscreen"])

        # Mode button
        self.mode = tk.Menu(master=self, tearoff=tk.OFF)
        self.add_cascade(label="Mode", menu=self.mode, underline=0)
        self.mode.add_cascade(label="Prompting", underline=0, command=self.helper_funcs["prompting_mode"])


    # Exits application
    def quit_app(self) -> None: 
        sys.exit(0)

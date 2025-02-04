import tkinter as tk ### Import tkinter or tk.Menu???
from tkinter import filedialog
import sys # Used for exit
import os

class MenuBar(tk.Menu):
    """Class representing menu bar at top of window."""
    def __init__(self, master, helper_funcs):
        """Initializes menu bar class.
        
        Args:
            master: parent widget of menu bar
        """
        super().__init__(master=master)

        self.master = master

        self.file_name = None

        self.__create_menu()

    def __create_menu(self) -> None:
        """Creates menu bar and options."""
        # File button
        self.file_menu = tk.Menu(master=self, tearoff=tk.OFF)
        self.add_cascade(label='File', menu=self.file_menu, underline=0)
        self.file_menu.add_command(label="Open Image", command=self.add_image_clicked)
        
        # self.file_menu.add_command(label="Exit", underline=1, command=self.quit) # Exits application
        
    def add_image_clicked(self, event=None) -> None:
        """Saves image path from file menu."""
        file_name = filedialog.askopenfilename(
            filetypes = [("Image file", ".bmp .png .jpg .tif"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ],
            initialdir = os.getcwd()
            )
        
        self.file_name = file_name
        # print(self.file_name)

    # Exits application
    def quit_app(self) -> None: 
        sys.exit(0)

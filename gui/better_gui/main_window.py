import tkinter as tk

# Helper classes
from main_frame import MainFrame
from menu_bar import MenuBar

class MainWindow(tk.Tk):
    """ Class representing main application window"""
    def __init__(self) -> None:
        """Initializes the main application window."""
        super().__init__()  # For class inheritance

        self.__configure_main_window() # Configuring main window

    def __configure_main_window(self) -> None:
        """Configures the main window components."""
        self.state("zoomed") # Maximizing main window once opened 

        # Setting application/window title
        self.__application_title = "Aiptasia image viewer app"
        self.title(self.__application_title) 

        # Creating primary frame inside window
        self.main_frame = MainFrame(master=self)

        # Creating menu bar
        self.menu_bar = MenuBar(master=self)
        self.configure(menu=self.menu_bar)

        ### Configure grid here or in main_frame?
        
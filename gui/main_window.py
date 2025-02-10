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

        # Creating primary frame inside main window
        self.main_frame = MainFrame(master=self)

    def __configure_main_window(self) -> None:
        """Configures the main window components."""
        self.state("zoomed") # Maximizing main window once opened 

        # Configuring grid inside main window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        ### What else should we do here? 
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

        self.create_main_frame()

    def __configure_main_window(self) -> None:
        """Configures the main window components."""
        self.state("zoomed") # Maximizing main window once opened 
        self.version_number = 0.1 # Version number of application
        # Configuring grid inside main window
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        ### What else should we do here? 

    def create_main_frame(self) -> None:
        """Create main frame inside main window and configure."""
        self.main_frame = MainFrame(master=self)
        self.main_frame.grid(row=0, column=0, sticky='nswe')
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
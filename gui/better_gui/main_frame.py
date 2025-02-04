import tkinter as tk

class MainFrame(tk.Frame):
    """Class representing main frame inside main window."""
    def __init__(self, master) -> None:
        """Initialize the frame.
        
        Args:
            master: A Tkinter widget to be the parent of the MainFrame object.
        """
        super().__init__()

        self.master = master

        self.__create_widgets() # Creating application widgets

    def __create_widgets(self):
        """Creates main window and frame widgets."""

    def __set_image(self):
        """Sets the image once selected from menu bar"""
        

    

# import tkinter as tk

class Prompt:
    """Class representing user point prompts on image."""
    def __init__(self, image_file: str, x: int, y: int, is_pos) -> None:
        """Initializes prompt object.
        
        Args: 
            image_file: string representing path to image
            x: x-coordinate of prompt on image
            y: y-coordinate of prompt on image
        """
        self.image_file = image_file # File path to image
        self.is_pos = is_pos # Boolean representing 
        self.coords = (x, y) # Coordinates of prompt on image

        self.store_prompt()

    def store_prompt(self) -> None:
        """Stores prompt details in CSV file."""
        pass
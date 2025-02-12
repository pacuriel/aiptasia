
# import tkinter as tk
import uuid

class Prompt:
    """Class representing user point prompts on image."""
    def __init__(self, image_file, image_coords, is_pos) -> None:
        """Initializes prompt object.
        
        Args: 
            image_file: string representing path to image
            x: x-coordinate of prompt on image
            y: y-coordinate of prompt on image
        """
        self.image_file = image_file # File path to image
        self.is_pos = is_pos # Boolean representing 
        self.image_coords = image_coords # Coordinates of prompt on image

        self.prompt_id = uuid.uuid4() # Generating prompt id

        self.store_prompt()

    def store_prompt(self) -> None:
        """Stores prompt details in CSV file."""
        pass
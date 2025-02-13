
# import tkinter as tk
import uuid

"""
Notes:
- Make light in terms of memory 
- Avoid storing tk widgets, if possible
- Highly modular/adaptable
- 
"""

class Prompt:
    """Class representing user point prompts on image."""
    def __init__(self, image_file, image_coords, canvas_coords, is_pos) -> None:
        """Initializes prompt object.
        
        Args: 
            image_file: string representing path to image
            x: x-coordinate of prompt on image
            y: y-coordinate of prompt on image
        """
        self.image_file = image_file # File path to image
        self.is_pos = is_pos # Boolean representing whether prompt is positive
        self.image_coords = image_coords # Coordinates of prompt on image
        self.canvas_coords = canvas_coords # Coordintaes of prompt on canvas 
        #(not sure about this ^ one bc it changes often)

        self.prompt_id = uuid.uuid4() # Generating unique prompt id (aka primary key)
        # self.aip_id = self.__set_aip_id()

    ### Placing and drawing prompts
    def place_prompt(self, event):
        pass

    def draw_prompt(self):
        pass

    def redraw_prompts(self):
        pass

    def canvas_to_image_coords(self, canvas_coords):
        pass

    def image_to_canvas_coords(self, image_coords):
        pass

    ### Setter and getter functions

    ### Utility/helper functions
    def __set_aip_id(self) -> uuid.UUID:
        """Sets aiptasia id if it doesn't have one yet.
        
        Returns:
            Unique identifier for aiptasia object."""
        
    def store_prompt(self) -> None:
        """Stores prompt details in CSV file."""
        pass
    
    

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
    """Class representing point prompts on image."""
    def __init__(self, image_file, prompt_coords, is_pos, ):#, aip_id) -> None:
        """Initializes new prompt object.
        
        Args: 
            image_file: string representing path to image
            x: x-coordinate of prompt on image
            y: y-coordinate of prompt on image
        """
        self.image_file = image_file # File path to image
        self.__is_pos = is_pos # Boolean representing whether prompt is positive
        self.__prompt_coords = prompt_coords # Coordinates of prompt on image
        self.__canvas_oval_id = None #

        self.__prompt_id = uuid.uuid4() # Generating unique prompt id (aka primary key)
        # self.aip_id = aip_id # Non-unique aiptasia ID
        ### Find way to set aip id in this class
        # self.aip_id = self.__set_aip_id()

        # Place new prompt on canvas at event location
        # self.place_prompt(event, canvas) 

    ### Setter and getter functions
    def get_prompt_id(self):
        return self.__prompt_id
    
    def get_is_pos(self):
        return self.__is_pos
    
    def get_prompt_coords(self):
        return self.__prompt_coords
    
    def set_canvas_oval_id(self, canvas_oval_id) -> None:
        """Sets canvas oval ID for visual point"""
        self.__canvas_oval_id = canvas_oval_id

    def get_canvas_oval_id(self):
        return self.__canvas_oval_id

    def __set_aip_id(self) -> uuid.UUID:
        """Sets aiptasia id if it doesn't have one yet.
        
        Returns:
            Unique identifier for aiptasia object."""

    ### Utility/helper functions
    def store_prompt(self) -> None:
        """Stores prompt details in CSV file."""
        pass

    def find_overlapping(self):
        pass
    
    def outside(self):
        pass

    def check_overlap(self):
        pass
    
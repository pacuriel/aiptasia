import pandas as pd

from image_canvas import ImageCanvas
from prompt import Prompt

class Prompting(ImageCanvas):
    """Class for prompting mode. Inherits from ImageCanvas."""
    def __init__(self, master, image_file) -> None:
        """Initialize the prompting mode."""
        super().__init__(master, image_file) # Initializing base class

        # Setting prompting related variables
        self.prompts = [] # List of user prompts
        self.aip_id = 0 # ID of current aiptasia being prompted (updates every positive prompt)
        ### Find a better way to set aiptasia ID ^

        self.prompt_csv_path = ".\\temp_log\\prompting.csv" # Path to prompting csv file

        self.__check_prompt_csv()

        self.__bind_events() # Binding events relevant to prompting
    
    def __check_prompt_csv(self):
        self.prompt_data = pd.read_csv(self.prompt_csv_path, header=0)
        if self.prompt_data.empty: return
        ### Load in previously prompted file here

    def __bind_events(self) -> None:
        """Binding prompting events to keys."""
        # Placing prompts
        self.canvas.bind('<Button-1>', self.place_new_prompt)
        self.canvas.bind('<Button-3>', self.place_new_prompt)

        # Undoing/redoing
        self.canvas.bind('<Control-z>', self.undo)
        self.canvas.bind('<Control-Shift-Z>', self.redo)

    ### Prompting
    def place_new_prompt(self, event) -> None:
        """Places new prompt on image canvas at cursor location."""   
        # Convert event coords to canvas coords
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)

        # Do nothing if curosr is outside of image region
        if self.outside(x_canvas, y_canvas):
            return

        # Ignoring if prompt clicked
        clicked_items = self.canvas.find_overlapping(x_canvas, y_canvas, x_canvas, y_canvas) # List of clicked items
        for prompt in self.prompts:
            if prompt.get_canvas_oval_id() in clicked_items: return # Ignoring if prompt clicked

        is_pos, color = (True, "green") if event.num == 1 else (False, "red") # Storing prompt type and color
        ### this ^ line is very satisfying. thanks python

        promtp_coords = self.canvas_to_image_coords(x_canvas, y_canvas) # Obtain image coordinates
        canvas_oval_id = self.draw_point(x_canvas, y_canvas, color=color) # Drawing prompt on canvas

        # Updating aiptasia ID
        if self.prompts and is_pos: # Prompts exist and current prompt is positive
            self.aip_id += 1

        # Creating new prompt object and appending to Prompt stack
        new_prompt = Prompt(image_file=self.image_file,
                            prompt_coords=promtp_coords,
                            is_pos=is_pos,
                            canvas_oval_id=canvas_oval_id,
                            aip_id=self.aip_id)
        self.prompts.append(new_prompt)

        self.append_prompt_to_csv(new_prompt) # Adding prompt to CSV

        # Appending to undo stack and clearing redo stack
        self.undo_stack.append(new_prompt)
        self.redo_stack.clear()

    def redraw_prompts(self) -> None:
        """Redraws point prompts on image canvas."""
        # Looping over prompt objects
        for prompt in self.prompts:
            self.canvas.delete(prompt.get_canvas_oval_id()) # Deleting current prompts
            x_image, y_image = prompt.get_prompt_coords() # Prompt coords on full image
            x_canvas, y_canvas = self.image_to_canvas_coords(x_image, y_image) # Converting to canvas coords
            color = "green" if prompt.get_is_pos() else "red" # Prompt color
            canvas_oval_id = self.draw_point(x_canvas, y_canvas, color) # Drawing on canvas
            prompt.set_canvas_oval_id(canvas_oval_id) # Updating canvas oval ID in Prompt class object
        
    def draw_point(self, x_c, y_c, color) -> int:
        """Draws a single point (oval) on canvas.
        
        Args:
            x_c: Prompt x-coordinate in relation to canvas.
            y_c: Prompt y-coordinate in relation to canvas.
            color: Prompt color.
        """
        r = max(4, 5 * self.scale) # Radius of point
        point_item = self.canvas.create_oval(x_c - r, y_c - r, x_c + r, y_c + r, fill=color, outline="black")
        return point_item
    
    ### Prompting utils
    def canvas_to_image_coords(self, x_canvas, y_canvas) -> tuple:
        """Converts canvas coordinates to image coordinates for full resolution image.
        
        Args:
            x_canvas: Canas x-coordinate
            y_canvas: Canvas y-coordinate
        Returns:
            Tuple containing full resolution image coordinates.   
        """
        # Getting image coords for current image
        x_image = (x_canvas - self.canvas.coords(self.container)[0]) / self.scale
        y_image = (y_canvas - self.canvas.coords(self.container)[1]) / self.scale

        # Accounting for image pyramid
        x_image *= (self.reduction**max(0, self.curr_img))
        y_image *= (self.reduction**max(0, self.curr_img))
        
        return (x_image, y_image)
    
    def image_to_canvas_coords(self, x_image, y_image) -> tuple:
        """Converts full resolution image coordinates to canvas coordinates.
        Args:
            x_image: Image x-coordinate
            y_image: Image y-coordinate
        Returns:
            Tuple containing canvas coordinates.   
        """
        # Accounting for image pyramid
        x_image /= self.reduction**max(0, self.curr_img)
        y_image /= self.reduction**max(0, self.curr_img)

        # Converting to canvas coords
        x_canvas = self.canvas.coords(self.container)[0] + (x_image * self.scale)
        y_canvas = self.canvas.coords(self.container)[1] + (y_image * self.scale)

        return (x_canvas, y_canvas)
    
    def append_prompt_to_csv(self, prompt: Prompt) -> None:
        """Adds prompt information to prompting CSV."""
        # Storing prompt info
        image_file = prompt.get_image_file()
        prompt_id = prompt.get_prompt_id()
        x_coord, y_coord = prompt.get_prompt_coords()
        is_pos = prompt.get_is_pos()
        aip_id = prompt.get_aip_id()
        canvas_oval_id = prompt.get_canvas_oval_id()

        # Adding new row with prompt info
        self.prompt_data.loc[len(self.prompt_data)] = [image_file,
                                                       prompt_id,
                                                       x_coord,
                                                       y_coord,
                                                       is_pos,
                                                       aip_id,
                                                       canvas_oval_id]
        
        self.prompt_data.to_csv(self.prompt_csv_path, index=False) # Updating prompt csv

    def remove_prompt_from_csv(self) -> None:
        """Removes last prompt row from the prompting CSV."""
        self.prompt_data.drop((len(self.prompt_data) - 1), inplace=True) # Dropping last row of prompt dataframe
        self.prompt_data.to_csv(self.prompt_csv_path, index=False) # Updating prompt csv
    
    ### Undo and redo functionality
    def undo(self, event):
        """Performs Undo operation."""
        # If undo stack is empty, do nothing
        if not self.undo_stack: return
        
        prev_prompt = self.undo_stack.pop() # Getting last event

        # Removing prompt
        canvas_oval_id = prev_prompt.get_canvas_oval_id() # Getting oval ID
        self.canvas.delete(canvas_oval_id) # Deleting prompt from canvas
        self.remove_prompt_from_csv() # Updating prompting CSV

        self.redo_stack.append(prev_prompt) # Appending to redo stack
        self.prompts.pop() # Removing from prompts list
        
        # Updating aiptasia ID
        if self.aip_id > 0 and prev_prompt.get_is_pos():
            self.aip_id -= 1

    def redo(self, event) -> None:
        """Performs Redo operation."""
        # If redo stack is empty, do nothing
        if not self.redo_stack: return

        prev_prompt = self.redo_stack.pop() # Getting previously undone prompt

        # Updating aiptasia ID and setting in Prompt object
        if prev_prompt.get_is_pos():
            self.aip_id += 1
        # prev_prompt.set_aip_id(self.aip_id) ### Do we have to do this???

        self.prompts.append(prev_prompt) # Appending to prompts list

        self.append_prompt_to_csv(prompt=prev_prompt) # Updating prompt CSV

        self.redraw_prompts() # Redrawing Prompts on canvas
        self.undo_stack.append(prev_prompt) # Appending to undo stack

    ### Baseclass overridings
    def wheel(self, event) -> None:
        """Calls namesake method in parent class and redraws prompts."""
        super().wheel(event=event) # Calling parent class wheel method
        self.redraw_prompts() # Redrawing prompts on canvas

    def destroy(self):
        """Prompting mode destructor."""
        super().destroy() # Parent class destroy method

        ### Update prompting csv here???
import logger

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

        self.__bind_events() # Binding events relevant to prompting
        
    def __bind_events(self) -> None:
        """Binding prompting events to keys."""
        # Placing prompts
        self.canvas.bind('<Button-1>', self.place_new_prompt)
        self.canvas.bind('<Button-3>', self.place_new_prompt)

        # Undoing/redoing
        self.canvas.bind('<Control-z>', self.undo)
        self.canvas.bind('<Control-Shift-KeyPress-z>', self.redo)

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
    
    def remove_prompt(self, prompt: Prompt):
        pass
    
    ### Undo and redo functionality
    def undo(self, event):
        """Performs Undo operation."""
        # If undo stack is empty, do nothing
        if not self.undo_stack: return
        
        prev_prompt = self.undo_stack.pop() # Getting last event

        # Removing prompt
        canvas_oval_id = prev_prompt.get_canvas_oval_id() # Getting oval ID
        self.canvas.delete(canvas_oval_id) # Deleting prompt from canvas

        self.redo_stack.append(prev_prompt) # Appending to redo stack
        self.prompts.pop() # Removing from prompts list
        
        # Updating aiptasia ID
        if self.aip_id > 0 and prev_prompt.get_is_pos():
            self.aip_id -= 1

    def redo(self, event) -> None:
        """Performs Redo operation."""
        print("Redo triggered")
        # If redo stack is empty, do nothing
        if not self.redo_stack: return

        prev_prompt = self.redo_stack.pop() # Previously undone prompt

        self.prompts


    ### Baseclass overridings
    def wheel(self, event) -> None:
        """Calls namesake method in parent class and redraws prompts."""
        super().wheel(event=event) # Calling parent class wheel method
        self.redraw_prompts() # Redrawing prompts on canvas
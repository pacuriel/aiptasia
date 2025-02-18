import logger

from image_canvas import ImageCanvas
from prompt import Prompt

class Prompting(ImageCanvas):
    """Class for prompting mode. Inherits from ImageCanvas."""
    def __init__(self, master, image_file):
        """Initialize the prompting mode."""
        # breakpoint()
        super().__init__(master, image_file) # Initializing base class

        # Setting prompting related variables
        self.pos_prompt_pts = []
        self.pos_prompt_items = []
        self.neg_prompt_pts = []
        self.neg_prompt_items = []
        self.prompts = []
        
        self.__bind_events() # Binding events relevant to prompting
        
        # self.__create_canvas_widgets()

    def __bind_events(self):
        """Binding prompting events to keys."""
        # Placing prompts
        self.canvas.bind('<Button-1>', self.place_new_prompt)
        self.canvas.bind('<Button-3>', self.place_new_prompt)

        # Undoing/redoing
        self.canvas.bind('<Control-z>', self.undo)

    ### Prompting
    def place_new_prompt(self, event):
        is_pos = True if event.num == 1 else False # Storing prompt type
        
        # Convert event coords to canvas coords
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)

        image_coords = self.canvas_to_image_coords(x_canvas, y_canvas) # Obtain image coordinates

        # Creating new prompt object and displaying
        new_prompt = Prompt(image_file=self.image_file,
                            prompt_coords=image_coords,
                            is_pos=is_pos)

        self.prompts.append(new_prompt)

        # Drawing prompt on image
        if is_pos:
            self.place_pos_prompt(event)
        else:
            self.place_neg_prompt(event)

        # Appending to undo stack and clearing redo stack
        self.undo_stack.append(new_prompt)
        self.redo_stack.clear()

    def draw_new_prompt(self, event): 
        pass

    def redraw_prompts(self, event):
        """Redraws point prompts on image canvas."""
        pass

    def place_pos_prompt(self, event) -> None:
        """Place a positive point prompt on the image at cursor location."""
        # Convert event coords to canvas coords
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)
        # canvas_prompt_coords = x_canvas, y_canvas
        # print("Canvas coords", canvas_prompt_coords)
        
        # Ignoring if prompt clicked
        clicked_items = self.canvas.find_overlapping(x_canvas, y_canvas, x_canvas, y_canvas) # List of clicked items
        for prompt in self.pos_prompt_items + self.neg_prompt_items:
            if prompt in clicked_items: return # Ignoring

        # Do nothing if outside of image region
        if self.outside(x_canvas, y_canvas):
            return
        
        # Convert canvas coords to full res image coords and store
        x_image, y_image = self.canvas_to_image_coords(x_canvas, y_canvas) # Obtain image coordinates
        self.pos_prompt_pts.append((x_image, y_image)) # Storing positive prompt coords relative to full image

        self.draw_point_prompts() # Drawing point prompt on canvas
    
    def place_neg_prompt(self, event) -> None:
        """Places a negative point prmpt"""
        # Convert event coords to canvas coords
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)

        # Ignoring if prompt clicked
        clicked_items = self.canvas.find_overlapping(x_canvas, y_canvas, x_canvas, y_canvas) # List of clicked items
        for prompt in self.pos_prompt_items + self.neg_prompt_items:
            if prompt in clicked_items: return # Ignoring

        # Do nothing if outside of image region
        if self.outside(x_canvas, y_canvas):
            return
        
        ### Convert to image coords and store
        x_image, y_image = self.canvas_to_image_coords(x_canvas, y_canvas) # Obtain image coordinates
        self.neg_prompt_pts.append((x_image, y_image)) # Storing negative prompt coords
        
        self.draw_point_prompts() # Drawing point prompt on canvas
    
    def draw_point_prompts(self) -> None:
        """Draws a point prompt on the canvas."""
        # Remove previous points on canvas
        for prompt in self.pos_prompt_items + self.neg_prompt_items:
            self.canvas.delete(prompt)

        # Removing all items from prompt lists
        self.pos_prompt_items.clear()
        self.neg_prompt_items.clear()

        # Redrawing positive prompts
        for x_image, y_image in self.pos_prompt_pts:
            # Converting to canvas coords
            x_canvas, y_canvas = self.image_to_canvas_coords(x_image, y_image)

            # Redrawing and storing positive prompt
            prompt_color = "green"
            prompt_item = self.draw_point(x_canvas, y_canvas, prompt_color)
            self.pos_prompt_items.append(prompt_item)

            # Making prompt clickable
            self.canvas.tag_bind(prompt_item, "<Button-1>", self.prompt_click_test)
        
        # Redrawing negative prompts
        for x_image, y_image in self.neg_prompt_pts:
            # Converting to canvas coords
            x_canvas, y_canvas = self.image_to_canvas_coords(x_image, y_image)
            
            # Redrawing and storing negative prompt
            prompt_color = "red"
            prompt_item = self.draw_point(x_canvas, y_canvas, prompt_color)
            self.neg_prompt_items.append(prompt_item)

    def draw_point_prompts_test(self) -> None:
        """Draws (or redraws) point prompts on canvas."""
        pass

    def draw_point(self, x_c, y_c, color):
        r = max(4, 5 * self.scale) # Radius of point
        point_item = self.canvas.create_oval(x_c - r, y_c - r, x_c + r, y_c + r, fill=color, outline="black")
        return point_item
    
    def canvas_to_image_coords(self, x_canvas, y_canvas):
        """Converts canvas coordinates to image coordinates for full resolution image.
        
        Args:
            x_canvas: canvas x-coordinate
            y_canvas: canvas y-coordinate
        Returns:
            Tuple containing full resolution image coordinates image coordinates.   
            """
        # Getting image coords for current image
        x_image = (x_canvas - self.canvas.coords(self.container)[0]) / self.scale
        y_image = (y_canvas - self.canvas.coords(self.container)[1]) / self.scale

        # Accounting for image pyramid
        x_image *= (self.reduction**max(0, self.curr_img))
        y_image *= (self.reduction**max(0, self.curr_img))
        
        return (x_image, y_image)
    
    def image_to_canvas_coords(self, x_image, y_image):
        """Converts full resolution image coordinates to canvas coordinates."""
        # Accounting for image pyramid
        x_image /= self.reduction**max(0, self.curr_img)
        y_image /= self.reduction**max(0, self.curr_img)

        # Converting to canvas coords
        x_canvas = self.canvas.coords(self.container)[0] + (x_image * self.scale)
        y_canvas = self.canvas.coords(self.container)[1] + (y_image * self.scale)

        return x_canvas, y_canvas
    
    def remove_prompt(self, prompt: Prompt):
        pass
    
    ### Undo and redo functionality
    def undo(self, event):
        """Performs Undo operation."""
        if not self.undo_stack: # If stack is empty
            return
        
        last_event = self.undo_stack.pop() # Getting last event

        ### Remove prompt here
        canvas_oval_id = last_event.get_canvas_oval_id() # Getting oval ID
        self.canvas.delete(canvas_oval_id) # Deleting prompt from canvas

        

        self.redo_stack.append(last_event) # Appending to redo stack

    def redo(self, event):
        """Performs Redo operation."""
        pass
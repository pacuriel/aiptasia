import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import warnings
import math
import uuid

from auto_scrollbar import AutoScrollbar
from prompt import Prompt 
"""
TODO:
- Switch ttk to tk? 
- Create class to handle user actions (and clean this class)?
- 
"""

class ImageCanvas:
    """Display and zoom image."""
    def __init__(self, master, image_file):
        """Initialize the ImageFrame."""

        self.__get_canvas_variables(image_file) # Storing variables relevant to canvas
        self.__create_canvas_widgets(master=master) # Creating canvas widget inside frame widget
        self.__bind_events() # Binding events to canvas widget
        self.__create_image_pyramid() # Creating image pyramid
        
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle((0, 0, self.imwidth, self.imheight), width=0)
        
        # self.show_image()  # show image on the canvas
        # self.canvas.focus_set()  # set focus on the canvas

    def __get_canvas_variables(self, image_file) -> None:
        """Stores class variables relevant to image canvas.
        
        Args:
            image_file: path to image to display on canvas. 
        """
        self.imscale = 1.0  # scale for the canvas image zoom, public for outer classes
        self.delta = 1.3  # zoom magnitude
        self.filter = Image.LANCZOS  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS
        # self.filter = Image.NEAREST  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS
        self.previous_state = 0  # previous state of the keyboard
        self.image_file = image_file  # image_file to the image, should be public for outer classes

        self.image = Image.open(self.image_file)  # open image, but down't load it
        self.imwidth, self.imheight = self.image.size  # public for outer classes
        self.min_side = min(self.imwidth, self.imheight)  # get the smaller image side

        # Stacks for undo/redo functionality
        self.undo_stack = []
        self.redo_stack = []
        
    def __create_canvas_widgets(self, master) -> None:
        self.main_frame = master
        self.main_window = self.main_frame.master
        self.application_title = self.main_window.title()

        # Create ImageFrame in master widget
        self.imframe = ttk.Frame(master)  # master of the ImageFrame object

        # Vertical and horizontal scrollbars for canvas
        hbar = AutoScrollbar(self.imframe, orient='horizontal')
        vbar = AutoScrollbar(self.imframe, orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')

        # Create canvas and bind it with scrollbars. Public for outer classes
        self.canvas = tk.Canvas(self.imframe, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        hbar.configure(command=self.scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.scroll_y)

    def __bind_events(self) -> None:
        """Binds user actions to events."""
        # Panning, zooming, etc.
        self.canvas.bind('<Configure>', lambda event: self.show_image())  # Canvas is resized
        self.canvas.bind('<Control-Button-1>', self.move_from)  # Remember canvas position
        self.canvas.bind('<Control-B1-Motion>',     self.move_to)  # Move canvas to the new position
        self.canvas.bind('<MouseWheel>', self.wheel)  # Zoom for Windows and MacOS, but not Linux
        # self.canvas.bind('<Button-5>',   self.wheel)  # Zoom for Linux, wheel scroll down
        # self.canvas.bind('<Button-4>',   self.wheel)  # zoom for Linux, wheel scroll up
        self.canvas.bind('<Motion>', self.__display_image_coords) ### Commented out for testing

        # Handle keystrokes in idle mode, because program slows down on a weak computers,
        # when too many key stroke events in the same time
        self.canvas.bind('<Key>', lambda event: self.canvas.after_idle(self.keystroke, event))

        # self.canvas.bind('<Button-1>', self.place_new_prompt)
        # self.canvas.bind('<Button-3>', self.place_new_prompt)
    
    def __create_image_pyramid(self) -> None:
        """Creates image pyramid and stores in class variable."""
        # Create image pyramid
        self.pyramid = [Image.open(self.image_file)]

        # Set ratio coefficient for image pyramid
        self.ratio = 1.0 #if not self.huge else max(self.imwidth, self.imheight) / self.huge_size
        self.curr_img = 0  # current image from the pyramid
        self.scale = self.imscale * self.ratio  # image pyramide scale
        self.reduction = 2  # reduction degree of image pyramid
        w, h = self.pyramid[-1].size

        min_size = 512

        # top pyramid image is around 512 pixels in size
        while w > min_size and h > min_size:  
            w /= self.reduction  # divide on reduction degree
            h /= self.reduction  # divide on reduction degree
            self.pyramid.append(self.pyramid[-1].resize((int(w), int(h)), self.filter))

    ### Prompting
    def place_new_prompt(self, event):
        is_pos = True if event.num == 1 else False
        
        # if is_pos: 
        #     aip_id = uuid.uuid4()
        #     self.aip_id = uuid.uuid4()
        # else:
        #     aip_id

        # Creating new prompt object and displaying
        new_prompt = Prompt(image_file=self.image_file,
                            event=event,
                            canvas=self.canvas,
                            is_pos=is_pos)
        
        self.prompts.append(new_prompt)

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

    def prompt_click_test(self, event):
        print("Positive prompt clicked")

    def draw_point(self, x_c, y_c, color):
        r = max(3, 5 * self.scale) # Radius of point
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

    ### Displaying image and image info
    def show_image(self):
        """Show image on the Canvas. Implements correct image zoom almost like in Google Maps."""
        box_image = self.canvas.coords(self.container)  # get image area
        box_canvas = (self.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvas.canvasy(0),
                      self.canvas.canvasx(self.canvas.winfo_width()),
                      self.canvas.canvasy(self.canvas.winfo_height()))
        box_img_int = tuple(map(int, box_image))  # convert to integer or it will not work properly
        # Get scroll region box
        box_scroll = [min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
                      max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]

        # Horizontal part of the image is in the visible area
        if  box_scroll[0] == box_canvas[0] and box_scroll[2] == box_canvas[2]:
            box_scroll[0]  = box_img_int[0]
            box_scroll[2]  = box_img_int[2]
        
        # Vertical part of the image is in the visible area
        if  box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1]  = box_img_int[1]
            box_scroll[3]  = box_img_int[3]
        
        # Convert scroll region to tuple and to integer
        self.canvas.configure(scrollregion=tuple(map(int, box_scroll)))  # set scroll region

        # get coordinates (x1,y1,x2,y2) of the image tile
        x1 = max(box_canvas[0] - box_image[0], 0)  
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = min(box_canvas[2], box_image[2]) - box_image[0]
        y2 = min(box_canvas[3], box_image[3]) - box_image[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            image = self.pyramid[max(0, self.curr_img)].crop(  # crop current img from pyramid
                                (int(x1 / self.scale), int(y1 / self.scale),
                                    int(x2 / self.scale), int(y2 / self.scale)))

            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1)), self.filter))
            imageid = self.canvas.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
        
    def redraw_figures(self):
        """Dummy function to redraw figures in the children classes."""
        pass
        
    def grid(self, **kw):
        """Put CanvasImage widget on the master widget."""
        self.imframe.grid(**kw)  # place CanvasImage widget on the grid
        self.imframe.grid(sticky='nswe')  # Make frame container sticky
        self.imframe.rowconfigure(0, weight=1)  # Make canvas expandable
        self.imframe.columnconfigure(0, weight=1)
    
    def __display_image_coords(self, event) -> None:
        """Displays coordinates of cursor relevant to image at top of main window.
        
        Args: 
            event: Tkinter user-triggered event
        """
        # Convert event to canvas coordinates
        x_canvas = self.canvas.canvasx(event.x)
        y_canvas = self.canvas.canvasy(event.y)

        # Checks if cursor is outside image area
        if self.outside(x_canvas, y_canvas):
            self.main_window.title(self.application_title)
            return
        
        # Obtain current image coordinates
        x_image, y_image = self.canvas_to_image_coords(x_canvas, y_canvas)

        # Update window title
        self.main_window.title(self.application_title + f" - Coordinates: ({int(x_image)}, {int(y_image)})")

    ### Scrolling
    def scroll_x(self, *args, **kwargs):
        """Scroll canvas horizontally and redraw the image."""
        self.canvas.xview(*args)  # scroll horizontally
        self.show_image()  # redraw the image

    def scroll_y(self, *args, **kwargs):
        """Scroll canvas vertically and redraw the image."""
        self.canvas.yview(*args)  # scroll vertically
        self.show_image()  # redraw the image

    def keystroke(self, event):
        """Scrolling with the keyboard.
            Independent from the language of the keyboard, CapsLock, <Ctrl>+<key>, etc."""
        if event.state - self.previous_state == 4:  # means that the Control key is pressed
            pass  # do nothing if Control key is pressed
        else:
            self.previous_state = event.state  # remember the last keystroke state
            # Up, Down, Left, Right keystrokes
            if event.keycode in [68, 39, 102]:  # scroll right: keys 'D', 'Right' or 'Numpad-6'
                self.scroll_x('scroll',  1, 'unit', event=event)
            elif event.keycode in [65, 37, 100]:  # scroll left: keys 'A', 'Left' or 'Numpad-4'
                self.scroll_x('scroll', -1, 'unit', event=event)
            elif event.keycode in [87, 38, 104]:  # scroll up: keys 'W', 'Up' or 'Numpad-8'
                self.scroll_y('scroll', -1, 'unit', event=event)
            elif event.keycode in [83, 40, 98]:  # scroll down: keys 'S', 'Down' or 'Numpad-2'
                self.scroll_y('scroll',  1, 'unit', event=event)

    ### Panning
    def move_from(self, event):
        """Remember previous coordinates for scrolling with the mouse """
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        """Drag (move) canvas to the new position."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # zoom tile and show it on the canvas

    ### Zooming
    def wheel(self, event):
        """Zoom with mouse wheel."""
        x = self.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
        y = self.canvas.canvasy(event.y)
        if self.outside(x, y): return  # zoom only inside image area
        scale = 1.0

        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down, smaller
            if round(self.min_side * self.imscale) < 250: return  # image is less than 250 pixels
            self.imscale /= self.delta
            scale        /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up, bigger
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height()) >> 1
            # if i < self.imscale: return  # 1 pixel is bigger than the visible area
            if self.imscale > 12: return
            self.imscale *= self.delta
            scale        *= self.delta

        # Take appropriate image from the pyramid
        k = self.imscale * self.ratio  # temporary coefficient
        self.curr_img = min((-1) * int(math.log(k, self.reduction)), len(self.pyramid) - 1)
        self.scale = k * math.pow(self.reduction, max(0, self.curr_img))

        self.canvas.scale('all', x, y, scale, scale)  # rescale all objects

        # Redraw some figures before showing image on the screen
        self.redraw_figures()  # method for child classes
        self.show_image() # Displaying image
        self.draw_point_prompts() # Redrawing point prompts

    def crop(self, bbox):
        """Crop rectangle from the image and return it."""
        return self.pyramid[0].crop(bbox)

    ### Helper functions
    def outside(self, x, y):
        """Checks if the point (x,y) is outside the image area."""
        bbox = self.canvas.coords(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            return False  # point (x,y) is inside the image area
        else:
            return True  # point (x,y) is outside the image area
    
    def destroy(self):
        """ImageFrame destructor."""
        self.image.close()
        for img in self.pyramid:
            img.close()
        # map(lambda i: i.close, self.pyramid)  # close all pyramid images
        del self.pyramid[:]  # delete pyramid list
        del self.pyramid  # delete pyramid variable
        self.canvas.destroy()
        self.imframe.destroy()

    ### Are the below two functions necessary? 
    def pack(self, **kw):
        """Exception: cannot use pack with this widget."""
        raise Exception('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        """Exception: cannot use place with this widget."""
        raise Exception('Cannot use place with the widget ' + self.__class__.__name__)

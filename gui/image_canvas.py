"""
Code adapted from: https://github.com/foobar167/junkyard/tree/master/manual_image_annotation1
"""

# Importing packages
import tkinter as tk
from PIL import Image, ImageTk

# Helper classes
# from auto_scrollbar import AutoScrollbar

# Class to display canvas widget on parent (MainWindow: tk.Frame)
class ImageCanvas:

    def __init__(self, master: tk.Tk, image_file: str):
        self.master = master
        self.image_file = image_file

        ### Relevant app variables
        self.__delta = 1.25 # Zoom magnitude

        # Filter to apply when displaying image
        # self.__filter = Image.NEAREST # origianl
        self.__filter = Image.LANCZOS # anti-aliasing

        self.__previous_state = 0 # Previous state of the key presses

        self.__create_canvas_widget() # Creating canvas widget and key bindings

        # Loading image and storing relevant details
        self.pil_image = Image.open(self.image_file) # Opening file as pil image
        self.img_width, self.img_height = self.pil_image.size # Image height/width
        self.__min_side = min(self.img_height, self.img_width) # Smallest side of image

        ### Setup image pyramid here?

        # Creating rectangle container to store/track image on Canvas
        self.img_container = self.canvas.create_rectangle(0, 0, self.img_width, self.img_height, width=0)

        self.__display_image() # Displaying image
        self.canvas.focus_set() # Set keyboard focus on canvas object

    # Creates canvas widget and binds keys to events
    def __create_canvas_widget(self) -> None:
        # Creating Canvas and binding keys to events
        self.canvas = tk.Canvas(self.master, background="gray12", cursor="spider", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nswe') # Displaying Canvas in grid of parent
        self.canvas.update() # Updating canvas
        self.__bind_events() # Calling function to bind keys to events

    ### Event bindings and associated functions
    # Binds keys to events
    def __bind_events(self) -> None:
            self.canvas.bind('<Button-1>', self.button_1_test)
            self.canvas.bind('<MouseWheel>', self.zoom_wheel) # Mouse wheel for zooming

    # Function to test key bidnings
    def button_1_test(self, event) -> None:
        print(f"Button 1 (LMB) pressed at {event.x, event.y}") # Sanity check
        self.__old_event = event # Updating previous event

    # Zooms at current cursor location inside image
    def zoom_wheel(self, event):

        pass

    def outside_img_region(self, event_x, event_y):
        img_area = self.canvas.coords(self.container)
        pass

    # Sets up image pyramid for more efficient memory utilization
    def __setup_image_pyramid(self):
        pass

    # Displays image on canvas
    def __display_image(self) -> None:
        # Tuple of image coordinates (top-left, bottom-right)
        img_coords_int = tuple(map(int, self.canvas.coords(self.img_container))) 

        # Visible area of canvas in canvas coordinates
        canvas_coords = (self.canvas.canvasx(0),
                         self.canvas.canvasy(0),
                         self.canvas.canvasx(self.canvas.winfo_width()),
                         self.canvas.canvasy(self.canvas.winfo_height()))

        # Scrollable region (smallest area that contains both image and visible canvas area)
        scroll_region = list(min(img_coords_int[i], canvas_coords[i]) for i in range(len(canvas_coords)))

        # Confirming horizontal/vertical parts of image are in visible canvasarea
        if scroll_region[0] == canvas_coords[0] and scroll_region[2] == canvas_coords[2]: #horizontal
            scroll_region[0] = img_coords_int[0]
            scroll_region[2] = img_coords_int[2]

        if scroll_region[1] == canvas_coords[1] and scroll_region[3] == canvas_coords[3]: #vertical
            scroll_region[1] = img_coords_int[1]
            scroll_region[3] = img_coords_int[3]

        scroll_region = tuple(map(int, scroll_region)) # Converting scroll region list to tuple

        self.canvas.configure(scrollregion=scroll_region) # Setting scrollable region in canvas

        # Computing visible portion of the image within the canvas
        x0 = max(canvas_coords[0] - img_coords_int[0], 0)
        y0 = max(canvas_coords[1] - img_coords_int[1], 0)
        x1 = min(canvas_coords[2], img_coords_int[2]) - img_coords_int[0]
        y1 = min(canvas_coords[3], img_coords_int[3]) - img_coords_int[1]

        # Displaying image if in visible area
        if int(x1 - x0) > 0 and int(y1 - y0) > 0:
            ### Call pyramid if using here
            img = self.pil_image # Storing image to display
            tk_image = ImageTk.PhotoImage(image=img) # Storing PIL Tk Image

            # Drawing image on canvas
            canvas_image_id = self.canvas.create_image(max(canvas_coords[0], img_coords_int[0]),
                                                       max(canvas_coords[1], img_coords_int[1]),
                                                       anchor='nw', # Note: could also use 'center' if above coords are halved
                                                       image=tk_image)
            
            self.canvas.lower(canvas_image_id) # Setting image as background (Should we do this???)

            
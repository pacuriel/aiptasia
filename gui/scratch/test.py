import tkinter as tk
from tkinter import ttk
import sys

root = tk.Tk()

#displaying an image in GUI
# canvas = tk.Canvas(root, width=1280, height=720)
# canvas.pack()
# img_file = "segmented_cat_5.png"
# img = tk.PhotoImage(file=img_file)
# canvas.create_image(10,10, anchor=tk.NW, image=img)
# root.mainloop()

#building basic hello world GUI
# frame = ttk.Frame(root, padding=50)
# frame.grid()
# ttk.Label(frame, text="Hello world", font=30).grid(column=0, row=0)
# ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()

# from tkinter import *

# class Board(Canvas):

#     def __init__(self, master=None, **kwargs):
#         Canvas.__init__(self, master, **kwargs)
#         self.bind('<Button-1>', self.on_click)
#         self.dots = []

#     def on_click(self, event):
#         r = 5
#         x, y = event.x, event.y
#         self.dots.append(self.create_oval(x-r, y-r, x+r, y+r))

# root = Tk()
# Board(root).pack()
# root.mainloop()

"""
# line drawing with two right mouse clicks - start and end points
def start_line(self, event):
    if self.line_start is None:
        self.line_start = (event.x, event.y)
    else:
        end_point_x, end_point_y = event.x, event.y
        self.canvas.create_line(self.line_start[0], self.line_start[1], end_point_x, end_point_y, fill='red')
        line_start = tuple([self.line_start[0], self.line_start[1]])
        line_end = tuple([end_point_x, end_point_y])
        line_coords.append([line_start, line_end])
        self.line_start = None

    # LINE COORDINATE TRANSFORMATION
    def transform_line_coords(i):
        original_coords = line_coords[i] # original coordinates
        homogeneous_coords = np.column_stack((np.array(original_coords), np.ones(len(original_coords))))
        transformation_matrix = self.mat_affine.T
        transformed_coords = np.dot(homogeneous_coords, transformation_matrix)
        cartesian = transformed_coords[:, :2]
        start_point = tuple([cartesian[0,0], cartesian[0,1]])
        end_point = tuple([cartesian[1,0], cartesian[1,1]])
        return [start_point, end_point]
            
    # overwrite original line coordinates [[(x1_start,y1_start), (x1_end,y1_end)], [(x2_start,y2_start), (x2_end,y2_end)]...], 
    # with transformed cordinates.
    global line_coords
    line_coords = [transform_line_coords(i) for i in range(0, len(line_coords))]
    
    # re-draw the lines defined in the global list of lines
    def draw_line(i):
        x1 = line_coords[i][0][0]
        y1 = line_coords[i][0][1]
        x2 = line_coords[i][1][0]
        y2 = line_coords[i][1][1]
        self.canvas.create_line(x1,y1,x2,y2, fill='red')
    
    draw_lines = [draw_line(i) for i in range(0, len(line_coords))]
    """

class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)

        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="Exit", underline=1, command=self.exit_app)

    def exit_app(self):
        sys.exit(0)

"""
box_image = self.canvas.coords(self.img_container)  # get image area
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

        # show image if it in the visible area
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  
            # image = self.__pyramid[max(0, self.__curr_img)].crop(  # crop current img from pyramid
            #                     (int(x1 / self.__scale), int(y1 / self.__scale),
            #                         int(x2 / self.__scale), int(y2 / self.__scale)))
            image = self.pil_image
            tk_image = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1)), self.__filter))
            imageid = self.canvas.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=tk_image)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.tk_image = tk_image  # keep an extra reference to prevent garbage-collection
"""

import tkinter as tk

def start_drag(event):
    canvas.scan_mark(event.x, event.y)

def drag(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create some items on the canvas
canvas.create_rectangle(50, 50, 150, 150, fill="blue")
canvas.create_oval(200, 200, 300, 300, fill="red")

# Bind mouse events for dragging
canvas.bind("<ButtonPress-1>", start_drag)
canvas.bind("<B1-Motion>", drag)

root.mainloop()
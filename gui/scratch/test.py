import tkinter as tk
from tkinter import ttk

root = tk.Tk()

#displaying an image in GUI
canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()
img_file = "CC7.265.1.2023.10.13.png"
img = tk.PhotoImage(file=img_file)
canvas.create_image(10,10, anchor=tk.NW, image=img)
root.mainloop()

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
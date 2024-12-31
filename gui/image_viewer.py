"""
Code adapted from PythonImageViewer on GH: https://github.com/ImagingSolution/PythonImageViewer
"""
import tkinter as tk            
from tkinter import filedialog, simpledialog  
from PIL import Image, ImageTk  
import math                    
import numpy as np              
import os
import matplotlib.pyplot as plt

line_coords = []

"""
Current setup idea/modifications: 
- Pan: hold mouse wheel and drag cursor
- Zoom: spin mouse wheel
- Positive point prompt: right click (Button-3)
- Negative point prompt: left click (Button-1)

Thought process for pos/neg prompt buttons: 
- Most prompts for our case will be the negative case, likely circling around each aiptasia oral disk
- Left click seems more stable (for me)
- The right click for positive point prompts will not have to be as accurate
"""

class ImageViewer(tk.Frame):
    
    # Initializing and setting window properties 
    def __init__(self, master=None):
        super().__init__(master)
        self.master.geometry("600x400") 
        self.pil_image = None 
        self.line_start = None
        self.my_title = "PyPointCounter"
        
        self.create_menu()
        self.create_widget()

        self.reset_transform()
    
    # Menu bar
    def create_menu(self):
        self.menu_bar = tk.Menu(self) # Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff = tk.OFF)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Image", command = self.menu_open_clicked)
        self.master.config(menu=self.menu_bar)

    def menu_open_clicked(self, event=None):
        filename = tk.filedialog.askopenfilename(
            filetypes = [("Image file", ".bmp .png .jpg .tif"), ("Bitmap", ".bmp"), ("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif") ],
            initialdir = os.getcwd()
            )

        self.set_image(filename)
    
    # Create canvas
    def create_widget(self):
        self.canvas = tk.Canvas(self.master, background="black")
        self.canvas.pack(expand=True,  fill=tk.BOTH)
        
        # bindings
        self.master.bind("<Button-1>", self.mouse_down_left) # MouseDown
        self.master.bind("<B1-Motion>", self.mouse_move_left) # MouseDrag
        self.master.bind("<MouseWheel>", self.mouse_wheel) # MouseWheel
        self.canvas.bind("<Button-3>", self.start_line) # Right mouse button for drawing lines
        self.canvas.bind("<Button-2>", self.mouse_wheel_button) #Mouse wheel button
    
    # Load image file
    def set_image(self, filename):
        if not filename:
            return
        self.pil_image = Image.open(filename)
        self.draw_image(self.pil_image)
        os.chdir(os.path.dirname(filename))
    
    ### User actions
    def mouse_down_left(self, event):
        self.__old_event = event

    def mouse_move_left(self, event):
        if (self.pil_image == None):
            return
        self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image()
        self.__old_event = event
    
    # zoom mouse wheel action
    def mouse_wheel(self, event):
        if self.pil_image == None:
            return
        if (event.delta > 0):
            self.scale_at(1.25, event.x, event.y)
        else:
            self.scale_at(0.8, event.x, event.y)
        self.redraw_image()

    # Test function for when mouse wheel is clicked
    def mouse_wheel_button(self, event): 
        print("Mouse wheel button clicked!")

    def reset_transform(self):
        self.mat_affine = np.eye(3)
    
    # Pan
    def translate(self, offset_x, offset_y):
        mat = np.eye(3)
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)
        self.mat_affine = np.dot(mat, self.mat_affine)
    
    # Zoom base function
    def scale(self, scale:float):
        mat = np.eye(3)
        mat[0, 0] = scale
        mat[1, 1] = scale
        self.mat_affine = np.dot(mat, self.mat_affine)
    
    # FUnction to zoom at cursor location
    def scale_at(self, scale:float, cx:float, cy:float):
        self.translate(-cx, -cy)
        self.scale(scale)
        self.translate(cx, cy)
    
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

    # Update display according to user actions
    def draw_image(self, pil_image):
        
        self.canvas.delete('all') # remove previously drawn lines
        
        # IMAGE TRANSFORMATION
        if pil_image == None:
            return

        self.pil_image = pil_image

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        mat_inv = np.linalg.inv(self.mat_affine)

        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
            )

        dst = self.pil_image.transform((canvas_width, canvas_height),Image.AFFINE,affine_inv,Image.NEAREST)
        im = ImageTk.PhotoImage(image=dst)
        item = self.canvas.create_image(0, 0,anchor='nw',image=im)
        self.image = im    
        
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
        
    def redraw_image(self):
        if self.pil_image == None:
            return
        
        self.draw_image(self.pil_image)

def main():
    root = tk.Tk()
    app = ImageViewer(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()
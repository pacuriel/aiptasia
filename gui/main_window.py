import tkinter as tk

from image_canvas import ImageCanvas

VERSION_NUMBER = 0.1

# Dictionaries to store prompt image coords. Format = {'file_name': [(pixel_coords_tuple)]}
pos_prompt_coords = dict() # Positive pixel coords (pixels to segment)
neg_prompt_coords = dict() # Negative pixel coords (pixels to ignore)

"""
Current setup idea/modifications: 
- Pan: hold ctrl and LMB and drag cursor
- Zoom: spin mouse wheel
- Positive point prompt: right click (Button-3)
- Negative point prompt: left click (Button-1)

Thought process for pos/neg prompt buttons: 
- Most prompts for our case will be the negative case, likely circling around each aiptasia oral disk
- Left click seems more stable (for me)
- The right click for positive point prompts will not have to be as accurate

Other possible features: 
- Look into adding a second layer for overlapping/touching aiptasia
- Set max zoom out such that entire image fits and is viewable (i.e. don't allow for infinite zoom out; seems pointless) 
"""

# Class representing main window of image viewer application
class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master) # Initialize main window frame
        self.master.title(f'Image Viewer App v{VERSION_NUMBER}') # Window title
        self.master.geometry('800x600')  # Size of the main window

        # Making the ImageCanvas widget adjust to window size
        self.master.rowconfigure(0, weight=1)  
        self.master.columnconfigure(0, weight=1)

        # image_file = "segmented_cat_5.png"
        image_file = "CC7.265.1.2023.10.13.png" # Test image to view

        canvas = ImageCanvas(self.master, image_file)  # Creating Canvas widget (aka where the magic happens)
        # canvas.grid(row=0, column=0)  # Displaying widget


def main(): 
    root = tk.Tk()
    root.state("zoomed")
    root.title("Test image viewer app")
 
    image_viewer = MainWindow(master=root)
    image_viewer.mainloop()


if __name__ == "__main__": 
    main()
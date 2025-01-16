# Python packages
import tkinter as tk
from PIL import Image, ImageTk
import os

# Helper classes
# from image_transformations import ImageTransformations
from test_user_actions import UserActions

class TestApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master.geometry("600x400")

        self.user_actions = UserActions(master=self.master) # Creating UserActions object

        self.create_canvas_widget() # Creating canvas widget

        self.image_file = "segmented_cat_5.png" # Test file to use

        self.set_image(img_file=self.image_file)

        # breakpoint()


    # Creates canvas widget and binds button presses
    def create_canvas_widget(self) -> None:
        # Creating Canvas object (or widget) as a child of main Tkinter window (self.master)  
        self.canvas = tk.Canvas(self.master, background="black", cursor="spider")
        
        # Packing canvas widget inside of its parent container
        # expand: allows canvas to resize with window
        # fill: specifies canvas should fill both H/V directions
        self.canvas.pack(expand=True, fill=tk.BOTH) 

        self.event_bindings() # Binding user actions to events

    # Binds user actions to events
    def event_bindings(self) -> None:
        # Control + LMB pressed
        self.canvas.bind("<Control-Button-1>", self.user_actions.ctrl_lmb_down)

        # Control + LMB pressed and held with motion 
        self.canvas.bind("<Control-B1-Motion>", self.user_actions.ctrl_lmb_pan)    

    # Sets and displays image given a file path (or name if in cwd)
    def set_image(self, img_file):
        if not img_file:
            return
        
        self.pil_image = Image.open(img_file) # Opening image file as PIL image
        self.user_actions.set_image(self.pil_image) # Setting PIL image in user actions object

        self.display_image(self.pil_image) # Displaying image on screen
        
        ### Change current working directory???
        # os.chdir(os.path.dirname(img_file))

     # Displays a given PIL image 
    def display_image(self, pil_image):
        # Resetting the canvas by deleting existing elements
        self.canvas.delete("all") 

        if pil_image == None:
            return
        
        self.pil_image = pil_image

        self.canvas.update() # Updating the GUI/app

        # Storing canvas width/height
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        tk_img = ImageTk.PhotoImage(image=self.pil_image) # Creating Tkinter image object
        self.tk_img = tk_img

        self.canvas.create_image((canvas_width / 2), (canvas_height / 2), anchor='center', image=tk_img) # Drawing the image



        


def main():

    root = tk.Tk()
    root.state("zoomed")
    root.title("Test image viewer app")
    
    app = TestApp(master=root)
    app.mainloop() # Running app

if __name__ == "__main__":
    main()
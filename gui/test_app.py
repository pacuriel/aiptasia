import tkinter as tk
from PIL import Image, ImageTk
import os

class TestApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master.geometry("600x400")

        self.create_canvas_widget()

        self.image_file = "segmented_cat_5.png" # Test file to use

        self.set_image(img_file=self.image_file)

        # breakpoint()

    # Creating canvas widget
    def create_canvas_widget(self):
        self.canvas = tk.Canvas(self.master, background="black", cursor="spider")
        self.canvas.pack(expand=True, fill=tk.BOTH)

    def set_image(self, img_file):
        if not img_file:
            return
        
        self.pil_image = Image.open(img_file)

        self.display_image(self.pil_image)
        
        ### Change current working directory???
        # os.chdir(os.path.dirname(img_file))


    def display_image(self, pil_image):
        
        self.canvas.delete("all")

        if pil_image == None:
            return
        
        self.pil_image = pil_image

        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # print(canvas_width, canvas_height)

        tk_img = ImageTk.PhotoImage(image=self.pil_image) # Creating Tkinter image object
        self.tk_img = tk_img

        self.canvas.create_image((canvas_width / 2), (canvas_height / 2), anchor='center', image=tk_img) # Drawing the image
        # breakpoint()



        


def main():

    root = tk.Tk()
    root.state("zoomed")
    root.title("Test image viewer app")
    
    app = TestApp(master=root)
    app.mainloop() # Running app

if __name__ == "__main__":
    main()
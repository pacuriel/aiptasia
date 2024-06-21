from tkinter import *
from tkinter import ttk

root = Tk()

#displaying an image in GUI
canvas = Canvas(root, width=1280, height=720)
canvas.pack()
img_file = "C:\\Users\\giant\\Desktop\\aiptasia\\data\\2023.12.8\\CC7.290.1_2023.12.8.png"
img = PhotoImage(file=img_file)
canvas.create_image(20,20, anchor=NW, image=img)
root.mainloop()

#building basic hello world GUI
# frame = ttk.Frame(root, padding=50)
# frame.grid()
# ttk.Label(frame, text="Hey cutie", font=30).grid(column=0, row=0)
# ttk.Button(frame, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()
import easygui #to open the filebox

import os
import tkinter as tk
from tkinter import ttk
import cv2
import matplotlib.pyplot as plt

from Cartoonifiers import base as bc
class App():
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('400x400')
        self.window.title('Cartoonify Your Image!')
        self.window.configure(background='white')
        ttk.Label(self.window, text="Cartoonifier",
                  background='white',
                  foreground="black",
                  font=("Times New Roman", 15)).grid(row=0, column=1)

        ttk.Label(self.window, text="Select Cartoonifier :",
                  font=("Times New Roman", 10)).grid(column=0,
                                                     row=5, padx=10, pady=25)

        # Combobox creation
        n = tk.StringVar()
        self.cartoonifier_selector = ttk.Combobox(self.window, width=27, textvariable=n)
        self.cartoonifier_selector['values'] = ('Basic',
                                           'Blur')
        self.cartoonifier_selector.grid(column=1, row=5)
        self.cartoonifier_selector.current(1)

        self.save_button = tk.Button(self.window, text="Save cartoon image", padx=40, pady=5)
        self.save_button.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
        self.save_button.grid_forget()
        self.save_button.bind('<Button-1>', self.save)

        self.upload = tk.Button(self.window, text="Cartoonify", padx = 10, pady = 5)
        self.upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
        self.upload.grid(column=1, row=7)
        self.upload.bind('<Button-1>', self.cartoonify_image)

        self.caroonified_image = None
        self.image_path = None

    def cartoonify_image(self, event):
        image_path = easygui.fileopenbox()
        self.image_path = image_path

        cartoonifier = bc.BaseCartoon(self.image_path)
        current_value = self.cartoonifier_selector.get()
        if current_value == 'Basic':
            print("Using Basic")
            cartoon_image = cartoonifier.use_basic_cartoon()
        elif current_value == 'Blur':
            print("Using Blur")
            cartoon_image = cartoonifier.use_blur_to_cartoonify()
        else:
            print("Unable to locate cartoonifier")

        plt.figure()
        plt.imshow(cartoon_image)
        plt.show()

        self.caroonified_image = cartoon_image

        self.save_button.grid(column=1, row=9)

    def save(self, event):
        # saving an image using imwrite()
        newName = os.path.splitext(self.image_path)[0] + "_cartoonified"
        path1 = os.path.dirname(self.image_path)
        extension = os.path.splitext(self.image_path)[1]
        path = os.path.join(path1, newName + extension)
        cv2.imwrite(path, cv2.cvtColor(self.caroonified_image, cv2.COLOR_RGB2BGR))
        I = "Image saved by name " + newName + " at " + path
        tk.messagebox.showinfo(title=None, message=I)

if __name__ == "__main__":
    App().window.mainloop()




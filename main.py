import easygui
import os
import tkinter as tk
from tkinter import ttk
import cv2
import matplotlib.pyplot as plt
import magic

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
        self.upload.bind('<Button-1>', self.cartoonify_button_action)

        self.caroonified_item = None
        self.file_path = None
        self.cartoonifier = bc.BaseCartoon()

    def cartoonify_image(self, image):
        current_value = self.cartoonifier_selector.get()
        if current_value == 'Basic':
            cartoon_image = self.cartoonifier.use_basic_cartoon(image)
        elif current_value == 'Blur':
            cartoon_image = self.cartoonifier.use_blur_to_cartoonify(image)
        else:
            print("Unable to locate cartoonifier")
        return cartoon_image
    def cartoonify_button_action(self, event):
        video_name = easygui.fileopenbox()
        self.file_path = video_name

        file_type = magic.from_buffer(open(video_name, "rb").read(2048)).split(",")[0]
        if "image" in file_type:
            img = self.cartoonifier.get_image(video_name)
            cartoon_image = self.cartoonify_image(img)

            plt.figure()
            plt.imshow(cartoon_image)
            plt.show()

            self.caroonified_item = cartoon_image

            self.save_button.grid(column=1, row=9)
        else:
            vidcap = self.cartoonifier.get_video(video_name)
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            success, image = vidcap.read()

            newName = os.path.splitext(self.file_path)[0] + "_cartoonified"
            path1 = os.path.dirname(self.file_path)
            extension = os.path.splitext(self.file_path)[1]
            video_name = os.path.join(path1, newName + extension)
            image_folder = os.path.join(path1, newName + "_frames")
            count = 0
            os.mkdir(image_folder)
            while success:
                cartoon_image = self.cartoonify_image(image)
                name = os.path.join(image_folder, "frame_" + str(count) + ".png")
                cv2.imwrite(name, cartoon_image)
                success, image = vidcap.read()
                count += 1

            images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
            frame = cv2.imread(os.path.join(image_folder, images[0]))
            height, width, layers = frame.shape

            cartoon_video = cv2.VideoWriter(video_name, 0, fps, (width, height))

            for image in images:
                cartoon_video.write(cv2.imread(os.path.join(image_folder, image)))

            cv2.destroyAllWindows()
            cartoon_video.release()

    def save(self, event):
        # saving an image using imwrite()
        newName = os.path.splitext(self.file_path)[0] + "_cartoonified"
        path1 = os.path.dirname(self.file_path)
        extension = os.path.splitext(self.file_path)[1]
        path = os.path.join(path1, newName + extension)
        cv2.imwrite(path, cv2.cvtColor(self.caroonified_item, cv2.COLOR_RGB2BGR))
        I = "Image saved by name " + newName + " at " + path
        tk.messagebox.showinfo(title=None, message=I)

if __name__ == "__main__":
    App().window.mainloop()




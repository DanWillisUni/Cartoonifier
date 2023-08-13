import easygui
import tkinter as tk
from tkinter import ttk
import magic
import shutil
import datetime

from utils import *
from varibles import *
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

        self.upload = tk.Button(self.window, text="Cartoonify", padx = 10, pady = 5)
        self.upload.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
        self.upload.grid(column=1, row=7)
        self.upload.bind('<Button-1>', self.cartoonify_button_action)

        self.cartoonifier = bc.BaseCartoon()

    def cartoonify_image(self, image):
        current_value = self.cartoonifier_selector.get()
        if current_value == 'Basic':
            cartoon_image = self.cartoonifier.use_basic_cartoon(image)
        elif current_value == 'Blur':
            cartoon_image = self.cartoonifier.use_blur_to_cartoonify(image)
        else:
            print("Unable to locate cartoonifier")
            sys.exit()
        return cartoon_image

    def generate_frame_dir(self, file_path):
        ct = datetime.datetime.now()
        print("current time:-", ct)
        print("Generating frames...")
        vidcap = cv2.VideoCapture(file_path)
        fps = round(vidcap.get(cv2.CAP_PROP_FPS))
        frame_count = round(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(frame_count)
        number_of_digits_in_frames = len(str(frame_count))
        print("Original Video FPS: " + str(fps))
        saving_fps = min(fps, KPS)
        print("Saving Video FPS: "+str(saving_fps))
        hop = round(fps / saving_fps)
        success, image = vidcap.read()
        image_folder = get_new_frame_dir(file_path)
        count = 0
        os.mkdir(image_folder)
        while success:
            if count % hop == 0:
                cartoon_image = self.cartoonify_image(image)
                name = os.path.join(image_folder, "frame_" + ("{:0"+ str(number_of_digits_in_frames) +"d}").format(count) + ".png")
                cv2.imwrite(name, cartoon_image)
            if count != 0 and count % round(frame_count/PERCENT_INCREMENTS) == 0:
                print(str(round(100 * count/frame_count)) + "%")
            success, image = vidcap.read()
            count += 1
        ct = datetime.datetime.now()
        print("current time:-", ct)
        return saving_fps

    def generate_video_from_frames(self, fps, file_path):
        image_folder = get_new_frame_dir(file_path)
        images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
        frame = cv2.imread(os.path.join(image_folder, images[0]))
        height, width, layers = frame.shape

        save_path = get_new_save_path(file_path)
        cartoon_video = cv2.VideoWriter(save_path, 0, fps, (width, height))

        for image in images:
            cartoon_video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        cartoon_video.release()
        if REMOVE_FRAME_DIR:
            shutil.rmtree(image_folder)
    def cartoonify_button_action(self, event):
        file_path = easygui.fileopenbox()
        file_type = magic.from_buffer(open(file_path, "rb").read(2048)).split(",")[0]

        if "image" in file_type:
            img = get_image(file_path) # Get image
            cartoon_image = self.cartoonify_image(img) # Cartoonify
            display_image(cartoon_image) # Display image preview
            self.save_image(cartoon_image, file_path) # Save image
        else: # TODO better check here
            saving_fps = self.generate_frame_dir(file_path)
            self.generate_video_from_frames(saving_fps, file_path)
    def save_image(self, img, file_path):
        path = get_new_save_path(file_path)
        cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        tk.messagebox.showinfo(title=None, message="Image saved: " + path)

if __name__ == "__main__":
    App().window.mainloop()
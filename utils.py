import cv2
import os
import matplotlib.pyplot as plt
def display_image(img):
    plt.figure()
    plt.imshow(img)
    plt.show()
def get_image(self, image_path):
    # read the image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # confirm that image is chosen
    if original_image is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()

    return cv2.resize(original_image, (960, 540))

def get_new_save_path(file_path):
    newName = os.path.splitext(file_path)[0] + "_cartoonified"
    path1 = os.path.dirname(file_path)
    extension = os.path.splitext(file_path)[1]
    path = os.path.join(path1, newName + extension)
    return path

def get_new_frame_dir(file_path):
    newName = os.path.splitext(file_path)[0] + "_cartoonified"
    path1 = os.path.dirname(file_path)
    image_folder = os.path.join(path1, newName + "_frames")
    return image_folder
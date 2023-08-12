import cv2
from Cartoonifiers import blur
from Cartoonifiers import basic_cartoonify

class BaseCartoon():
    def get_image(self, image_path):
        # read the image
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        # print(image)  # image is stored in form of numbers

        # confirm that image is chosen
        if original_image is None:
            print("Can not find any image. Choose appropriate file")
            sys.exit()

        return cv2.resize(original_image, (960, 540))

    def get_video(self, video_path):
        return cv2.VideoCapture(video_path)

    def use_blur_to_cartoonify(self, image):
        return blur.cartoonify(image)
    def use_basic_cartoon(self, image):
        return basic_cartoonify.cartoonify(image)
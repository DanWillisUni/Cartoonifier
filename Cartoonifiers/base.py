import cv2
from Cartoonifiers import blur
from Cartoonifiers import basic_cartoonify

class BaseCartoon():
    def __init__(self, image_path):
        self.base_image = self.get_image(image_path)

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

    def use_blur_to_cartoonify(self):
        return blur.cartoonify(self.base_image)
    def use_basic_cartoon(self):
        return basic_cartoonify.cartoonify(self.base_image)
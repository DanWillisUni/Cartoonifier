import cv2
from Cartoonifiers import blur
from Cartoonifiers import basic_cartoonify

class BaseCartoon():


    def use_blur_to_cartoonify(self, image):
        return blur.cartoonify(image)
    def use_basic_cartoon(self, image):
        return basic_cartoonify.cartoonify(image)
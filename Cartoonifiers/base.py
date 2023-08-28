import cv2
from Cartoonifiers import blur
from Cartoonifiers import basic_cartoonify

class BaseCartoon():
    def use_blur_cartoon_calculated(self, image, how_cartoonified):
        return self.use_blur_to_cartoonify(image)
    def use_blur_to_cartoonify(self, image):
        return blur.cartoonify(image)
    def use_basic_cartoon_calculated(self, image, how_cartoonified):
        BLUR_KERNAL_SIZE, THRESHOLD, THRESHOLD_BLOCK_SIZE, THRESHOLD_BLUR, BILATERAL_D = basic_cartoonify.calculate_perfect_settings(how_cartoonified)
        return basic_cartoonify.cartoonify(image, BLUR_KERNAL_SIZE, THRESHOLD, THRESHOLD_BLOCK_SIZE, THRESHOLD_BLUR, BILATERAL_D)
    def use_basic_cartoon(self, image):
        return basic_cartoonify.cartoonify(image)
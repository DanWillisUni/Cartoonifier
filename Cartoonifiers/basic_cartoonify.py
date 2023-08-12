import cv2 #for image processing

import matplotlib.pyplot as plt
from tkinter import *

def cartoonify(img):
	# converting an image to grayscale
	grayScaleImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# applying median blur to smoothen an image
	smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)

	# retrieving the edges for cartoon effect
	# by using thresholding technique
	getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
	                                cv2.ADAPTIVE_THRESH_MEAN_C,
	                                cv2.THRESH_BINARY, 9, 9)

	# applying bilateral filter to remove noise
	# and keep edge sharp as required
	colorImage = cv2.bilateralFilter(img, 9, 300, 300)

	# masking edged image with our "BEAUTIFY" image
	cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

	return cartoonImage

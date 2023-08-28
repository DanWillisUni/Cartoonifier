import cv2 #for image processing

MAX_PIXEL = 255 # suggest not change

DEFAULT_BLUR_KERNAL_SIZE = 5 # odd and greater than 1
DEFAULT_THRESHOLD = "Mean"
DEFAULT_THRESHOLD_BLOCK_SIZE = 11
DEFAULT_THRESHOLD_BLUR = 6
DEFAULT_BILATERAL_D = 15
DEFAULT_BILATERAL_SIGMA_COLOUR = 25
DEFAULT_BILATERAL_SIGMA_SPACE = 25

def adaptive_threshold(img, type, box_size, blur_val):
	return cv2.adaptiveThreshold(img, MAX_PIXEL,
								 type,
								 cv2.THRESH_BINARY, box_size, blur_val)
def otsu_threshold(img):
	return cv2.threshold(img, 0, MAX_PIXEL, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

def cartoonify(img,
			   _blur=DEFAULT_BLUR_KERNAL_SIZE,
			   _threshold_type=DEFAULT_THRESHOLD,
			   _threshold_box_size=DEFAULT_THRESHOLD_BLOCK_SIZE,
			   _threshold_blur=DEFAULT_THRESHOLD_BLUR,
			   _bilateral_d=DEFAULT_BILATERAL_D,
			   _bilateral_sigma_colour=DEFAULT_BILATERAL_SIGMA_COLOUR,
			   _bilateral_sigma_space=DEFAULT_BILATERAL_SIGMA_SPACE):
	return custom_cartoonify(img,
							 _blur,
							 _threshold_type,
							 _threshold_box_size,
							 _threshold_blur,
							 _bilateral_d,
							 _bilateral_sigma_colour,
							 _bilateral_sigma_space)
def custom_cartoonify(img, _blur, _threshold_type, _box_size, _blur_val, _bilateral_d, _bilateral_sigma_colour, _bilateral_sigma_space):
	# converting an image to grayscale
	gray_scale_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# applying median blur to smoothen an image
	smooth_gray_scale = cv2.medianBlur(gray_scale_image, DEFAULT_BLUR_KERNAL_SIZE)

	# retrieving the edges for cartoon effect
	# by using thresholding technique
	get_edge = None
	if _threshold_type == "Gauss":
		get_edge = adaptive_threshold(smooth_gray_scale, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, _box_size, _blur_val)
	elif _threshold_type == "Gauss+Otsu":
		gauss = adaptive_threshold(smooth_gray_scale, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, _box_size, _blur_val)
		get_edge = otsu_threshold(gauss)
	elif _threshold_type == "Mean":
		get_edge = adaptive_threshold(smooth_gray_scale, cv2.ADAPTIVE_THRESH_MEAN_C, _box_size, _blur_val)
	elif _threshold_type == "Otsu":
		get_edge = otsu_threshold(smooth_gray_scale)
	else:
		print("ERROR - Unknown threshold type")

	# applying bilateral filter to remove noise
	# and keep edge sharp as required
	color_image = cv2.bilateralFilter(img, _bilateral_d, _bilateral_sigma_colour, _bilateral_sigma_space)

	# masking edged image with our "BEAUTIFY" image
	cartoon_image = cv2.bitwise_and(color_image, color_image, mask=get_edge)

	return cartoon_image

def calculate_perfect_settings(how_cartoony):
	BLUR_KERNAL_SIZE = round((10 - how_cartoony) / 1.5)
	if BLUR_KERNAL_SIZE % 2 == 0:
		BLUR_KERNAL_SIZE += 1

	THRESHOLD = DEFAULT_THRESHOLD
	THRESHOLD_BLOCK_SIZE = round(how_cartoony * 1.6)
	if THRESHOLD_BLOCK_SIZE % 2 == 0:
		THRESHOLD_BLOCK_SIZE += 1
	THRESHOLD_BLUR = 15 - round(how_cartoony * 1.2)
	BILATERAL_D = round(4.5 * how_cartoony)
	return BLUR_KERNAL_SIZE, THRESHOLD, THRESHOLD_BLOCK_SIZE, THRESHOLD_BLUR, BILATERAL_D

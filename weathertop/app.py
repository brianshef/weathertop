from os import environ
import logging
import cv2
import numpy as np

# Logging
_loglevel = environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
	level=_loglevel,
	format='[%(asctime)s] [%(levelname)s]: %(message)s'
)
logging.getLogger(name=__name__)


def readImg(filename='./assets/map2.png'):
	logging.info(f"Loading {filename} ... ")
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	return img, filename


def enhance(img, brightness=0, contrast=0):
	if brightness < -127 or brightness > 127:
		logging.error(f"enhance() requires brightness to be between -127 and +127. Supplied: {brightness}")
	if contrast < -127 or contrast > 127:
		logging.error(f"enhance() requires contrast to be between -127 and +127. Supplied: {constrast}")
	_maxVal = 255
	_maxContrast = 127
	if brightness != 0:
		if brightness > 0:
			shadow = brightness
			highlight = _maxVal
		else:
			shadow = 0
			highlight = _maxVal + brightness
		alpha_b = (highlight - shadow)/_maxVal
		gamma_b = shadow
		
		enhanced = cv2.addWeighted(img, alpha_b, img, 0, gamma_b)
	else:
		enhanced = img.copy()
	
	if contrast != 0:
		f = 131*(contrast + _maxContrast)/(_maxContrast*(131-contrast))
		alpha_c = f
		gamma_c = _maxContrast*(1-f)
		
		enhanced = cv2.addWeighted(enhanced, alpha_c, enhanced, 0, gamma_c)

	return enhanced


def getContours(img):
	# alg = cv2.CHAIN_APPROX_NONE
	alg = cv2.THRESH_BINARY_INV
	brightness = 32
	contrast = 40

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	enhanced = enhance(gray, brightness=brightness, contrast=contrast)
	cv2.imshow(f"enhanced b={brightness} c={contrast}", enhanced)
	# # Static threshold
	# (T, threshold) = cv2.threshold(enhanced, 140, 255, alg)
	# Dynamic threshold
	(T, threshold) = cv2.threshold(enhanced, 0, 255, alg | cv2.THRESH_OTSU)
	cv2.imshow(f"threshold {T}", threshold)

	contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	return contours


def labelShape(img, label='unknown', center=(0, 0), color=(0, 0, 0), thickness=1):
	cv2.putText(img, label, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)


def labelShapes(img, contours, scalar=0.01):
	magenta = (255, 0, 255)
	yellow = (255, 255, 0)
	thickness = 2
	for c in contours:
		approx = cv2.approxPolyDP(c, scalar * cv2.arcLength(c, True), True)
		
		m = cv2.moments(c)
		x, y = 0, 0
		if m['m00'] != 0.0:
			x = int(m['m10']/m['m00'])
			y = int(m['m01']/m['m00'])
		center = (x, y)

		corners = len(approx)
		if corners == 3:
			cv2.drawContours(img, [c], 0, yellow, thickness)
			labelShape(img, 'triangle', center, color=yellow)
		elif corners == 4:
			pass
			# labelShape(img, 'quad', center)
		elif corners == 5:
			pass
			# labelShape(img, 'pentagon', center)
		elif corners == 6:
			pass
			# labelShape(img, 'hex', center)
		elif corners == 8:
			pass
			# labelShape(img, 'octagon', center)
		elif corners > 8 and corners < 10:
			pass
			# labelShape(img, 'polygon', center)
		else:
			cv2.drawContours(img, [c], 0, magenta, thickness)
			labelShape(img, 'circle', center, color=magenta)


def showImg(img, filename="image"):
	logging.info(f"Displaying {filename} ... ")
	cv2.imshow("Weathertop", img)
	logging.info(f" ... press any key to close {filename}")
	cv2.waitKey(0)


def main(config):
	logging.debug(config)
	logging.info(f"Weathertop (c) Brian Shef 2024")
	img, filename = readImg(filename=f"{config.source}/map2.png")
	contours = getContours(img)
	logging.info(f"Identified {len(contours)} contours in {filename}")
	logging.info("Labelling shapes ... ")
	labelShapes(img, contours)
	showImg(img, filename)
	cv2.destroyAllWindows()
	logging.info("Done")
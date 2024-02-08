# (c) Brian Shef 2024

import logging
import numpy as np
import cv2


APPNAME = "Weathertop"


def readImg(filename='./assets/map.png'):
	logging.info("Loading %s ... ", filename)
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	return img, filename


def getContours(img):
	tval = 215
	maxt = 255
	alg = cv2.CHAIN_APPROX_NONE

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, threshold = cv2.threshold(gray, tval, maxt, alg)
	contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	return contours


def labelShape(img, label='unknown', center=(0, 0), color=(0, 0, 0), thickness=1):
	cv2.putText(img, label, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)


def labelShapes(img, contours, scalar=0.01):
	magenta = (255, 0, 255)
	yellow = (255, 255, 0)
	thickness = 1
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
		else:
			cv2.drawContours(img, [c], 0, magenta, thickness)
			labelShape(img, 'circle', center, color=magenta)


def showImg(img, filename="image"):
	logging.info("Displaying %s ... ", filename)
	cv2.imshow(APPNAME, img)
	logging.info(" ... press any key to close %s", filename)
	cv2.waitKey(0)


def main():
	logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
	logging.info("%s (c) Brian Shef 2024", APPNAME)
	img, filename = readImg()
	contours = getContours(img)
	logging.info("Identified %d contours in %s", len(contours), filename)
	logging.info("Labelling shapes ... ")
	labelShapes(img, contours)
	showImg(img, filename)
	cv2.destroyAllWindows()
	logging.info("Done")


if __name__ == '__main__':
	main()


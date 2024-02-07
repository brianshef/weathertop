# (c) Brian Shef 2024

import logging
import cv2


APPNAME = "Weathertop"


def readImg(filename='./assets/map.png'):
	logging.info("Loading %s ... ", filename)
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	return img


def showImg(img):
	logging.info("Displaying image ... ")
	cv2.imshow(APPNAME, img)
	logging.info(" ... press any key to close image.")
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def main():
	logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
	logging.info("%s (c) Brian Shef 2024", APPNAME)
	img = readImg()
	showImg(img)
	logging.info("Done.")


if __name__ == '__main__':
	main()


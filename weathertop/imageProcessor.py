import cv2
import numpy as np
import logging
from weathertop import colors

class Processor:
    def __init__(self, src, logger=None) -> None:
        self.src = src
        if logger is None:
            self.logger = logging.getLogger(type(self).__name__)
            self.logger.setLevel('DEBUG')
        else:
            self.logger = logger
        self.original = self.readImg(self.src)
    
    def readImg(self, src):
        self.logger.info(f"Loading {src} ... ")
        try:
            return cv2.imread(src, cv2.IMREAD_COLOR)
        except Exception as e:
            self.logger.fatal(f"failed to load {src}: {e}")
            return None

    def showImg(self, img=None, title=None):
        if img is None:
            img = self.original
        if title is None:
            title = self.src
        self.logger.debug(f"Displaying {title} ... ")
        cv2.imshow(title, img)
        logging.info(f" ... press any key to close {title}")
    
    def getCorners(self, contour, epsilon=0.01) -> int:
        return len(
            cv2.approxPolyDP(contour, epsilon * cv2.arcLength(contour, True), True)
        )
    
    def getCenter(self, contour) -> tuple[int, int]:
        m = cv2.moments(contour)
        x, y = 0, 0
        if m['m00'] != 0.0:
            x = int(m['m10']/m['m00'])
            y = int(m['m01']/m['m00'])
        return (x, y)
    
    def labelShape(self, img, contour, label='unknown', color=colors.GREEN, thickness=1):
        img = self.original.copy() if img is None else img
        cv2.putText(img, label, self.getCenter(contour), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    def isCircle(self, contour) -> bool:
        _peri = cv2.arcLength(contour, True)
        if _peri <= 0.0:
            return False
        _circularity = 4 * np.pi * cv2.contourArea(contour) / (_peri * _peri)
        return _circularity > 0.9

    def isTriangle(self, contour) -> bool:
        return self.getCorners(contour, epsilon=0.04) == 3

    def enhance(self, brightness=0, contrast=0):
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
            enhanced = cv2.addWeighted(self.original, alpha_b, self.original, 0, gamma_b)
        else:
            enhanced = self.original.copy()
        
        if contrast != 0:
            f = 131*(contrast + _maxContrast)/(_maxContrast*(131-contrast))
            alpha_c = f
            gamma_c = _maxContrast*(1-f)
            enhanced = cv2.addWeighted(enhanced, alpha_c, enhanced, 0, gamma_c)

        return enhanced
    
    def getContours(self, dynamic=False, debug=False):
        enhanced = self.enhance(brightness=32, contrast=64)
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)

        threshold = 0.0
        if dynamic:
            (T, threshold) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        else:
            (T, threshold) = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
        
        if debug:
            self.showImg(enhanced, title=f"enhanced {self.src}")
            self.showImg(gray, title=f"gray enhanced {self.src}")
        
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.logger.debug(f"found {len(contours)} total contours in {self.src} (T={T})")
        return contours
        
    def getShapes(self):
        contours = self.getContours(dynamic=True, debug=True)
        circles = [c for c in contours if self.isCircle(c)]
        triangles = [c for c in contours if self.isTriangle(c)]

        self.logger.debug(f"found {len(circles)} circles and {len(triangles)} triangles in {self.src}")

        p = self.original.copy()
        for c in circles:
            cv2.drawContours(p, [c], -1, colors.MAGENTA, 1)
            self.labelShape(p, c, "CIRCLE", color=colors.MAGENTA)
        
        for t in triangles:
            cv2.drawContours(p, [c], -1, colors.RED, 1)
            self.labelShape(p, c, "TRIANGLE", color=colors.RED)
        
        self.showImg(p, f"Weathertop processed {self.src}")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


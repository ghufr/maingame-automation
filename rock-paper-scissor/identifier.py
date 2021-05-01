import cv2


class Identifier:
    def __init__(self, label, img):
        self.img = img
        self.thresh = None
        self.label = label
        self.h = 0

    def apply_hsv_filter(self, hsv_filter):
        self.thresh = cv2.inRange(self.img, hsv_filter[0], hsv_filter[1])
        return self.thresh

    def find_contours(self):
        cnts, _ = cv2.findContours(
            self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rectangles = []

        for cnt in cnts:
            rect = cv2.boundingRect(cnt)
            rw = rect[2]
            rh = rect[3]
            self.h = rh
            area = rw * rh
            if (area > 300):
                rectangles.append(rect)

        return rectangles

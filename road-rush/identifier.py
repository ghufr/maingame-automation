import cv2


class Identifier:
    hsv_filter = []
    label = ''
    area = 0
    aspect_ratio = 1
    w = 0
    h = 0

    def __init__(self, label, hsv_filter, w, h):
        self.label = label
        self.hsv_filter = hsv_filter
        self.area = w * h
        self.w = w
        self.h = h
        self.aspect_ratio = w / h

    def apply_hsv_filter(self, img_hsv, img_gray):
        img_thresh = cv2.inRange(
            img_hsv, self.hsv_filter[0], self.hsv_filter[1])

        img_thresh_blur = cv2.GaussianBlur(img_thresh, (5, 5), 0)
        img_masked = cv2.bitwise_and(img_thresh_blur, img_gray)
        # cv2.imshow(self.label, img_thresh_blur)
        return img_masked

    def find(self, img_masked):
        contours, hist = cv2.findContours(
            img_masked, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        rectangles = []
        # print(self.label, self.aspect_ratio)
        for cnt in contours:
            rect = cv2.boundingRect(cnt)
            rw = rect[2]
            rh = rect[3]
            area = rw * rh
            aspect_ratio = rw / rh
            # print(rw, rh, area)
            diff = abs(self.aspect_ratio - aspect_ratio)
            # print(self.label, diff)
            if (diff < 0.4 and area > 1000):
                rectangles.append(rect)
                # print('Jumlah Item: ',  len[rectagles])
        return rectangles

    def draw_rectangles(self, img_bgr, rectangles, color=(255, 255, 0)):
        for x, y, w, h in rectangles:
            cv2.rectangle(img_bgr, (x, y), (x+w, y+h), color, 2)

        return img_bgr

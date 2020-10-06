import cv2


class Identifier:
    hsv_filter = []
    label = ''
    area = 0
    w = 0
    h = 0

    def __init__(self, label, hsv_filter, w=10, h=10):
        self.label = label
        self.hsv_filter = hsv_filter
        self.area = w * h
        self.w = w
        self.h = h

    def apply_hsv_filter(self, img_hsv, img_gray):
        img_thresh = cv2.inRange(
            img_hsv, self.hsv_filter[0], self.hsv_filter[1])

        img_thresh_blur = cv2.GaussianBlur(img_thresh, (5, 5), 0)
        img_masked = cv2.bitwise_and(img_thresh_blur, img_gray)
        cv2.imshow(self.label, img_thresh_blur)
        return img_masked

    def find(self, img_masked):
        contours, hist = cv2.findContours(
            img_masked, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        rectangles = []
        sizes = []
        # print(self.label, self.aspect_ratio)
        # print()
        for cnt in contours:
            rect = cv2.boundingRect(cnt)
            rw = rect[2]
            rh = rect[3]
            area = rw * rh
            # aspect_ratio = rw / rh
            # print(rw, rh, area)

            # print(self.label, diff)
            if (self.label == 'skacang'):
                if (len(contours) > 20):
                    break

            if (area > self.area + 20):

                # print(area)
                rectangles.append(rect)
                sizes.append(area)
                # print('Jumlah Item: ',  len[rectagles])
        # print(len(rectangles))
        return rectangles, sizes

    def draw_rectangles(self, img_bgr, rectangles, color=(255, 255, 0)):
        for x, y, w, h in rectangles:
            cv2.rectangle(img_bgr, (x, y), (x+w, y+h), color, 2)

        return img_bgr

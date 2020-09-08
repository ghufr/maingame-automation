import cv2
import numpy as np

img = cv2.imread("screens/sample-1.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread("assets/telur.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]


# Mangkok or bungkus?

thresh = cv2.threshold(gray_img, 120, 255, 0)[1]
# im2, contours, hierarchy = cv2.findContours(
#     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# Object detection inside mangkok
gray_img_blurred = cv2.blur(gray_img, (10, 10))

result = cv2.matchTemplate(gray_img_blurred, template, cv2.TM_CCOEFF_NORMED)
loc = np.where(result >= 0.7)

for pt in zip(*loc[::-1]):
    cv2.rectangle(gray_img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

cv2.imshow("img", gray_img)
cv2.imshow("result", result)
cv2.imshow("treshold", thresh)


cv2.waitKey(0)
cv2.destroyAllWindows()

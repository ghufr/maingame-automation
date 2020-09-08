import cv2

img = cv2.imread('screens/sample-1.png')
template = cv2.imread('classifier/hostage/h-4.png', 0)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_gray = img_gray[320:520, 200:300]

result = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF_NORMED)

cv2.imshow("Result", result)
cv2.imshow("Gray", img_gray)
print(img_gray)

cv2.imwrite('res.png', img_gray)

cv2.waitKey(0)

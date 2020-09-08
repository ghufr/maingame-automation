import cv2
import numpy as np

from wincap import WinCap

import math
import pyautogui


def get_center(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    return cX, cY


def get_angle(p1, p2):
    return math.atan2(p1[1] - p2[1], p1[0] - p2[0]) * 180/math.pi


wincap = WinCap('Jungle Swing - Google Chrome')


def polar2cartesian(rho: float, theta_rad: float, rotate90: bool = False):
    """
    Converts line equation from polar to cartesian coordinates

    Args:
        rho: input line rho
        theta_rad: input line theta
        rotate90: output line perpendicular to the input line

    Returns:
        m: slope of the line
           For horizontal line: m = 0
           For vertical line: m = np.nan
        b: intercept when x=0
    """
    x = np.cos(theta_rad) * rho
    y = np.sin(theta_rad) * rho
    m = np.nan
    if not np.isclose(x, 0.0):
        m = y / x
    if rotate90:
        if m is np.nan:
            m = 0.0
        elif np.isclose(m, 0.0):
            m = np.nan
        else:
            m = -1.0 / m
    b = 0.0
    if m is not np.nan:
        b = y - m * x

    return m, bPoints on line


def line_end_points_on_image(rho: float, theta: float, image_shape: tuple):
    """
    Returns end points of the line on the end of the image
    Args:
        rho: input line rho
        theta: input line theta
        image_shape: shape of the image

    Returns:
        list: [(x1, y1), (x2, y2)]
    """
    m, b = polar2cartesian(rho, theta, True)

    end_pts = []

    if not np.isclose(m, 0.0):
        x = int(0)
        y = int(solve4y(x, m, b))
        if point_on_image(x, y, image_shape):
            end_pts.append((x, y))
            x = int(image_shape[1] - 1)
            y = int(solve4y(x, m, b))
            if point_on_image(x, y, image_shape):
                end_pts.append((x, y))

    if m is not np.nan:
        y = int(0)
        x = int(solve4x(y, m, b))
        if point_on_image(x, y, image_shape):
            end_pts.append((x, y))
            y = int(image_shape[0] - 1)
            x = int(solve4x(y, m, b))
            if point_on_image(x, y, image_shape):
                end_pts.append((x, y))

    return end_pts


def solve4x(y: float, m: float, b: float):
    """
    From y = m * x + b
         x = (y - b) / m
    """
    if np.isclose(m, 0.0):
        return 0.0
    if m is np.nan:
        return b
    return (y - b) / m


def solve4y(x: float, m: float, b: float):
    """
    y = m * x + b
    """
    if m is np.nan:
        return b
    return m * x + b


def point_on_image(x: int, y: int, image_shape: tuple):
    """
    Returns true is x and y are on the image
    """
    return 0 <= y < image_shape[0] and 0 <= x < image_shape[1]


def intersection(m1: float, b1: float, m2: float, b2: float):
    # Consider y to be equal and solve for x
    # Solve:
    #   m1 * x + b1 = m2 * x + b2
    x = (b2 - b1) / (m1 - m2)
    # Use the value of x to calculate y
    y = m1 * x + b1

    return int(round(x)), int(round(y))


def hough_lines_end_points(lines: np.array, image_shape: tuple):
    """
    Returns end points of the lines on the edge of the image
    """
    if len(lines.shape) == 3 and \
            lines.shape[1] == 1 and lines.shape[2] == 2:
        lines = np.squeeze(lines)
    end_pts = []
    for line in lines:
        rho, theta = line
        end_pts.append(
            line_end_points_on_image(rho, theta, image_shape))
    return end_pts


def hough_lines_intersection(lines: np.array, image_shape: tuple):
    """
    Returns the intersection points that lie on the image
    for all combinations of the lines
    """
    if len(lines.shape) == 3 and \
            lines.shape[1] == 1 and lines.shape[2] == 2:
        lines = np.squeeze(lines)
    lines_count = len(lines)
    intersect_pts = []
    for i in range(lines_count - 1):
        for j in range(i + 1, lines_count):
            m1, b1 = polar2cartesian(lines[i][0], lines[i][1], True)
            m2, b2 = polar2cartesian(lines[j][0], lines[j][1], True)
            x, y = intersection(m1, b1, m2, b2)
            if point_on_image(x, y, image_shape):
                intersect_pts.append([x, y])
    return np.array(intersect_pts, dtype=int)


while(True):
    bgr = wincap.get_screenshot()

    w = bgr.shape[1]
    h = bgr.shape[0]

    hsv = cv2.cvtColor(bgr, cv2.COLOR_RGB2HSV)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # thresh = cv2.inRange(hsv, (30, 0, 53), (180, 255, 255))
    thresh = cv2.inRange(hsv, (30, 0, 0), (33, 255, 255))
    blur = cv2.GaussianBlur(thresh, (3, 3), 0)
    # blur = cv2.bitwise_and(blur, gray)
    # ret3, thresh = cv2.threshold(
    #     thresh, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # ret, thresh2 = cv2.threshold(thresh, 127, 255, 0)

    # contours, hierarchy = cv2.findContours(
    #     blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # first = contours[0][0]

    # ncontours = []
    # for cnt in contours:
    #     rect = cv2.minAreaRect(cnt)
    #     width = rect[1][0]
    #     height = rect[1][1]
    #     area = width * height
    #     if (area > 3):
    #         ncontours.append(cnt)
    #         first = (cnt[0])
    #         last = cnt[1]
    #         print(first)
    #         break
    # cv2.circle(img, (first[0], 2), 7, (255, 255, 255), -1)
    # cv2.drawContours(thresh, [first], 0, (255, 255, 255), 3)
    # cv2.drawContours(thresh, [last], 0, (255, 255, 255), 3)

    # if (area > 2000):

    # ncontours.append(cnt)
    # print(area)
    # print(len(ncontours))
    # if (len(ncontours) == 2):
    #     first = ncontours
    #     print(first)
    # cv2.circle(img, first, 7, (255, 255, 255), -1)
    # cv2.circle(img, last, 7, (255, 255, 255), -1)

    #     print(contours)
    # print(ncontours)
    # center_1, center_2 = get_center(
    #     ncontours[0]), get_center(ncontours[1])
    # angle = get_angle(center_1, center_2)
    # angle2 = get_angle(center_2, center_1)

    # cv2.line(img, center_1, center_2, (255, 255, 0), 2)
    # cv2.circle(img, center_2, 7, (255, 255, 255), -1)

    # print(angle + angle2)
    # cv2.rec
    # print(angle)
    # ssm = angle + angle2
    # if (ssm < 6 and ssm >= 0):
    #     # pyautogui.click(200, 200)
    #     print('Match')
    edge = cv2.Canny(blur, 50, 150, apertureSize=3)
    # cv2.drawContours(edge, ncontours, -1, (0, 255, 255), 2)
    # dst = cv2.Canny(blur, 50, 100, apertureSize=5)
    # print(len[thresh])
    lines = cv2.HoughLines(edge, 1, np.pi / 180, 120)

    if lines is not None:
        print(len(lines))
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            # print(rho, theta)
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            # if (theta < 3.1 and theta > 2):
            #     pyautogui.click(200, 200)
            #     print(theta, 'Match')
            # else:
            #     print(theta)
            cv2.line(bgr, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

    # with_contour = bgr

    # for cnt in contours:
    #     rect = cv2.minAreaRect(cnt)
    #     width = rect[1][0]
    #     height = rect[1][1]
    #     area = width * height
    #     if area > 3:
    #         rows, cols = with_contour.shape[:2]
    #         [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
    #         lefty = int((-x*vy/vx) + y)
    #         righty = int(((cols-x)*vy/vx)+y)
    #         cv2.line(with_contour, (cols-1, righty),
    #                  (0, lefty), (0, 255, 0), 2)

    cv2.imshow('Blur', blur)
    cv2.imshow('BGR', bgr)
    cv2.imshow('RGB', rgb)
    cv2.imshow('Canny', edge)
    cv2.imshow('Threshold', thresh)

    # cv2.imwrite('thresh.png', img)
    # break

    if cv2.waitKey(25) == ord('q'):
        cv2.destroyAllWindows()
        break

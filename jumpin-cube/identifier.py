import math


class Identifier:

    def is_gameover(self, cap):
        # h = 679
        # w = 50%
        w_half = math.floor(cap.shape[1] * 0.5)
        h = cap.shape[0]
        # print(cap.shape[1], h)
        # print(w_half)
        pixel = cap[w_half][440]

        return False

        # if (pixel[0] == 163 and pixel[1] == 193 and pixel[2] == 63):
        #     return True
        # else:
        #     return False

    def detect(self, cap):
        h = math.floor(cap.shape[0] * 0.5)
        w = math.floor(cap.shape[1] * 0.5)

        pixel = cap[w][h]
        print(pixel, end=" ")
        if (pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255):
            return True
        else:
            return False

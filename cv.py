import time

import cv2
import numpy as np

field_mat = [[70, 33, 10, 10, 10, 32, 70, 70],
             [63, 70, 33, 10, 10, 32, 70, 70],
             [63, 70, 11, 11, 70, 7041, 70, 70],
             [63, 70, 11, 11, 11, 10, 10, 11],
             [70, 70, 11, 11, 70, 70, 70, 70],
             [30, 70, 30, 30, 70, 70, 70, 7041],
             [11, 70, 33, 32, 70, 70, 70, 70],
             [1140, 70, 33, 10, 10, 70, 70, 7050], ]

downRed = np.array([0, 140, 6])
upRed = np.array([0, 140, 6])

downBlack = np.array([0, 140, 6])
upBlack = np.array([0, 140, 6])

keyboardcontrol = 'None'
direction = 'None'

Flag_line_blue = False
Flag_line_orange = False
Flag_button = False
Flag_obj_green = False
Flag_obj_red = False
Flag_line = False

time_button = time.time()


def searchForColor(frame, minhsv, maxhsv, draw=False):
    mask = cv2.inRange(frame, minhsv, maxhsv)
    contors, k = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = 0, 0, 0, 0
    for cont in contors:
        area = cv2.contourArea(cont)
        if area > 250:
            x1, y1, w1, h1 = cv2.boundingRect(cont)
            if w1 * h1 > w * h:
                x, y, w, h = x1, y1, w1, h1
    if (draw):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return x, y, w, h


def createMapMatrix(frame):
    global field_mat
    for i in range(8):
        for j in range(8):
            img = frame[i * 50:(i + 1) * 50, j * 50:(j + 1) * 50]
            ImageHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            xR, yR, wR, hR = searchForColor(img, downRed, upRed)
            xG, yG, wG, hG = searchForColor(img, downRed, upRed)
            xY, yY, wY, hY = searchForColor(img, downRed, upRed)
            xO, yO, wO, hO = searchForColor(img, downRed, upRed)
            xB, yB, wB, hB = searchForColor(img, downRed, upRed)
            if wY * hY > 0:
                field_mat = 0
            elif wG * hG > 0:
                # зеленая труба
                if wG > hG:
                    if (yG + hG / 2) > 50 / 2:
                        field_mat = 33
                    else:
                        field_mat = 31
                else:
                    if (xG + wG / 2) > 50 / 2:
                        field_mat = 32
                    else:
                        field_mat = 34

            elif wB * hB > 0:
                # пандусы(рампы)
                deltx = xB - xR
                delty = yB - yR
                if abs(deltx) < abs(delty):
                    if delty < 0:
                        field_mat = 54
                    else:
                        field_mat = 52
                else:
                    if deltx < 0:
                        field_mat = 53
                    else:
                        field_mat = 51

            elif wR * hR > 0:
                # трубы красные
                if wR < hR:  # vertical
                    if hO * wO > 0:  # pandus
                        field_mat = 7011
                    else:  # ground
                        field_mat = 7011
                else:
                    if hO * wO > 0:  # pandus
                        field_mat = 7011
                    else:  # ground
                        field_mat = 7011

            elif wO * hO > 0:
                xBl, yBl, wBl, hBl = searchForColor(img, downBlack, upBlack)
                if wBl > hBl:  # horizontal
                    field_mat = 10101
                else:  # vertical
                    field_mat = 10101

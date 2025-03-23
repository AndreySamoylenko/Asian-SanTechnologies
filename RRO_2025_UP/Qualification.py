import os
import time

import RobotAPI as rapi
import cv2
import numpy as np

from basic_functions import *

from Future_engeneers_path_creation_new import create_path

# создаём объект для работы с камерой робота
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)


def drawMap(map__frame, matrix):
    for j in range(len(matrix)):
        for i in range(len(matrix[j])):
            if os.path.exists(f"/home/pi/robot/field_pictures/{matrix[j][i]}.png"):
                map__frame[j * 100:(j + 1) * 100, i * 100:(i + 1) * 100] = cv2.imread(
                    f"/home/pi/robot/field_pictures/{matrix[j][i]}.png")  # надо будет закинуть на распберри картинки
            else:
                print(f'{matrix[j][i]}.png does not exist in the folder')


fps = 0
fps_count = 0
t = time.time()

color = (255, 255, 255)  # белый цвет (B, G, R)
map_frame = np.full((800, 800, 3), color, dtype=np.uint8)

mat = [[52, 20, 20, 34, 10, 20, 10, 42], [10, 10, 20, 20, 34, 20, 10, 62], [32, 20, 20, 34, 20, 10, 10, 62],
       [10, 10, 20, 20, 20, 34, 10, 62], [10, 10, 32, 20, 20, 20, 34, 20], [71, 10, 10, 10, 10, 10, 10, 20],
       [10, 10, 42, 10, 20, 10, 10, 33], [10, 10, 34, 32, 10, 20, 10, 10]]


def transponation(matrix):
    matrix1 = [[61, 61, 61, 10, 10, 10, 42, 10],
               [10, 10, 10, 10, 20, 20, 20, 34],
               [10, 10, 20, 33, 10, 33, 10, 10],
               [10, 10, 20, 20, 10, 51, 10, 10],
               [10, 10, 20, 20, 10, 20, 10, 10],
               [71, 33, 41, 20, 20, 20, 34, 10],
               [20, 31, 10, 31, 10, 10, 10, 10],
               [10, 10, 10, 10, 10, 20, 10, 10]]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix1[i][j] = matrix[j][i]
    return matrix1


list_of_motions = []
list_of_motions = create_path(mat, [0, 0, 0, 0, 0, 0, 1])

# list_of_motions = ["L1","X4","L1","X2","L1","X1","R1","G1","L1","X3","L1","G1","R2","X1","L1","X1","L1","F1","X3","L1","G1","R1","F0",
#                    "X1","P1","L1","X1","R1","P1","R1","X2","L1","P1","OO"]

# list_of_motions = ["x1", "r1", "x1", "r1", "f1", "f0", "OO", "x1", "R1", "X1", "L1", "X1", "G1",
#                    "x1", "R1", "X1", "L1", "F1", "X1", "R1", "X2", "L1", "X1", "G1",
#                    "x1", "L1", "X2", "R1", "X2", "F0", "X2", "R1", "X2", "G1",
#                    "x2", "R1", "X1", "R1", "X1", "R1", "P1", "L1", "X1", "R1", "P1", "L1", "X1", "R1", "P1"]
#
# list_of_motions = ["T3","X1", "R1", "P1", "L1", "X1", "R1", "P1", "L1", "X1", "R1", "P1"]

list_of_motions.append("OO")
counter = -1

state = "button wait"
timer_actions = 0
while 1:
    frame = robot.get_frame(wait_new_frame=1)

    if state == "button wait":
        send("99")
        if digitalRead():
            send("B0")
            state = "string reading"
            timer_actions = time.time()

    if state == "string reading":
        if time.time() - timer_actions > 0.5:
            timer_actions = time.time()
            counter %= len(list_of_motions)
            send(list_of_motions[counter])

        if digitalRead():
            send("  ")
            state = "wait for action to end"

    if state == "wait for action to end":
        if not digitalRead():
            state = "string reading"
            counter += 1
            counter %= len(list_of_motions)

    fps_count += 1
    if time.time() > t + 1:
        fps = fps_count
        fps_count = 0
        t = time.time()
    #
    if state == "button wait":
        drawMap(map_frame, mat)
        robot.set_frame(map_frame, 40)
    else:
        cv2.rectangle(frame, (0, 0), (320, 30), (0, 0, 0), -1)
        cv2.rectangle(frame, (530, 0), (640, 30), (0, 0, 0), -1)
        robot.text_to_frame(frame, f"{state} {list_of_motions[counter]}", 20, 20)
        robot.text_to_frame(frame, f"FPS: {fps}", 530, 20)
        robot.set_frame(frame, 40)

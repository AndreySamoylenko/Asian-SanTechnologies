import os
import time

import RobotAPI as rapi
from class_and_for_all import *

# создаём объект для работы с камерой робота
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)
# создаём объект для работы с матрицей и компьютерным зрением
mc = MainComputer((8, 8), 1)


def drawMap(map__frame, matrix):
    for j in range(len(matrix)):
        for i in range(len(matrix[j])):
            path = f"/home/pi/robot/field_pictures/{matrix[j][i]}.png"
            if os.path.exists(path):
                map__frame[j * 50:(j + 1) * 50, i * 50:(i + 1) * 50] = cv2.resize(cv2.imread(path), [50, 50])
                # надо будет закинуть на распберри картинки
            else:
                print(f'{matrix[j][i]}.png does not exist in the folder')


mat = np.full((15, 15), 0, dtype=np.int8)

fps = 0
fps_count = 0
t = time.time()

color = (255, 255, 255)  # белый цвет (B, G, R)
map_frame = np.full((750, 750, 3), color, dtype=np.uint8)

list_of_motions = []

counter = -1

state = "button waiting"
timer_actions = 0

# -------------------Algorithm starts here----------------------
# to add:
# check what floor are we on
# spin around and scan all tiles

while 1:
    frame = robot.get_frame(wait_new_frame=1)

    if state == "button waiting":
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
            state = "driving"

    if state == "driving":
        if not digitalRead():
            counter += 1
            if counter == len(list_of_motions):
                counter = 0
                list_of_motions = []
                state = "Matrix analysis"
            else:
                state = "Surroundings scanning"

    if state == "Surroundings scanning":
        frame = robot.get_frame(wait_new_frame=1)
        edges = mc.analyse_edges(frame)

        if sum(edges) and mat.shape != (8,8):  # если обнаружен край и мы в нем заинтересованы
            if mat.shape == (15, 15):  # если край обнаружен впервые
                mat = mc.from_15x15_to_15x8(mat, edges.index(1))  # меняем форму матрицы
            elif mc.robot_orientation % 2 == 0:  # если это второй край
                mat = mc.from_15x8_to_8x8(mat, edges.index(1))  # меняем форму матрицы

        prev_matrix, messages, flags = mc.scan_frame(frame, mat)

    if state == "Matrix analysis":
        pass

    fps_count += 1
    if time.time() > t + 1:
        fps = fps_count
        fps_count = 0
        t = time.time()

    if state == "button wait":
        drawMap(map_frame, mat)
        robot.set_frame(map_frame, 40)
    else:
        cv2.rectangle(frame, (0, 0), (320, 30), (0, 0, 0), -1)
        cv2.rectangle(frame, (530, 0), (640, 30), (0, 0, 0), -1)
        robot.set_frame(frame, 40)

    robot.text_to_frame(frame, f"{state} {list_of_motions[counter]}", 20, 20)
    robot.text_to_frame(frame, f"FPS: {fps}", 530, 20)

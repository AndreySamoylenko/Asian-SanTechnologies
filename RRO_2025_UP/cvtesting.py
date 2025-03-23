import time

import RobotAPI as rapi
from RobotAPI import RobotAPI

from basic_functions import *
from cv import *

# создаём объект для работы с камерой робота

robot: RobotAPI = rapi.RobotAPI(flag_serial=False, flag_keyboard=True)
robot.set_camera(100, 640, 480)


def drawTelemetry(frame_, zones=True, text=True):
    for i in range(len(messages[0])):
        if text:
            robot.text_to_frame(frame_, messages[0][i], interest_zones[keys_[flags[0][i]]][0][i][0][0] + 10,
                                interest_zones[keys_[flags[0][i]]][0][i][1][1] + 25, (50, 10, 200))
            robot.text_to_frame(frame_, messages[1][i], interest_zones[keys_[flags[1][i]]][1][i][0][0] + 10,
                                interest_zones[keys_[flags[1][i]]][1][i][0][1] - 25, (50, 10, 200))
        if zones:
            cv2.rectangle(frame_, interest_zones[keys_[flags[0][i]]][0][i][0], interest_zones[keys_[flags[0][i]]][0][i][1], (200, 250, 250),
                          3)
            cv2.rectangle(frame_, interest_zones[keys_[flags[1][i]]][1][i][0], interest_zones[keys_[flags[1][i]]][1][i][1], (200, 250, 250),
                          3)
    for i in range(len(edge_cords[1])):
        cv2.rectangle(frame_, edge_cords[1][i][0], edge_cords[1][i][1], (0, 20, 200), 2)


t = time.time()
timer_actions = 0

fps = 0
fps_count = 0
fps_t = time.time()

x, y, w, h = 0, 0, 0, 0

frame = robot.get_frame(wait_new_frame=1)
frame1 = frame

prev_matrix = [[0, 0, 0],
               [0, 0, 0]]

messages = [['', '', ''],
            ['', '', '']]

floor = 1  # 1 - нижний этаж/уровень, 2 - верхний этаж/уровень
edges = [0, 0, 0]
flags = [[0] * 3] * 2

state = 'key reading'

while 1:
    fps_count += 1

    if time.time() - t > 1:
        print(f"{prev_matrix[0]}\n{prev_matrix[1]}  \n --\n{edges}\n--")

        fps = fps_count
        fps_count = 0
        t = time.time()

    key = robot.get_key()

    if state == "key reading":
        mess = '  '
        if key >= 0:
            if key == 87:
                mess = "x1"
            elif key == 65:
                mess = "l1"
            elif key == 68:
                mess = "r1"
            elif key == 83:
                mess = "X1"

        if time.time() - timer_actions > 0.2:
            timer_actions = time.time()
            send(mess)

        if digitalRead():
            send("  ")
            state = "wait for action to end"

    if state == "wait for action to end":
        if not digitalRead():
            state = "key reading"

    frame = robot.get_frame(wait_new_frame=1)

    if time.time() - fps_t > 0.2:
        fps_t = time.time()
        edges = analyse_edges(frame, floor)
        prev_matrix, messages, flags = scanTheFrame(frame, floor)

    drawTelemetry(frame, zones=True, text=True)

    cv2.rectangle(frame, (0, 0), (150, 30), (0, 0, 0), -1)
    robot.text_to_frame(from_cringe_to_normal(from_cords_to_slice(frame, interest_zones['same'][0][0])), "FPS: " + str(fps), 20, 20)

    robot.set_frame(frame)

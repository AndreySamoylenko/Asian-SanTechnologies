import os
import time

import RobotAPI as rapi
from RobotAPI import RobotAPI

from basic_functions import *
from cv import *

# создаём объект для работы с камерой робота

robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

# Создаём пустое изображение (в формате BGR)
color = (255, 255, 255)  # белый цвет (B, G, R)
map_frame = np.full((750, 750, 3), color, dtype=np.uint8)

field_map_predv = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                           )


def drawMap(map__frame, matrix):
    # print(len(matrix),len(matrix[0]))
    for j in range(len(matrix)):
        for i in range(len(matrix[j])):
            if os.path.exists(f"field pictures/{matrix[j][i]}.png"):
                map__frame[j * 50:(j + 1) * 50, i * 50:(i + 1) * 50] = cv2.resize(cv2.imread(
                    f"field pictures/{matrix[j][i]}.png"), [50, 50])  # надо будет закинуть на распберри картинки

            else:
                pass
                # print(matrix[j][i])
            # надо будет закинуть на распберри картинки


def drawTelemetry(frame_, zones=True, text=True):
    for i in range(len(messages[0])):
        if text:
            robot.text_to_frame(frame_, messages[0][i], interest_zones[keys_[flags[0][i]]][0][i][0][0] + 10,
                                interest_zones[keys_[flags[0][i]]][0][i][1][1] + 25, (50, 150, 200))
            robot.text_to_frame(frame_, messages[1][i], interest_zones[keys_[flags[1][i]]][1][i][0][0] + 10,
                                interest_zones[keys_[flags[1][i]]][1][i][0][1] - 25, (50, 150, 200))
        if zones:
            cv2.rectangle(frame_, interest_zones[keys_[flags[0][i]]][0][i][0], interest_zones[keys_[flags[0][i]]][0][i][1], (200, 250, 250),
                          3)
            cv2.rectangle(frame_, interest_zones[keys_[flags[1][i]]][1][i][0], interest_zones[keys_[flags[1][i]]][1][i][1], (200, 250, 250),
                          3)


t = time.time()
timer_actions = time.time()

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

current_orientation = 1  # up
current_position = [8, 8]
floor = 1  # 1 - нижний этаж/уровень, 2 - верхний этаж/уровень

flags = [[0] * 3] * 2

next_move = ''
state = 'button wait'

while 1:
    fps_count += 1

    if time.time() - t > 1:
        # print(flags)
        fps = fps_count
        fps_count = 0
        t = time.time()

    if state == "button wait":
        send("99")
        if digitalRead():
            send("B0")
            state = "scan"
            timer_actions = time.time()
            time.sleep(2)

    if state == 'scan':
        frame = robot.get_frame(wait_new_frame=1)
        edges = analyse_edges(frame, floor)
        prev_matrix, messages, flags = scanTheFrame(frame, floor)

        updateMap(prev_matrix, field_map_predv, current_position, current_orientation)
        # print(prev_matrix[1][1])
        if (isTileValid(prev_matrix[1][1], floor)  # если мы можем проехать вперёд и клетка справа относительно робота сканирована
                and field_map_predv[current_position[0] + ((current_orientation - 1) % 2) * (3 - current_orientation)]
                [current_position[1] + (current_orientation % 2) * (2 - current_orientation)]):
            if prev_matrix[1][1] % 10 == 0:
                next_move = "x1"
            elif floor == 1:
                floor = 2
                next_move = 'f1'
            elif floor == 2:
                floor = 1
                next_move = 'f0'

            current_position[0] += (current_orientation % 2) * (2 - current_orientation)
            current_position[1] -= ((current_orientation - 1) % 2) * (3 - current_orientation)

        else:
            next_move = "r1"
            current_orientation = current_orientation % 4 + 1

        state = 'message sending'

    if state == "message sending":
        if time.time() - timer_actions > 0.5:
            timer_actions = time.time()
            send(next_move)

        if digitalRead():
            send("  ")
            state = "wait for action to end"

    if state == "wait for action to end":
        if not digitalRead():
            state = "scan"

    drawMap(map_frame, field_map_predv)
    # drawTelemetry(frame, zones=True, text=True)

    cv2.rectangle(map_frame, (0, 0), (320, 30), (0, 0, 0), -1)
    cv2.rectangle(map_frame, (530, 0), (640, 30), (0, 0, 0), -1)
    robot.text_to_frame(map_frame, f"{state}", 20, 20)
    robot.text_to_frame(map_frame, f"FPS: {fps}", 530, 20)
    robot.set_frame(map_frame)

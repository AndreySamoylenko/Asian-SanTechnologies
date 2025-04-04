import time

import RobotAPI as rapi
from RobotAPI import RobotAPI
from class_and_for_all import *

# создаём объект для работы с камерой робота

robot: RobotAPI = rapi.RobotAPI(flag_serial=False, flag_keyboard=True)
robot.set_camera(100, 640, 480)

mc = MainComputer(position=[8, 8], direction=1)


def drawTelemetry(frame_, messages, flags):
    for i in range(len(messages[0])):
        robot.text_to_frame(frame_, messages[0][i], interest_zones[keys_[flags[0][i]]][0][i][0][0] + 10,
                            interest_zones[keys_[flags[0][i]]][0][i][1][1] + 25, (50, 10, 200))
        robot.text_to_frame(frame_, messages[1][i], interest_zones[keys_[flags[1][i]]][1][i][0][0] + 10,
                            interest_zones[keys_[flags[1][i]]][1][i][0][1] - 25, (50, 10, 200))

        cv2.rectangle(frame_, interest_zones[keys_[flags[0][i]]][0][i][0], interest_zones[keys_[flags[0][i]]][0][i][1],
                      (200, 250, 250), 3)
        cv2.rectangle(frame_, interest_zones[keys_[flags[1][i]]][1][i][0], interest_zones[keys_[flags[1][i]]][1][i][1],
                      (200, 250, 250), 3)
    for dot in edge_cords[mc.elevation]:
        cv2.rectangle(frame, dot[0], dot[1], (0, 0, 0), 2)


t = time.time()
timer_actions = 0

fps = 0
fps_count = 0
fps_t = time.time()

x, y, w, h = 0, 0, 0, 0

frame = robot.get_frame(wait_new_frame=1)
frame1 = frame

prev_matrix = np.full((15, 15, 1), 0)

messages = [['', '', ''],
            ['', '', '']]

floor = 2  # 1 - нижний этаж/уровень, 2 - верхний этаж/уровень
mc.elevation = floor
edges = [0, 0, 0]
flags = [[0] * 3] * 2

state = 'key reading'

while 1:
    fps_count += 1

    if time.time() - t > 1:
        # print(f"{edges}\n--")
        # print(f"{flags}\n--")

        fps = fps_count
        fps_count = 0
        t = time.time()

    frame = robot.get_frame(wait_new_frame=1)

    if time.time() - fps_t > 0.2:
        fps_t = time.time()
        edges = mc.analyse_edges(frame)
        messages, flags = mc.scan_frame(frame, prev_matrix, telemetry=1)

    # drawTelemetry(frame, messages, flags)

    cv2.rectangle(frame, (0, 0), (150, 30), (0, 0, 0), -1)
    for dot in interest_zones['lower']:
        cv2.rectangle(frame, dot[0][0], dot[0][1], (0, 0, 0), 1)
        cv2.rectangle(frame, dot[1][0], dot[1][1], (0, 0, 0), 1)
        cv2.rectangle(frame, dot[2][0], dot[2][1], (0, 0, 0), 1)

    robot.set_frame(frame)

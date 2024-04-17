import os
import time

import RobotAPI as rapi
from Future_engeneers_path_creation_new import create_path
from class_and_for_all import *

# создаём объект для работы с камерой робота
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

mc = MainComputer(position=[8, 8], direction=1)


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

mat = [[10, 10, 20, 32, 20, 20, 1041, 34],
       [10, 42, 10, 20, 20, 34, 10, 62],
       [10, 20, 20, 20, 34, 10, 10, 62],
       [33, 10, 10, 10, 20, 10, 10, 62],
       [20, 10, 20, 10, 20, 10, 10, 71],
       [20, 10, 20, 10, 10, 10, 10, 10],
       [31, 10, 33, 10, 41, 10, 20, 33],
       [10, 10, 10, 20, 20, 20, 34, 31]]

#huh
floor = 1

list_of_motions = create_path(mat, 0)
# list_of_motions = ['X2',"X1","F1","F0","F1","X1"]
print(list_of_motions)
# list_of_motions = ["Q0"]
# list_of_motions = [


#     # 'X2', 'R1', 'X1', 'G0',
#     # 'R2', 'X1', 'L1', 'X1', 'L1', 'F1', 'X2', 'F0',
#     # 'X2', 'L1', 'X3', 'L1', 'X2', 'R1', 'X1', 'L1', 'X1', 'G0',
#     # 'R2', 'X1', 'R1', 'X1', 'L1', 'X2', 'R1',
#     'X1', 'R1', 'F1', 'F0', 'F1',
#     'X2','OO', 'R1', 'X3', 'R1', 'X2', 'F0', 'F1', 'X1', 'G0',
#     'R2', 'X1', 'F0', 'F1', 'X2', 'L1', 'X2', 'L1', 'X1', 'R1', 'X1', 'L1', 'X1',
#     'F0', 'F1', 'F0', 'X1', 'R1', 'X1']

# list_of_motions = ['X1', 'F1', 'F0', 'F1', 'OO', 'X2']

list_of_motions = [f'a{floor}'] + list_of_motions + ['OO']

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

    if state == "button wait":
        drawMap(map_frame, mat)
        robot.set_frame(map_frame, 40)
    else:
        cv2.rectangle(frame, (0, 0), (320, 30), (0, 0, 0), -1)
        cv2.rectangle(frame, (530, 0), (640, 30), (0, 0, 0), -1)
        robot.text_to_frame(frame, f"{state} {list_of_motions[counter]} {floor}", 20, 20)
        robot.text_to_frame(frame, f"FPS: {fps}", 530, 20)
        robot.set_frame(frame, 40)

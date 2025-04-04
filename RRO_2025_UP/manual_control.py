import time

import cv2

import RobotAPI as rapi
from class_and_for_all import *

# создаём объект для работы с камерой робота
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

mc = MainComputer(position=[8, 8], direction=1)

fps = 0
fps_count = 0
t = time.time()

counter = -1

state = "button wait"
timer_actions = 0
flag = 0

while 1:
    frame = robot.get_frame(wait_new_frame=1)
    key = robot.get_key()

    if state == "button wait":
        send("99")
        if digitalRead():
            send("B0")
            state = "key reading"
            timer_actions = time.time()

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
            elif key == 49:
                flag = (flag + 1) % 2

        if time.time() - timer_actions > 0.3:
            timer_actions = time.time()
            send(mess)

        if digitalRead():
            send("  ")
            state = "wait for action to end"

    if state == "wait for action to end":
        if not digitalRead():
            state = "key reading"

    fps_count += 1
    if time.time() > t + 1:
        fps = fps_count
        fps_count = 0
        t = time.time()

    cv2.rectangle(frame, (0, 0), (320, 30), (0, 0, 0), -1)
    cv2.rectangle(frame, (530, 0), (640, 30), (0, 0, 0), -1)
    robot.text_to_frame(frame, str(state), 20, 20)
    robot.text_to_frame(frame, f"FPS: {fps}", 530, 20)

    # if flag:
    cv2.rectangle(frame, (190, 55), (450, 85), (0, 0, 0), 2)
    cv2.rectangle(frame, (180, 105), (460, 135), (0, 0, 0), 2)
    cv2.rectangle(frame, (170, 215), (470, 245), (0, 0, 0), 2)

    robot.set_frame(frame, 40)

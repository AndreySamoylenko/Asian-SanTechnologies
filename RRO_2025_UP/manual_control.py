import time

import RobotAPI as rapi
from class_and_for_all import *

# создаём объект для работы с камерой робота
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

mc = MainComputer(position=[8, 8], direction=1)

fps = 0
fps_count = 0
t = time.time()


def drawTelemetry(frame_, messages, flags):
    for i in range(len(messages[0])):
        robot.text_to_frame(frame_, messages[0][i], interest_zones[keys_[flags[0][i]]][0][i][0][0] + 10,
                            interest_zones[keys_[flags[0][i]]][0][i][1][1] + 25, (50, 10, 200))
        robot.text_to_frame(frame_, messages[1][i], interest_zones[keys_[flags[1][i]]][1][i][0][0] + 10,
                            interest_zones[keys_[flags[1][i]]][1][i][0][1] - 25, (50, 10, 200))

        cv2.rectangle(frame_, interest_zones[keys_[flags[0][i]]][0][i][0], interest_zones[keys_[flags[0][i]]][0][i][1],
                      (200, 250, 250),3)
        cv2.rectangle(frame_, interest_zones[keys_[flags[1][i]]][1][i][0], interest_zones[keys_[flags[1][i]]][1][i][1],
                      (200, 250, 250),3)

    for dot in edge_cords[mc.elevation]:
        cv2.rectangle(frame, dot[0], dot[1], (0, 0, 0), 2)


KEY_MAP = {
    # Буквы (английская раскладка)
    65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e',
    70: 'f', 71: 'g', 72: 'h', 73: 'i', 74: 'j',
    75: 'k', 76: 'l', 77: 'm', 78: 'n', 79: 'o',
    80: 'p', 81: 'q', 82: 'r', 83: 's', 84: 't',
    85: 'u', 86: 'v', 87: 'w', 88: 'x', 89: 'y',
    90: 'z',

    # Цифры
    48: '0', 49: '1', 50: '2', 51: '3', 52: '4',
    53: '5', 54: '6', 55: '7', 56: '8', 57: '9',

    # Пробел, Esc, Enter, Tab
    32: 'space',
    27: 'esc',
    13: 'enter',
    9: 'tab',
    8: 'backspace',

    # Спецсимволы
    186: ';',
    187: '=',
    188: ',',
    189: '-',
    190: '.',
    191: '/',
    192: '`',
    219: '[',
    220: '\\',
    221: ']',
    222: "'",

    # Стрелки
    37: 'left',
    38: 'up',
    39: 'right',
    40: 'down',
}

mat = np.full((15, 15, 1), 0)

state = "button wait"
timer_actions = 0
flag = 0
messages, flags = [[0] * 3] * 2, [[0] * 3] * 2
mess = '  '
counter = -1
premoves = ['A0', 'a1', 'l1']

while 1:
    frame = robot.get_frame(wait_new_frame=1)
    key = robot.get_key()

    if state == "button wait":
        send("99")
        if digitalRead():
            send("B0")
            state = "string reading"
            timer_actions = time.time()

    if state == "key reading":
        if key in KEY_MAP.keys():
            key = KEY_MAP[key]
            if key == 'w' or key == 'up':
                mess = "x1"
            elif key == 'a' or key == 'left':
                mess = "l1"
            elif key == 'd' or key == 'right':
                mess = "r1"
            elif key == 's' or key == 'down':
                mess = "X1"
            elif key == 'g':
                mess = "G0"
            elif key == 'p':
                mess = "P1"
            elif key == 'z':
                mess = f"f{2 - mc.elevation}"

        if time.time() - timer_actions > 0.3:
            timer_actions = time.time()
            send(mess)

        if digitalRead():
            if mess == 'f0':
                mc.elevation = 1
            elif mess == 'f1':
                mc.elevation = 2
            send("  ")
            mess = '  '
            state = "wait for action to end"

    if state == "string reading":
        if time.time() - timer_actions > 0.5:
            timer_actions = time.time()
            send(premoves[counter])

        if digitalRead():
            send("  ")
            state = "wait for action to end"

    if state == "wait for action to end":
        if not digitalRead():
            if counter + 1 < len(premoves):
                if premoves[counter] != 'A0':
                    state = "string reading"
                else:
                    state = "floor checking"
                counter += 1
            else:
                state = "key reading"

    if state == "floor checking":
        floor = mc.check_floor(frame)
        mc.elevation = floor
        premoves[1] = f'a{floor}'
        print(mc.elevation)
        state = "string reading"

    fps_count += 1
    if time.time() > t + 1:
        fps = fps_count
        messages, flags = mc.scan_frame(frame, mat, telemetry=1)
        fps_count = 0
        t = time.time()

    cv2.rectangle(frame, (0, 0), (320, 30), (0, 0, 0), -1)
    cv2.rectangle(frame, (530, 0), (640, 30), (0, 0, 0), -1)
    robot.text_to_frame(frame, str(state), 20, 20)
    robot.text_to_frame(frame, f"FPS: {fps}", 530, 20)

    # if flag:
    cv2.rectangle(frame, mc.cords_for_floor[0], mc.cords_for_floor[1], (0, 0, 0), 2)

    drawTelemetry(frame, messages, flags)

    robot.set_frame(frame, 40)

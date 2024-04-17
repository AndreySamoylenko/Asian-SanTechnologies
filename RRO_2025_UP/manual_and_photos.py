import time
import os
import cv2
import numpy as np
import RobotAPI as rapi
from class_and_for_all import *

# Создаём объект для работы с камерой робота
robot = rapi.RobotAPI(flag_serial=False)
robot.set_camera(100, 640, 480)

mc = MainComputer(position=[8, 8], direction=1)

fps = 0
fps_count = 0
t = time.time()

# Папка для сохранения слайсов
SAVE_DIR = "saved_zones"
os.makedirs(SAVE_DIR, exist_ok=True)  # Создаём папку, если её нет

# Определяем interest_zones (как вы предоставили)
interest_zones = {
    "higher": [
        [[[0, 190], [160, 360]], [[180, 170], [460, 350]], [[480, 190], [640, 360]]],
        [[[90, 95], [215, 150]], [[240, 100], [400, 180]], [[425, 95], [550, 150]]]
    ],
    "same": [
        [[[20, 230], [180, 420]], [[200, 240], [440, 450]], [[460, 230], [620, 420]]],
        [[[100, 125], [230, 220]], [[230, 120], [410, 220]], [[410, 125], [540, 220]]]
    ],
    "lower": [
        [[[60, 270], [200, 450]], [[220, 270], [420, 480]], [[440, 270], [580, 450]]],
        [[[120, 165], [210, 270]], [[230, 155], [410, 270]], [[430, 165], [520, 270]]]
    ]
}

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


def save_interest_zones(frame, interest_zones):
    """Сохраняет все interest zones из кадра в папку SAVE_DIR."""
    timestamp = int(time.time())
    saved_count = 0

    for zone_type, zone_groups in interest_zones.items():
        for group_idx, zone_group in enumerate(zone_groups):
            for zone_idx, zone_coords in enumerate(zone_group):
                try:
                    (x1, y1), (x2, y2) = zone_coords
                    # Убедимся, что координаты валидны
                    if x1 >= x2 or y1 >= y2:
                        print(f"Неверные координаты: {zone_type} group {group_idx} zone {zone_idx}")
                        continue

                    # Вырезаем зону с проверкой границ
                    zone_slice = frame[y1:y2, x1:x2]

                    if zone_slice.size == 0:
                        print(f"Пустая зона: {zone_type} group {group_idx} zone {zone_idx}")
                        continue

                    # Создаем имя файла
                    filename = f"{SAVE_DIR}/{zone_type}_group{group_idx}_zone{zone_idx}_{timestamp}.png"

                    # Проверяем, существует ли папка
                    if not os.path.exists(SAVE_DIR):
                        os.makedirs(SAVE_DIR)

                    # Сохраняем изображение
                    if cv2.imwrite(filename, zone_slice):
                        saved_count += 1
                        print(f"Успешно сохранено: {filename}")
                    else:
                        print(f"Ошибка сохранения: {filename}")

                except Exception as e:
                    print(f"Ошибка обработки зоны {zone_type} group {group_idx} zone {zone_idx}: {str(e)}")

    print(f"Всего сохранено зон: {saved_count}")
    return saved_count > 0

KEY_MAP = {
    65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e',
    70: 'f', 71: 'g', 72: 'h', 73: 'i', 74: 'j',
    75: 'k', 76: 'l', 77: 'm', 78: 'n', 79: 'o',
    80: 'p', 81: 'q', 82: 'r', 83: 's', 84: 't',
    85: 'u', 86: 'v', 87: 'w', 88: 'x', 89: 'y',
    90: 'z',
    48: '0', 49: '1', 50: '2', 51: '3', 52: '4',
    53: '5', 54: '6', 55: '7', 56: '8', 57: '9',
    32: 'space', 27: 'esc', 13: 'enter', 9: 'tab',
    8: 'backspace', 186: ';', 187: '=', 188: ',',
    189: '-', 190: '.', 191: '/', 192: '`',
    219: '[', 220: '\\', 221: ']', 222: "'",
    37: 'left', 38: 'up', 39: 'right', 40: 'down',
}

mat = np.full((15, 15, 1), 0)

state = "button wait"
timer_actions = 0
flag = 0
messages, flags = [[0] * 3] * 2, [[0] * 3] * 2
mess = '  '
counter = -1
premoves = ['A0', 'a1', 'l1']

while True:
    frame = robot.get_frame(wait_new_frame=1)
    key = robot.get_key()

    # Если нажата клавиша H (код 72), сохраняем interest zones
    if key == 72:  # 72 - код клавиши 'H'
        save_interest_zones(frame, interest_zones)

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
        messages, flags, smth = mc.scan_frame(frame, mat, 1)
        fps_count = 0
        t = time.time()

    cv2.rectangle(frame, (0, 0), (320, 30), (0, 0, 0), -1)
    cv2.rectangle(frame, (530, 0), (640, 30), (0, 0, 0), -1)
    robot.text_to_frame(frame, str(state), 20, 20)
    robot.text_to_frame(frame, f"FPS: {fps}", 530, 20)

    cv2.rectangle(frame, mc.cords_for_floor[0], mc.cords_for_floor[1], (0, 0, 0), 2)
    drawTelemetry(frame, messages, flags)

    robot.set_frame(frame, 40)
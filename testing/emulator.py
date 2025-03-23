import os

import numpy as np

os.system("")

field_mat = np.array([
    [42, 10, 10, 10, 10, 10, 10, 10],
    [20, 33, 20, 20, 20, 34, 10, 33],
    [10, 31, 10, 10, 20, 10, 10, 20],
    [10, 10, 10, 10, 10, 10, 20, 51],
    [41, 10, 20, 20, 10, 10, 20, 20],
    [10, 10, 20, 20, 10, 10, 31, 31],
    [10, 20, 10, 31, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 63, 63, 63],
])

visible_mat = np.array([[0] * 8] * 8)


class emulator:
    def __init__(self):
        self.robot_position = [3, 3]
        self.robot_orientation = 1

    def reveal_2x3(self, field, visible):
        offsetx, offsety = 0, 0
        height, width = 3, 3
        if self.robot_orientation % 2:
            offsetx = -1
            offsety = -2 * (self.robot_orientation == 1) + (self.robot_orientation == 3)
            height = 2
        else:
            offsetx = -2 * (self.robot_orientation == 4) + (self.robot_orientation == 2)
            offsety = -1
            width = 2

        new_tiles_pos = [self.robot_position[0] + offsetx, self.robot_position[1] + offsety]
        for x in range(new_tiles_pos[0], new_tiles_pos[0] + width):
            for y in range(new_tiles_pos[1], new_tiles_pos[1] + height):
                if visible[y][x] == 0:
                    visible[y][x] = field[y][x]

    def move_robot_f(self):
        dir = self.robot_orientation
        if dir % 2:
            self.robot_position[1] += dir - 2
        else:
            self.robot_position[0] += 3 - dir

    def turn_robot(self, way):
        global robot_orientation
        if way > 0:
            robot_orientation = (robot_orientation + way - 1) % 4 + 1
        elif way < 0:
            way = -way
            robot_orientation = (robot_orientation + way - 1) % 4 + 1

    def display_symb(self, tile, underline=0):
        # ANSI-коды цвета
        BLACK = "\033[30m"  # Чёрный
        RED = "\033[31m"  # Красный
        BLUE = "\033[34m"  # Синий
        GREEN = "\033[32m"  # Зеленый цвет текста
        YELLOW = "\033[33m"  # Желтый
        WHITE = "\033[97m"  # Белый
        RESET = "\033[0m"  # Сброс цвета
        UNDERLINE = "\033[4m"  # Код подчеркивания
        ITALIC = "\033[3m"

        # Цвет фона
        BLACK_BG = "\033[40m"  # Чёрный фон
        WHITE_BG = "\033[47m"  # Белый фон
        RED_BG = "\033[41m"  # Красный фон
        GREEN_BG = "\033[42m"  # Зелёный фон
        PURPL_BG = "\033[45m"

        alph = {0: [BLACK, PURPL_BG, "\u2584\u2580", RESET],
                1: [BLACK, PURPL_BG, "??", RESET],
                10: [WHITE, WHITE_BG, "\u2588\u2588", RESET],
                20: [BLACK, WHITE_BG, "\u2588\u2588", RESET],
                31: [RED, BLACK_BG, f"\u25CF{BLUE}\u25CF", RESET],
                32: [WHITE, BLACK_BG, "\u2588\u2588", RESET],
                33: [BLUE, BLACK_BG, f"\u25CF{RED}\u25CF", RESET],
                34: [WHITE, BLACK_BG, "\u2588\u2588", RESET],
                41: [RED, WHITE_BG, "\u25CF\u25CF", RESET],
                42: [RED, WHITE_BG, "\u2590\u258C", RESET],
                51: [RED, BLACK_BG, "\u25CF\u25CF", RESET],
                52: [RED, BLACK_BG, "\u2590\u258C", RESET],
                61: [WHITE, GREEN_BG, "\u2584\u2584", RESET],
                62: [WHITE, GREEN_BG, f"\u2588{GREEN}\u2588", RESET],
                63: [WHITE, GREEN_BG, "\u2580\u2580", RESET],
                64: [GREEN, GREEN_BG, f"\u2588{WHITE}\u2588", RESET]}

        if tile in alph.keys():
            result = ''.join(alph[tile])
        else:
            result = ''.join(alph[1])
        char = ' '
        if underline:
            if self.robot_orientation == 1:
                char = f"{YELLOW}\u2191"
            elif self.robot_orientation == 2:
                char = f"{YELLOW}\u2192"
            elif self.robot_orientation == 3:
                char = f"{YELLOW}\u2193"
            elif self.robot_orientation == 4:
                char = f"{YELLOW}\u2190"
        print(result, end=char)

    def show_map(self, visible, erase=1):
        if erase:
            os.system('cls')
        rows, cols = len(visible), len(visible[0])
        for y in range(cols):
            for x in range(rows):
                self.display_symb(visible[y][x], self.robot_orientation, self.robot_position[1] == y and self.position[0] == x)
            print()

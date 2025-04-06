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


class Emulator:
    def __init__(self, position=None, direction=1, floor=1):
        if position is None:
            position = [3, 3]
        self.robot_position = position
        self.robot_orientation = direction
        self.floor = floor

    def reveal_2x3(self, field, visible):
        height, width = 2, 3  # Default for horizontal orientation (1 or 3)

        # Determine the offsets based on orientation
        if self.robot_orientation % 2:  # 1 (up) or 3 (down)
            if self.robot_orientation == 1:  # facing up
                x_offset = -1
                y_offset = -2
            else:  # facing down (3)
                x_offset = -1
                y_offset = 1
        else:  # 2 (right) or 4 (left)
            height, width = 3, 2  # Switch to vertical rectangle
            if self.robot_orientation == 2:  # facing right
                x_offset = 1
                y_offset = -1
            else:  # facing left (4)
                x_offset = -2
                y_offset = -1

        # Calculate starting position
        start_x = self.robot_position[0] + x_offset
        start_y = self.robot_position[1] + y_offset

        # Ensure we stay within bounds
        rows, cols = len(field), len(field[0])

        for y in range(max(0, start_y), min(rows, start_y + height)):
            for x in range(max(0, start_x), min(cols, start_x + width)):
                if visible[y][x] == 0:
                    visible[y][x] = field[y][x]

    def move_robot_f(self, field):
        # Get field dimensions
        height = len(field)
        width = len(field[0]) if height > 0 else 0

        # Verify current position is valid
        if not (0 <= self.robot_position[1] < height and
                0 <= self.robot_position[0] < width):
            print("Error: Robot is outside the field boundaries")
            exit()

        old_tile = field[self.robot_position[1]][self.robot_position[0]]
        new_pos = self.robot_position.copy()

        # Calculate new position based on orientation
        if self.robot_orientation % 2:  # 1 (up) or 3 (down)
            new_pos[1] += self.robot_orientation - 2
        else:  # 2 (right) or 4 (left)
            new_pos[0] += 3 - self.robot_orientation

        # Check if new position is valid
        if not (0 <= new_pos[1] < height and
                0 <= new_pos[0] < width):
            print("Error: Cannot move outside field boundaries")
            exit(1)

        new_tile = field[new_pos[1]][new_pos[0]]

        # Movement validation logic
        if new_tile == 0:
            print("Error: Trying to move to undefined tile (0)")
            exit()
        elif old_tile == 10:
            if new_tile == 10 or new_tile == 30 + self.robot_orientation:
                self.robot_position = new_pos
            else:
                print(f"Invalid move: Cannot go from {old_tile} to {new_tile} (facing {self.robot_orientation})")
                exit()
        elif old_tile == 20:
            if new_tile == 20 or new_tile == 30 + ((self.robot_orientation + 2) - 1) % 4 + 1:
                self.robot_position = new_pos
            else:
                print(f"Invalid move: Cannot go from {old_tile} to {new_tile} (facing {self.robot_orientation})")
                exit()
        elif old_tile // 10 == 3:  # Ramp tiles (31-34)
            if (abs(old_tile - new_tile) == 2 or  # Ramp-to-ramp
                    (old_tile == 30 + self.robot_orientation and new_tile == 20) or
                    (old_tile == 30 + ((self.robot_orientation - 1) + 2) % 4 + 1 and new_tile == 10)):
                self.robot_position = new_pos
                self.floor = new_tile // 10
            else:
                print(f"Invalid ramp move: Cannot go from {old_tile} to {new_tile}")
                exit()
        else:
            print(f"Unknown tile type: {old_tile}")
            exit()

    def turn_robot(self, way):
        self.robot_orientation = (self.robot_orientation + way - 1) % 4 + 1

    def edge_check(self, mat):
        mat = np.array(mat)
        height, width = mat.shape[:2]
        result = -1
        if self.robot_orientation == 1:
            result = self.robot_position[1]
        elif self.robot_orientation == 2:
            result = width - 1 - self.robot_position[0]
        elif self.robot_orientation == 3:
            result = height - 1 - self.robot_position[1]
        elif self.robot_orientation == 4:
            result = self.robot_position[0]

        if result > 2: result = -1
        return result

    def display_symb(self, tile, underline=0):
        # ANSI-коды цвета
        BLACK = "\033[30m"  # Чёрный
        RED = "\033[31m"  # Красный
        BLUE = "\033[34m"  # Синий
        GREEN = "\033[32m"  # Зеленый цвет текста
        YELLOW = "\033[33m"  # Желтый
        WHITE = "\033[97m"  # Белый
        RESET = "\033[0m"  # Сброс цвета

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
                32: [RED, BLACK_BG, f"\u259D{BLUE}\u2596", RESET],
                33: [BLUE, BLACK_BG, f"\u25CF{RED}\u25CF", RESET],
                34: [BLUE, BLACK_BG, f"\u259D{RED}\u2596", RESET],
                41: [RED, WHITE_BG, "\u25CF\u25CF", RESET],
                42: [WHITE, RED_BG, "\u258C\u2590", RESET],
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
                self.display_symb(visible[y][x], self.robot_position[1] == y and self.robot_position[0] == x)
            print()

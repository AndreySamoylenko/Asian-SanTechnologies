import os

import numpy as np

from Future_engeneers_path_creation_new import *
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

    def get_3x2_rows(self, matrix):
        #idktbh
        """
        Возвращает область 3x2 из матрицы в виде строк (рядов),
        ориентированную по направлению

        Параметры:
            matrix: входная матрица (2D список/массив)
            center_x, center_y: центральные координаты
            direction: направление (1 - вверх, 2 - вправо, 3 - вниз, 4 - влево)

        Возвращает:
            Список списков - область 3x2, где каждый подсписок это строка (ряд)
            Всегда возвращает 2 строки по 3 элемента
        """
        direction = self.robot_orientation
        center_x = self.robot_position[0] + (robot_pos_finder(replace_ints_in_matrix(matrix), False)[1] - 8)
        center_y = self.robot_position[1] + (robot_pos_finder(replace_ints_in_matrix(matrix), False)[0] - 8)
        print(center_x, center_y)

        rows = len(matrix)
        if rows == 0:
            return [[0] * 3, [0] * 3]  # Всегда возвращаем 2 строки по 3 элемента

        cols = len(matrix[0])
        result = []

        # Определяем смещения для разных направлений
        if direction == 1:  # Вверх
            offsets = [(-2, -1), (-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1)]
        elif direction == 2:  # Вправо
            offsets = [(-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
        elif direction == 3:  # Вниз
            offsets = [(1, -1), (1, 0), (1, 1), (2, -1), (2, 0), (2, 1)]
        elif direction == 4:  # Влево
            offsets = [(-1, -2), (0, -2), (1, -2), (-1, -1), (0, -1), (1, -1)]
        else:
            raise ValueError("Направление должно быть от 1 до 4")

        # Собираем данные с проверкой границ
        values = []
        for dy, dx in offsets:
            y = center_y + dy
            x = center_x + dx
            if 0 <= y < rows and 0 <= x < cols:
                values.append(matrix[y][x])
            else:
                values.append(0)

        # Всегда возвращаем 2 строки по 3 элемента
        return [values[:3], values[3:]]

    def update_map(self, new_tiles, mat):
        cords_of_tiles_on_map = [0, 0]

        if self.robot_orientation == 1:
            cords_of_tiles_on_map = [self.robot_position[0] - 2, self.robot_position[1] - 1]
        elif self.robot_orientation == 2:
            cords_of_tiles_on_map = [self.robot_position[0] - 1, self.robot_position[1] + 1]
        elif self.robot_orientation == 3:
            cords_of_tiles_on_map = [self.robot_position[0] + 1, self.robot_position[1] - 1]
        elif self.robot_orientation == 4:
            cords_of_tiles_on_map = [self.robot_position[0] - 1, self.robot_position[1] - 2]

        height_of_new_tiles = 2
        width_of_new_tiles = 3
        if len(new_tiles) == 2 and len(new_tiles[0]) == 3:
            for i in range(height_of_new_tiles):
                for j in range(width_of_new_tiles):
                    if 0 <= cords_of_tiles_on_map[0] + 2 < 15 and 0 <= cords_of_tiles_on_map[1] + 2 < 15:
                        # поворот клетки перед записью в матрицу
                        direction_of_map_object = new_tiles[i][j] % 10
                        if direction_of_map_object:
                            new_tiles[i][j] -= direction_of_map_object
                            if 40 <= new_tiles[i][j] < 53:
                                new_tiles[i][j] += direction_of_map_object % 2 + 1
                            else:
                                new_tiles[i][j] += (direction_of_map_object + self.robot_orientation - 1 - 1) % 4 + 1
                        # поворот зоны вставки
                        cords_insert = []
                        if self.robot_orientation == 1:
                            cords_insert = [cords_of_tiles_on_map[0] + i, cords_of_tiles_on_map[1] + j]
                        elif self.robot_orientation == 2:
                            cords_insert = [cords_of_tiles_on_map[0] + j, cords_of_tiles_on_map[1] + (1 - i)]
                        elif self.robot_orientation == 3:
                            cords_insert = [cords_of_tiles_on_map[0] + (1 - i), cords_of_tiles_on_map[1] + (2 - j)]
                        elif self.robot_orientation == 4:
                            cords_insert = [cords_of_tiles_on_map[0] + (2 - j), cords_of_tiles_on_map[1] + i]
                        else:
                            print("wrong direction")

                        if mat[cords_insert[0]][cords_insert[1]] == 0:
                            mat[cords_insert[0]][cords_insert[1]] = new_tiles[i][j]
        else:
            print("new_tiles wrong parameter")

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

    def edge_check(self, matrix):

        size = 8  # Размер матрицы 8x8

        x = self.robot_position[0] + (robot_pos_finder(replace_ints_in_matrix(matrix))[1] - 8)
        y = self.robot_position[1] + (robot_pos_finder(replace_ints_in_matrix(matrix))[0] - 8)

        if self.robot_orientation == 1:  # Вверх (проверяем y)
            distance = y
        elif self.robot_orientation == 2:  # Вправо (проверяем x)
            distance = (size - 1) - x
        elif self.robot_orientation == 3:  # Вниз (проверяем y)
            distance = (size - 1) - y
        elif self.robot_orientation == 4:  # Влево (проверяем x)
            distance = x
        else:
            raise ValueError("Некорректное направление. Допустимые значения: 1-4")

        if distance == 1:
            return 0
        elif distance == 2:
            return 1
        else:
            return -1

    def from_15x15_to_15x8(self, m15x15, distance_to_edge):
        tile_under_robot = int(m15x15[self.robot_position[1]][self.robot_position[0]])
        m15x15[self.robot_position[1]][self.robot_position[0]] = 70

        if self.robot_orientation != 1:
            m15x15 = self.rotate_matrix(m15x15, 5 - self.robot_orientation)
            self.robot_orientation = 1

        new_pos = []
        for i in range(15):
            for j in range(15):
                if m15x15[i][j] == 70:
                    new_pos = [i, j]
                    break

        m15x8 = m15x15[new_pos[0] - distance_to_edge:(new_pos[0] - distance_to_edge) + 8, 0:15]
        m15x8[distance_to_edge][new_pos[1]] = tile_under_robot
        self.robot_position = [new_pos[1], distance_to_edge]
        return m15x8

    @staticmethod
    def rotate_matrix(mat_, turn_value):
        mat1 = mat_
        mat_res = []
        for turn in range(turn_value):
            mat_res = np.array(mat_)
            for i in range(len(mat1)):
                for j in range(len(mat1[0])):
                    direction = mat1[j][i] % 10
                    mat1[j][i] -= direction
                    if direction:
                        if 5 >= mat1[j][i] // 10 >= 4:
                            direction = direction % 2 + 1
                        else:
                            direction = direction % 4 + 1

                    mat_res[i, len(mat1[0]) - 1 - j] = mat1[j][i] + direction

            mat1 = mat_res
        return mat_res

    def from_15x15_to_15x8(self, m15x15, distance_to_edge):
        """
        inputs:
        матрица с полем 15 на 15
        расстояние от робота до края

        outputs:
        матрица 8х15 с полем

        вообще эта функция берет имеющееся поле
        разворачивает его так, чтобы найденный край был сверху
        и записывает в новую матрицу 8 строк находящихся ниже найденного края.

        после чего переписывает позицию и направление робота
        """

        tile_under_robot = int(m15x15[self.robot_position[1]][self.robot_position[0]]) # запомнили на какой клетке стояли (её код)
        m15x15[self.robot_position[1]][self.robot_position[0]] = 70
        # заменили её на 70 (код робота)((чтобы потом по этому коду её найти и заменить обратно))

        if self.robot_orientation != 1:      # если матрица повернута не так как нам нужно
            m15x15 = self.rotate_matrix(m15x15, 5 - self.robot_orientation) # поворачиваем
            self.robot_orientation = 1

        new_pos = []
        # ищем заранее оставленный код робота в повернутой матрице (хотя если на россию пройдем то я буду юзать матрицу поворота)
        for i in range(15):
            for j in range(15):
                if m15x15[i][j] == 70:
                    new_pos = [i, j]   # и собственно записываем ее
                    break

        m15x8 = m15x15[new_pos[0] - distance_to_edge:(new_pos[0] - distance_to_edge) + 8, 0:15]
        # забираем из старой матрицы 8 строк ниже края и пишем их как новую матрицу
        m15x8[distance_to_edge][new_pos[1]] = tile_under_robot
        # возвращаем клетку под роботом на место
        self.robot_position = [new_pos[1], distance_to_edge]
        # перезаписываем позицию
        return m15x8
        # возвращаем новую матрицу

    def from_15x8_to_8x8(self, m15x8, distance_to_edge):
        """
        тут всё проще чем в предыдущей функции
        мы уже знаем с каких сторон край ожидается
        и обрабатываем как раз эти два случая
        """
        if self.robot_orientation % 2 == 0: # проверим верное ли направление
            # (1 и 3 быть не может потому что, тогда мы найдем тот край в котором уже были)
            if self.robot_orientation == 2:
                m8x8 = m15x8[0:8, self.robot_position[0] + distance_to_edge - 7:self.robot_position[0] + distance_to_edge + 1]
                return m8x8
            elif self.robot_orientation == 4:
                m8x8 = m15x8[0:8, self.robot_position[0] - distance_to_edge:self.robot_position[0] - distance_to_edge + 8]
                return m8x8
            else:
                print('oh no, wrong direction')
        else:
            print('opa, wrong direction')

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

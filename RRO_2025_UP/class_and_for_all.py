import RPi.GPIO as GPIO
import cv2
import numpy as np
import serial

# -------------------------Serial----------------------------------
ser = serial.Serial('/dev/ttyS0', 9600)
ser.flush()  # очищаем буфер


def send(message):
    data_to_send = message + "\n"  # Data to send (must be bytes)
    ser.write(data_to_send.encode('utf-8'))


# -------------------------GPIO----------------------------------

# Choose the correct GPIO numbering scheme (BCM is recommended)
GPIO.setmode(GPIO.BCM)
# Define the GPIO pin you're using
GPIO_PIN = 23
GPIO.setup(GPIO_PIN, GPIO.IN)


def digitalRead():
    return GPIO.input(GPIO_PIN)


# -------------------------HSV----------------------------------
# здесь лежат наборы границ цветов в цветовом пространстве HSV
# они нужны для использования в функции cv2.inRange()
downRed = np.array([0, 90, 0])
upRed = np.array([10, 255, 255])
downRed1 = np.array([170, 90, 0])
upRed1 = np.array([180, 255, 255])

downEdge = np.array([170, 80, 0])
upEdge = np.array([180, 255, 255])
downEdge1 = np.array([0, 80, 0])
upEdge1 = np.array([10, 255, 255])

downBlue = np.array([104, 44, 82])
upBlue = np.array([117, 255, 255])

downGreen = np.array([58, 114, 0])
upGreen = np.array([88, 255, 255])

downWhite = np.array([0, 0, 130])
upWhite = np.array([180, 70, 255])

# -------------------------Cords for cv2----------------------------------

edge_cords = {1: (((220, 105), (420, 135)), ((170, 215), (470, 245)), ((200, 440), (440, 480))),
              2: (((220, 145), (420, 175)), ((170, 255), (470, 280)), ((200, 440), (440, 480)))}

interest_zones = {"higher": [[[[0, 190], [160, 360]], [[180, 170], [460, 350]], [[480, 190], [640, 360]]],
                             [[[90, 95], [215, 150]], [[240, 100], [400, 180]], [[425, 95], [550, 150]]]],

                  "same": [[[[20, 230], [180, 420]], [[200, 240], [440, 450]], [[460, 230], [620, 420]]],
                           [[[100, 125], [230, 220]], [[230, 120], [410, 220]], [[410, 125], [540, 220]]]],

                  "lower": [[[[60, 270], [200, 450]], [[220, 270], [420, 480]], [[440, 270], [580, 450]]],
                            [[[120, 165], [210, 270]], [[230, 155], [410, 270]], [[430, 165], [520, 270]]]]}

cords_for_white = {1: [[[[20, 210], [200, 400]], [[200, 210], [440, 430]], [[440, 210], [620, 400]]],
                       [[[100, 115], [215, 160]], [[0, 0], [0, 0]], [[440, 115], [550, 160]]]],
                   2: [[[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]],
                       [[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]]]}

for i in range(len(cords_for_white[1])):
    for j in range(len(cords_for_white[1][i])):
        for k in range(len(cords_for_white[1][i][j])):
            for l in range(len(cords_for_white[1][i][j][k])):
                if cords_for_white[1][i][j][k][l] == 0:
                    cords_for_white[1][i][j][k][l] = int((interest_zones["higher"][i][j][k][l] + interest_zones["same"][i][j][k][l]) / 2)
                if cords_for_white[2][i][j][k][l] == 0:
                    cords_for_white[2][i][j][k][l] = int((interest_zones["lower"][i][j][k][l] + interest_zones["same"][i][j][k][l]) / 2)

keys_ = ['lower', 'same', 'higher']


# -------------------------CLASS----------------------------------


class MainComputer:
    def __init__(self, position=None, direction=1):
        if position is None:
            position = [8, 8]
        self.robot_position = position
        self.robot_orientation = direction

    elevation = 1
    cords_for_floor = [[290, 440], [640 - 290, 480]]

    @staticmethod
    def count_in_matrix(code, matrix):
        result = 0
        for stroke in matrix:
            for elem in stroke:
                if elem == code:
                    result += 1
        return result

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

    @staticmethod
    def from_cords_to_slice(frame_, massive2x2):
        # небольшая функция для уменьшения записи
        return frame_[massive2x2[0][1]:massive2x2[1][1], massive2x2[0][0]:massive2x2[1][0]]

    @staticmethod
    def count_white(massive, step=5):
        summa = 0
        summb = 0
        for row in range(0, len(massive), step):
            for pixel in range(0, len(massive[row]), step):
                if massive[row][pixel] > 0:
                    summa += 1
                else:
                    summb += 1
        return summa, summb

    @staticmethod
    def search_for_color(frame_, minhsv, maxhsv, min_area=50):
        if minhsv[0] == downRed[0]:
            mask1 = cv2.inRange(frame_, downRed, upRed)
            mask2 = cv2.inRange(frame_, downRed1, upRed1)
            mask = cv2.bitwise_or(mask1, mask2)
        elif minhsv[0] == downEdge[0]:
            mask1 = cv2.inRange(frame_, downEdge, upEdge)
            mask2 = cv2.inRange(frame_, downEdge1, upEdge1)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(frame_, minhsv, maxhsv)

        contours, k = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = 0, 0, 0, 0
        for cont in contours:
            area = cv2.contourArea(cont)
            if area > min_area:
                x1, y1, w1, h1 = cv2.boundingRect(cont)
                if w1 * h1 > w * h:
                    x, y, w, h = x1, y1, w1, h1

        return x, y, w, h

    def tube_crutch(self, frame_):
        # мой любимый костыль для труб
        """
        красные трубы если находятся в положении 2 относительно робота
        (то есть робот не может их забрать с этой позиции, но если трубу повернуть то сможет)
        в центральной клетке ближней к роботу то на кадре в не видно красной подставки
        поэтому мы придумали такой выход из положения

        мы берем четыре отрезка на нашей зоне интереса и смотрим попарную разницу яркости пикселей на них
        смотрим разницу между максимумом и минимумом горизонтальных отрезков
        и её же для вертикальных отрезков

        и если эти две разницы в пропорции далеки от единицы то значит там есть труба
        """

        gray = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
        gray = gray.astype(np.int16)
        frame_height, frame_width = gray.shape[:2]
        differences = [[], []]
        const_x, const_y = int(0.8 * frame_width), int(0.8 * frame_height)

        for pix in range(int(0.3 * frame_width), int(0.7 * frame_width)):
            differences[0].append(gray[const_y][pix + 1] - gray[const_y][pix])
            differences[0].append(gray[frame_height - const_y][pix + 1] - gray[frame_height - const_y][pix])

        for pix in range(int(0.3 * frame_height), int(0.7 * frame_height)):
            differences[1].append(gray[pix + 1][const_x] - gray[pix][const_x])
            differences[1].append(gray[pix + 1][frame_width - const_x] - gray[pix][frame_width - const_x])

        diffs1 = max(differences[0]) - min(differences[0])
        diffs2 = max(differences[1]) - min(differences[1])
        if abs(diffs1 / diffs2 - 1) > 0.5:
            return True
        return False

    def look_at_tile(self, frame_, white_flag, crutch_flag=0):
        message = "none"
        result = 0

        frame_height, frame_width = frame_.shape[:2]
        min_area = frame_height * frame_width * 0.04
        frame_b = cv2.blur(frame_, [11, 11])

        ImageHSV = cv2.cvtColor(frame_b, cv2.COLOR_BGR2HSV)
        if white_flag:  # если клетка белая
            xR, yR, wR, hR = self.search_for_color(ImageHSV, downRed, upRed, min_area)
            xG, yG, wG, hG = self.search_for_color(ImageHSV, downGreen, upGreen, min_area)

            if wG * hG > 0:
                # зеленая труба
                if wG > hG:
                    if (yG + hG / 2) > frame_height / 2:
                        result = 61
                    else:
                        result = 63  # это вроде невозможный вариант (чтобы увидеть такое нужно быть вне поля)
                else:
                    if (xG + wG / 2) > frame_width / 2:
                        result = 62
                    else:
                        result = 64
                message = "stand " + str(result - 60)
            elif wR * hR > 0:
                # трубы красные
                if crutch_flag == 2:
                    if wR > 0.5 * frame_width:
                        result = 41
                    else:
                        result = 42
                else:
                    if wR < hR:  # vertical
                        result = 42
                    else:  # horizontal
                        result = 41
                message = "tube " + str(result - 40)
            elif crutch_flag and self.tube_crutch(frame_):
                result = 42
                message = "tube " + str(result - 40)
            else:
                result = 10
                message = 'lower X'
        else:  # если клетка черная
            min_area = frame_height * frame_width * 0.02

            xB, yB, wB, hB = self.search_for_color(ImageHSV, downBlue, upBlue, min_area * 0.5)
            xR, yR, wR, hR = self.search_for_color(ImageHSV, downRed, upRed, min_area)

            if wB * hB > 0:
                # пандусы(рампы)
                deltx = xB - xR
                delty = yB - yR
                x, y, w, h = xB, yB, wB, hB

                if abs(deltx) < abs(delty):
                    if delty < 0:
                        result = 34  # рампа направо (синий ближе к роботу)
                    else:
                        result = 32  # рампа налево (красный ближе к роботу)
                else:
                    if deltx < 0:
                        result = 33  # рампа назад (верх ближе к роботу)
                    else:
                        result = 31  # рампа вперед (низ ближе к роботу)
                message = "ramp " + str(result - 30)
            elif wR * hR > 0:
                # трубы красные
                if crutch_flag == 2:
                    if wR > 0.5 * frame_width:
                        result = 51
                    else:
                        result = 52
                else:
                    if wR < hR:  # vertical
                        result = 52
                    else:  # horizontal
                        result = 51
                message = "tube " + str(result - 40)
            elif crutch_flag == 1 and self.tube_crutch(frame_):
                result = 52
                message = "tube " + str(result - 40)
            else:
                result = 20
                message = 'upper X'

        return result, message

    def is_tile_white(self, tile, step=5):
        hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, downWhite, upWhite)
        white_dots, black_dots = self.count_white(mask, step)
        return white_dots > black_dots

    def check_floor(self, frame):
        if self.is_tile_white(self.from_cords_to_slice(frame, self.cords_for_floor), step=2):
            return 1
        return 2

    def edge_check(self, frame_):
        frame_height, frame_width = frame_.shape[:2]
        frame1 = cv2.blur(frame_, [6, 6])
        ImageHSV = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
        xe, ye, we, he = self.search_for_color(ImageHSV, downEdge, upEdge, 20)
        if we >= frame_width * 0.7:
            return 1
        return 0

    def analyse_edges(self, frame_):
        result = []
        for edge in range(len(edge_cords[1])):
            result.append(self.edge_check(self.from_cords_to_slice(frame_, edge_cords[self.elevation][edge])))
        return result[::-1]

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

    def from_15x8_to_8x8(self, m15x8, distance_to_edge):
        if self.robot_orientation % 2 == 0:
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

    def visible_tiles(self, mat):
        cords_of_tiles_on_map = [0, 0]
        if self.robot_orientation == 1:
            cords_of_tiles_on_map = [self.robot_position[0] - 2, self.robot_position[1] - 1]
        elif self.robot_orientation == 2:
            cords_of_tiles_on_map = [self.robot_position[0] - 1, self.robot_position[1] + 1]
        elif self.robot_orientation == 3:
            cords_of_tiles_on_map = [self.robot_position[0] + 1, self.robot_position[1] - 1]
        elif self.robot_orientation == 4:
            cords_of_tiles_on_map = [self.robot_position[0] - 1, self.robot_position[1] - 2]
        width, height = 2 + self.robot_orientation % 2, 3 - self.robot_orientation % 2
        overall_cords = [[cords_of_tiles_on_map[0], cords_of_tiles_on_map[1]],
                         [cords_of_tiles_on_map[0] + width, cords_of_tiles_on_map[1] + height]]
        return self.from_cords_to_slice(mat, overall_cords)

    def scan_frame(self, frame, mat, telemetry=0):
        messages = [['a', 'b', 'c'], ['d', 'e', 'f']]
        elevation_differences = [[0, 0, 0], [0, 0, 0]]

        visible = self.visible_tiles(mat)
        whites = [[0, 0, 0], [0, 0, 0]]

        edges = self.analyse_edges(frame)
        strokes_to_scan = 2
        if sum(edges):
            strokes_to_scan = edges.index(1)  # индекс первой единицы буквально и есть расстояние до края в клетках

        for stroke in range(strokes_to_scan):
            for tile in range(len(elevation_differences[0])):
                if visible[stroke][tile] == 0 or telemetry:
                    local_frame = self.from_cords_to_slice(frame, cords_for_white[self.elevation][stroke][tile])

                    _, __, wb, hb = self.search_for_color(
                        cv2.cvtColor(self.from_cords_to_slice(frame, interest_zones[keys_[2 - self.elevation]][stroke][tile]),
                                     cv2.COLOR_BGR2HSV),
                        downBlue, upBlue)

                    whites[stroke][tile] = self.is_tile_white(local_frame)

                    if wb * hb > 0:
                        elevation_differences[stroke][tile] = 2 - self.elevation
                        visible[stroke][tile], messages[stroke][tile] = self.look_at_tile(
                            self.from_cords_to_slice(frame, interest_zones[keys_[elevation_differences[stroke][tile]]][stroke][tile]), 0,
                            0)

                    else:
                        elevation_differences[stroke][tile] = 3 - (self.elevation + whites[stroke][tile])
                        visible[stroke][tile], messages[stroke][tile] = self.look_at_tile(
                            self.from_cords_to_slice(frame, interest_zones[keys_[elevation_differences[stroke][tile]]][stroke][tile]),
                            whites[stroke][tile], (tile == 1) * (stroke+1))

        if telemetry:
            return messages, elevation_differences

        self.update_map(visible, mat)

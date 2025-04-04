"""
каждой клетке присваивается значение веса, равное количеству новых клеток которых можно увидеть из этой клетки
едем в сторону клетки с наибольшим весом

(возможно добавим краям веса)
"""
import time

import cv2

from emulator import Emulator
import numpy as np
from Future_engeneers_path_creation_new import *
mat = [[42, 10, 10, 10, 10, 10, 10, 10], [64, 10, 20, 10, 10, 34, 32, 10], [64, 10, 20, 20, 10, 10, 10, 10], [64, 10, 20, 20, 20, 34, 20, 41], [10, 10, 33, 20, 10, 10, 20, 20], [10, 10, 32, 20, 20, 20, 34, 71], [32, 52, 20, 34, 10, 10, 10, 10], [10, 20, 20, 34, 20, 20, 20, 34]]
field_mat = np.array(mat)
visible_mat = np.array([[0] * 8] * 8)

weight_mat = np.array([[0] * 8] * 8)
coefficient_mat = np.array([[0, 1, 1, 1, 0],
                            [1, 1, 1, 1, 1],
                            [1, 1, 0, 1, 1],
                            [1, 1, 1, 1, 1],
                            [0, 1, 1, 1, 0]])

coefficient_mat1 = np.array([[1, 1, 1],
                             [1, 0, 1],
                             [1, 1, 1],
                             ])

def sort_coords_by_matrix_values(coords, matrix):
    """
    Сортирует координаты по значениям в матрице в порядке убывания

    Args:
        coords: Список координат в формате [(row1, col1), (row2, col2), ...]
        matrix: 2D матрица (NumPy array или список списков)

    Returns:
        Список координат, отсортированных по убыванию значений в матрице
    """
    # Проверяем, является ли matrix numpy array, если нет - преобразуем
    if not isinstance(matrix, np.ndarray):
        matrix = np.array(matrix)

    # Создаем список кортежей (значение, координата) для сортировки
    value_coord_pairs = []
    for coord in coords:
        row, col = coord
        # Проверяем, что координаты в пределах матрицы
        if 0 <= row < matrix.shape[0] and 0 <= col < matrix.shape[1]:
            value = matrix[row, col]
            value_coord_pairs.append((value, coord))

    # Сортируем по значению в порядке убывания
    value_coord_pairs.sort(key=lambda x: -x[0])

    # Извлекаем только координаты (без значений)
    sorted_coords = [coord for (value, coord) in value_coord_pairs]

    return sorted_coords

def split_dict_by_values_optimized(coord_dict, matrix):
    """
    Оптимизированная версия с использованием list comprehensions
    """
    coords_10 = [
        coord for coord in coord_dict
        if coord[0] < len(matrix) and
           coord[1] < len(matrix[0]) and
           matrix[coord[0]][coord[1]] == 10
    ]

    coords_20 = [
        coord for coord in coord_dict
        if coord[0] < len(matrix) and
           coord[1] < len(matrix[0]) and
           matrix[coord[0]][coord[1]] == 20
    ]

    return coords_10, coords_20

def interest_calculation(field_mat, coef_mat):
    unrevealed = np.array([[1 if cell == 0 else 0 for cell in row] for row in field_mat])
    # print(unrevealed)
    rows, cols = len(field_mat), len(field_mat[0])
    k_rows, k_cols = len(coef_mat), len(coef_mat[0])
    offset_r, offset_c = k_rows // 2, k_cols // 2  # Центр маски

    result = np.array([[0] * cols] * rows)

    for r in range(rows):
        for c in range(cols):
            total = 0
            for kr in range(k_rows):
                for kc in range(k_cols):
                    nr, nc = r + kr - offset_r, c + kc - offset_c
                    if 0 <= nr < rows and 0 <= nc < cols:  # Проверка границ
                        total += unrevealed[nr][nc] * coef_mat[kr][kc]
            result[r][c] = total

    return result


def scan_iteration(field_mat, pos, dir):
    obj = cv2.imread("white_picture.jpg")
    interest = interest_calculation(field_mat, coefficient_mat)
    pos = robot.robot_position
    waves = wave_ini((pos[0], pos[1]), neighbour_ini(field_mat))
    waves_all = []
    for i in waves:
        waves_all += i

    # ------------------- cell to go calculating -------------------#
    revealed = np.array([[0 if cell == 0 else 1 for cell in row] for row in field_mat])
    cords = {}
    for i in range(len(field_mat)):
        for j in range(len(field_mat)):
            cords[(i, j)] = int(revealed[i][j]) * int(interest[i][j])
            interest[i][j] = int(revealed[i][j]) * int(interest[i][j])

    way = []
    good, bad = split_dict_by_values_optimized(cords, field_mat)
    good = sort_coords_by_matrix_values(good, interest)
    bad = sort_coords_by_matrix_values(bad, interest)

    while not way:
        # Prioritize good cells first
        if good and interest[good[0][0]][good[0][1]] > 0:  # Fixed indexing here
            to_go = good[0]
            flag = "good"
        elif bad and interest[bad[0][0]][bad[0][1]] > 0:  # Fixed indexing here
            to_go = bad[0]
            flag = "bad"
        else:
            # No interesting cells left
            pos = robot.robot_position
            if field_mat[pos[0]][pos[1]] == 20:
                print_colored("waves_calculation")
                waves = wave_ini(robot.robot_position, neighbour_ini(field_mat))
                print(waves)

            field_mat[field_mat == 0] = 99
            print(field_mat)
            print(create_path(replace_ints_in_matrix(field_mat), 1))
            return None  # Added return to prevent infinite loop

        con_dict = neighbour_ini(replace_ints_in_matrix(field_mat))
        waves = wave_ini((pos[1], pos[0]), con_dict)

        ini(obj, replace_ints_in_matrix(visible_mat))
        wave_visual(waves, obj)
        cv2.imshow("map", cv2.resize(obj, (600, 600)))
        cv2.waitKey(1)

        way = wave_back_way(waves, (pos[1], pos[0]), to_go, con_dict, 0, obj, field_mat)

        if way and str(field_mat[to_go[0]][to_go[1]])[0] != '3':
            way_visualisation(obj, way[0], 0, 1, (0, 255, 0), 10, 0, replace_ints_in_matrix(field_mat))
            way = way_to_commands_single(way[0], replace_ints_in_matrix(field_mat), int_to_dir(dir))[0]
            return way
        else:
            # Remove unreachable point and try again
            if flag == "good":
                good.pop(0)
                print("Removed unreachable good point:", to_go)
            else:
                bad.pop(0)
                print("Removed unreachable bad point:", to_go)

def full_scan(mat,robot):

    robot.reveal_2x3(mat,visible_mat)
    real_to_emu(robot,"R1",mat)

    robot.reveal_2x3(mat,visible_mat)
    real_to_emu(robot,"R1",mat)

    robot.reveal_2x3(mat, visible_mat)
    real_to_emu(robot, "R1", mat)

    robot.reveal_2x3(mat, visible_mat)
    real_to_emu(robot, "R1", mat)

    robot.show_map(visible_mat,0)
    time.sleep(0.05)

    # надо придумать каким образом починить эту затычку
    # visible_mat[robot.robot_position[0]][robot.robot_position[1]] = 10

    if np.any(mat == 0):
        real_to_emu(robot,scan_iteration(visible_mat,robot.robot_position,robot.robot_orientation),visible_mat)
        return [0]
    return [1, mat]

def real_to_emu(emulator, commands, field):
    """
    Execute robot commands:
    - 'X#' = Move forward # tiles (normal ground)
    - 'F#' = Move forward # tiles (ramp logic)
    - 'L#' = Turn left # times (90° each)
    - 'R#' = Turn right # times (90° each)
    """
    print(commands)
    for cmd in commands:
        if not cmd:
            continue  # Skip empty commands

        action = cmd[0].upper()
        steps = int(cmd[1:]) if len(cmd) > 1 else 1  # Default to 1 step

        if action == 'L':
            for _ in range(steps):
                emulator.turn_robot(-1)  # Left turn
        elif action == 'R':
            for _ in range(steps):
                emulator.turn_robot(1)   # Right turn
        elif action == 'X':
            for _ in range(steps):
                emulator.move_robot_f(field)  # Normal forward movement
        elif action == 'F':
            for _ in range(steps):
                # Ramp movement (same as 'X' but with ramp checks)
                emulator.move_robot_f(field)
        else:
            pass

        emulator.reveal_2x3(field_mat,visible_mat)
        # print(emulator.robot_position, emulator.robot_orientation)
        emulator.show_map(visible_mat,0)
        time.sleep(0.03)

def int_to_dir(int):
    if int == 1: return "U"

    elif int == 2: return "R"

    elif int == 3: return "D"

    else: return "L"

pos = robot_pos_finder(replace_ints_in_matrix(field_mat))
robot = Emulator()
robot.robot_position = [pos[1],pos[0]]

visible_mat[pos[0],pos[1]] = 10

while 1 :
    mat = full_scan(visible_mat,robot)
    if mat[0] != 0:
        break

create_path(mat[1])


# scan_iteration(interest_calculation(field_mat,coefficient_mat),field_mat,(3,5),1)
# ini_for_nerds(replace_ints_in_matrix(field_mat))
# print(coefficient_mat1)
# robot_position = [4, 3]
# robot_orientation = 1
# em.reveal_2x3(robot_position, robot_orientation, field_mat, visible_mat)
# print(visible_mat)
# # print(weight_mat)
# em.show_map(visible_mat, robot_position, robot_orientation)
# em.turn_robot(1)
# em.reveal_2x3(robot_position, robot_orientation, field_mat, visible_mat)
# em.show_map(visible_mat, robot_position, robot_orientation)

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

field_mat = np.array(
[[20, 10, 10, 10, 10, 10, 71, 31], [10, 10, 10, 10, 10, 10, 10, 20], [42, 10, 20, 10, 20, 41, 33, 20], [20, 10, 10, 10, 20, 10, 31, 33], [20, 20, 20, 34, 20, 10, 10, 62], [20, 10, 10, 10, 33, 10, 10, 62], [20, 32, 20, 20, 20, 34, 10, 62], [33, 20, 10, 10, 20, 20, 52, 34]])

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

def scan_iteration(field_mat,pos,dir):
    interest = interest_calculation(field_mat,coefficient_mat)

    # ------------------- cell to go calculating -------------------#
    revealed = np.array([[0 if cell == 0 else 1 for cell in row] for row in field_mat])
    cords = {}
    for i in range(len(field_mat)):
        for j in range(len(field_mat)):
            cords[(i,j)] = int(revealed[i][j])*int(interest[i][j])
            interest[i][j] = int(revealed[i][j])*int(interest[i][j])


    way = []

    good, bad = split_dict_by_values_optimized(cords,field_mat)
    good = sort_coords_by_matrix_values(good,interest)
    bad = sort_coords_by_matrix_values(bad, interest)

    while not way:


        if interest[good[0]] > 0:
            to_go = good[0]
            flag = "good"
        else:
            to_go = bad[0]
            flag = "bad"

        con_dict = neighbour_ini(replace_ints_in_matrix(field_mat))

        waves = wave_ini((pos[1],pos[0]),con_dict)
        obj = cv2.imread("white_picture.jpg")  # картинка для фона

        ini(obj,replace_ints_in_matrix(visible_mat))
        wave_visual(waves,obj)
        cv2.imshow("map", cv2.resize(obj, (600, 600)))
        cv2.waitKey(1)

        way = wave_back_way(waves,(pos[1],pos[0]),to_go,con_dict,0,obj,field_mat)
        print("way", way)
        if way and str(field_mat[to_go[0]][to_go[1]])[0] != 3:

            way_visualisation(obj,way[0],0,1,(0,255,0),10,0,replace_ints_in_matrix(field_mat))
            way = way_to_commands_single(way[0],replace_ints_in_matrix(field_mat),int_to_dir(dir))[0]
            return way
        else:
            if flag == "good":
                good.pop(0)
            else:
                bad.pop(0)

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
    time.sleep(0.2)

    # ------------------- solution ability checking -------------------#
    # tubes = [[1 if (cell > 40 and cell < 53) else 0 for cell in row] for row in mat]
    # if (sum([element for row in tubes for element in row])) == 3:
    #
    #     to_unload = [[1 if cell > 60 else 0 for cell in row] for row in mat]
    #     if (sum([element for row in to_unload for element in row])) > 2:
    #
    #         # one digit mat values may cause some issues
    #         mat[mat == 0] = 99
    #
    #         mat[robot.robot_position[0]][robot.robot_position[1]] = 71
    #
    #         ini_for_nerds(replace_ints_in_matrix(mat))
    #         way = 1
    #         if way:
    #             # return [1, mat]
    #             pass
    #         else:
    #             print_colored("Seems like this thing is impossible to solve tbh", "red")
    #             return exit()

    #todo надо придумать каким образом починить эту затычку
    visible_mat[robot.robot_position[0]][robot.robot_position[1]] = 10

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
        time.sleep(0.1)

def int_to_dir(int):
    if int == 1: return "U"

    elif int == 2: return "R"

    elif int == 3: return "D"

    else: return "L"

pos = robot_pos_finder(replace_ints_in_matrix(field_mat))
robot = Emulator()
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


import math
import time

import cv2
from exel_stuff import *
from emulator import Emulator
import numpy as np
from Future_engeneers_path_creation_new import *

mat = rand_pat_from_file()
mat = string_to_list(mat)
field_mat = np.array(mat)
# print(field_mat)

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

def ramp_pair_finder(mat):
    possible_pairs = []
    # print(mat)

    for i in range(len(mat)-1):
        for j in range(len(mat)-1):
            if mat[i][j] + mat[i+1][j] == 64 and (mat[i][j]!= 0 and mat[i][j] != 64):
                possible_pairs.append([(i,j), (i+1,j)])
            elif mat[i][j] + mat[i][j+1] == 66:
                possible_pairs.append([(i,j), (i,j+1)])

    for i in possible_pairs:
        if borders_with_zero(mat, i[0]):
            return i[0]
        elif borders_with_zero(mat, i[1]):
            return i[1]

def borders_with_zero(mat, coord):
    y, x = coord  # распаковываем координаты
    rows = len(mat)
    if rows == 0:
        return False
    cols = len(mat[0])

    # Проверяем соседние клетки (верх, низ, лево, право)
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny = y + dy
        nx = x + dx
        if 0 <= ny < rows and 0 <= nx < cols:
            if mat[ny][nx] == 0:
                return True
    return False

def borders_with_tube(mat, coord):
    y, x = coord  # распаковываем координаты
    rows = len(mat)
    if rows == 0:
        return False
    cols = len(mat[0])

    # Проверяем соседние клетки (верх, низ, лево, право)
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny = y + dy
        nx = x + dx
        if 0 <= ny < rows and 0 <= nx < cols:
            if str(mat[ny][nx])[0] == "5" or str(mat[ny][nx])[0] == "4" or str(mat[ny][nx])[0] == "6":
                return True
    return False

def scan_iteration(field_mat, pos, dir, obj):
    interest = interest_calculation(field_mat, coefficient_mat)

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
        # Check if we have any points left to consider
        if not good and not bad:
            # Handle case when no points are left
            tubes = np.char.startswith(field_mat.astype(str), '4')
            tubes = np.sum(tubes)

            tubes_1 = np.char.startswith(field_mat.astype(str), '5')
            tubes_1 = np.sum(tubes_1)


            to_unload = np.char.startswith(field_mat.astype(str), '6')
            to_unload = np.sum(to_unload)

            if tubes + tubes_1 + to_unload < 6:
                print_colored("our last chance", "red")
                print(field_mat)
                print("\n\n", tubes, to_unload)
                to_go = ramp_pair_finder(field_mat)
                # cv2.waitKey()

                con_dict = neighbour_ini(replace_ints_in_matrix(field_mat))
                waves = wave_ini((pos[1], pos[0]), con_dict)
                way = wave_back_way(waves, (pos[1], pos[0]), to_go, con_dict, 0, obj, field_mat)
                print(way)

                ini(obj, replace_ints_in_matrix(visible_mat))
                wave_visual(waves, obj)
                cv2.imshow("map", cv2.resize(obj, (600, 600)))
                cv2.waitKey(1)

                way_visualisation(obj, way[0], 0, 1, (0, 255, 0), 10, 0, replace_ints_in_matrix(field_mat))
                way = way_to_commands_single(way[0], replace_ints_in_matrix(field_mat), int_to_dir(robot.robot_orientation))[0]
                way += "X1"
                return  way
            else:
                return "scanned"

        # Prioritize good cells first
        if good and interest[good[0][0]][good[0][1]] > 0:
            to_go = good[0]
            flag = "good"
        elif bad and interest[bad[0][0]][bad[0][1]] > 0:
            to_go = bad[0]
            flag = "bad"
        else:
            # If we get here, it means we have lists but all points have interest <= 0
            # We should remove these points and try again
            if good:
                good.pop(0)
                continue
            if bad:
                bad.pop(0)
                continue

        con_dict = neighbour_ini(replace_ints_in_matrix(field_mat))
        waves = wave_ini((pos[1], pos[0]), con_dict)

        way = wave_back_way(waves, (pos[1], pos[0]), to_go, con_dict, 0, obj, field_mat)

        if way and str(field_mat[to_go[0]][to_go[1]])[0] != '3':
            ini(obj, replace_ints_in_matrix(visible_mat))
            wave_visual(waves, obj)
            cv2.imshow("map", cv2.resize(obj, (600, 600)))
            cv2.waitKey(1)

            way_visualisation(obj, way[0], 0, 1, (0, 255, 0), 10, 0, replace_ints_in_matrix(field_mat))
            way = way_to_commands_single(way[0], replace_ints_in_matrix(field_mat), int_to_dir(dir))[0]
            return way
        else:
            # Remove unreachable point and try again
            if flag == "good" and good:  # Added check for non-empty list
                good.pop(0)
                print("Removed unreachable good point:", to_go)
            elif bad:  # Added check for non-empty list
                bad.pop(0)
                print("Removed unreachable bad point:", to_go)
            else:
                print("No more points to try")
                return None

def full_scan(mat,robot):
    obj = cv2.imread("white_picture.jpg")

    way_to_scan = scan_iteration(visible_mat,robot.robot_position,robot.robot_orientation, obj)
    if  way_to_scan != "scanned":
        real_to_emu(robot,way_to_scan,visible_mat)

        robot.reveal_2x3(mat, visible_mat)
        real_to_emu(robot, "R1", mat)

        robot.reveal_2x3(mat, visible_mat)
        real_to_emu(robot, "R1", mat)

        robot.reveal_2x3(mat, visible_mat)
        real_to_emu(robot, "R1", mat)

        robot.reveal_2x3(mat, visible_mat)
        real_to_emu(robot, "R1", mat)

        robot.show_map(visible_mat, 0)
        time.sleep(0.05)

    else:
        print_colored("Lets start our solution", "green")
        pos = robot.robot_position

        if mat[pos[1]][pos[0]] == 20:
            waves = wave_ini((pos[1],pos[0]), neighbour_ini(replace_ints_in_matrix(mat)))

            closest_1st_f = []
            for i in waves:
                for j in i:
                    if mat[j[0]][j[1]] == 10:
                        closest_1st_f = j
                        break
                if closest_1st_f:
                    break

            print(closest_1st_f)
            way = wave_back_way(waves, (pos[1],pos[0]), closest_1st_f, neighbour_ini(replace_ints_in_matrix(mat)), 0 ,obj,replace_ints_in_matrix(mat),0)
            way_visualisation(obj, way[0], 0, 1, (0, 255, 0), 10, 0, replace_ints_in_matrix(field_mat))
            # cv2.waitKey()
            way = way_to_commands_single(way[0],mat,int_to_dir(robot.robot_orientation))
            real_to_emu(robot,way[0],mat)

        pos = robot.robot_position

        if borders_with_tube(mat, (pos[1], pos[0])):
            waves = wave_ini((pos[1], pos[0]), neighbour_ini(replace_ints_in_matrix(mat)))

            closest_no_t = []
            for i in waves:
                for j in i:
                    if not borders_with_tube(mat, (j[0], j[1])):
                        closest_no_t = j
                        break
                if closest_no_t:
                    break

            way = wave_back_way(waves, (pos[1], pos[0]), closest_no_t, neighbour_ini(replace_ints_in_matrix(mat)),
                                0, obj, replace_ints_in_matrix(mat), 0)
            way_visualisation(obj, way[0], 0, 1, (0, 255, 0), 10, 0, replace_ints_in_matrix(field_mat))
            cv2.waitKey()
            way = way_to_commands_single(way[0], replace_ints_in_matrix(mat), int_to_dir(robot.robot_orientation))
            real_to_emu(robot, way[0], mat)
            pos = robot.robot_position


        mat[mat == 0] = 99
        mat[pos[1]][pos[0]] = 71
        while robot.robot_orientation != 1:
            robot.turn_robot(1)

        ini_for_nerds(replace_ints_in_matrix(mat))
        # cv2.waitKey()


        way = create_path(mat, 1)
        print(way)
        if way:
            return way , 1
        else:
            print_colored("Failed to solve, seems like wrong scan", "red")
            return

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
while 1 :
    mat = full_scan(visible_mat,robot)
    if mat:
        break

print(mat[0])



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

"""
каждой клетке присваивается значение веса, равное количеству новых клеток которых можно увидеть из этой клетки
едем в сторону клетки с наибольшим весом

(возможно добавим краям веса)
"""
from emulator import *
import numpy as np
from Future_engeneers_path_creation_new import *

em = emulator
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

def border_find(interest,mat,pos,dir):
    revealed = np.array([[0 if cell == 0 else 1 for cell in row] for row in field_mat])
    cords = {}
    for i in range(len(field_mat)):
        for j in range(len(field_mat)):
            cords[(i,j)] = revealed[i][j]*interest[i][j]
    way = []
    while not way:
        to_go = max(cords.values())
        for key, val in cords.items():
            if val == to_go:
                to_go = key
                break
        con_dict = neighbour_ini(replace_ints_in_matrix(mat))
        waves = wave_ini(pos,con_dict)
        way = wave_back_way(waves,pos,to_go,con_dict,0,None,mat)
        if way:
            way = way_to_commands([way,0],field_mat)
            print("way")
        else:
            del cords[to_go]


border_find(interest_calculation(field_mat,coefficient_mat),field_mat,(3,5),1)

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

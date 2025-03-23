"""
каждой клетке присваивается значение веса, равное количеству новых клеток которых можно увидеть из этой клетки
едем в сторону клетки с наибольшим весом

(возможно добавим краям веса)
"""
import time
import numpy as np
from emulator import Emulator

em = Emulator()
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


em.show_map(field_mat)



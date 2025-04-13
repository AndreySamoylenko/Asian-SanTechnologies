import cv2
import copy
from Future_engeneers_path_creation_new import create_path, ini_for_nerds, replace_ints_in_matrix

mat = [[41, 33, 61, 61, 61, 20, 71, 10],
       [10, 20, 10, 10, 10, 20, 33, 10],
       [10, 20, 10, 33, 10, 31, 20, 10],
       [10, 20, 10, 31, 10, 10, 10, 10],
       [10, 10, 10, 33, 41, 10, 20, 20],
       [20, 20, 32, 20, 34, 32, 20, 52],
       [10, 10, 10, 10, 10, 10, 10, 10],
       [10, 10, 10, 10, 10, 10, 10, 10]]
way = create_path(mat,1)
ini_for_nerds(replace_ints_in_matrix(mat))
# print((0,0) == [0,0])
# print(replace_ints_in_matrix(mat))

# cv2.waitKey(0)
#
# fix case when start point = finish point (can be brain damaging task)
# add unload path building (rn it only gets to the closest unload point) (if closest unload point = point to pick up tube it wont work properly because of previous problem)
# make code a little bit more readable (rn it really messy)

# (important) - add to final str unload variant (1!!!!1!!!1!!)


# def border_find(interest,mat,pos,dir):
#     revealed = np.array([[0 if cell == 0 else 1 for cell in row] for row in field_mat])
#     cords = {}
#     for i in range(len(field_mat)):
#         for j in range(len(field_mat)):
#             cords[(i,j)] = revealed[i][j]*interest[i][j]
#     way = []
#     while not way:
#         to_go = max(cords.values())
#         for key, val in cords.items():
#             if val == to_go:
#                 to_go = key
#                 break
#         con_dict = neighbour_ini(replace_ints_in_matrix(mat))
#         waves = wave_ini(pos,con_dict)
#         way = wave_back_way(waves,pos,to_go,con_dict,0,None,mat)
#         if way:
#             way = way_to_commands([way,0],field_mat)
#             print("way")
#         else:
#             del cords[to_go]
#
#
# border_find(interest_calculation(field_mat,coefficient_mat),field_mat,(3,5),1)
def get_3x2_area_safe(matrix, center_x, center_y, direction):
    """
    Возвращает область 3x2 из матрицы, заменяя отсутствующие клетки на 0

    Параметры:
        matrix: входная матрица (2D список/массив)
        center_x, center_y: центральные координаты
        direction: направление (1 - вверх, 2 - вправо, 3 - вниз, 4 - влево)

    Возвращает:
        Список списков - область 3x2, где отсутствующие клетки заменены на 0
    """
    rows = len(matrix)
    if rows == 0:
        return [[0] * 3, [0] * 3] if direction in [1, 3] else [[0] * 2] * 3

    cols = len(matrix[0])
    result = []

    # Определяем смещения для разных направлений
    if direction == 1:  # Вверх
        offsets = [(-2, -1), (-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1)]
        row_len = 3
    elif direction == 2:  # Вправо
        offsets = [(-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
        row_len = 2
    elif direction == 3:  # Вниз
        offsets = [(1, -1), (1, 0), (1, 1), (2, -1), (2, 0), (2, 1)]
        row_len = 3
    elif direction == 4:  # Влево
        offsets = [(-1, -2), (0, -2), (1, -2), (-1, -1), (0, -1), (1, -1)]
        row_len = 2
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

    # Формируем результат в виде строк
    if direction in [1, 3]:  # Для вверх/вниз - 2 строки по 3 элемента
        return [values[:3], values[3:]]
    else:  # Для вправо/влево - 3 строки по 2 элемента
        return [values[i:i + 2] for i in range(0, 6, 2)]

import math
from copy import deepcopy
from os import system, name

import cv2 #что бы окошки выводить
# from playsound3 import playsound #что бы звуки включать
import time #что бы время считать

# import ctypes #что бы иконку окна менять
import itertools #что бы проще составлять все возможные комбинации
import copy # что бы list = list1 работало нормально
from itertools import groupby #et hz zachem
import re
import os
import numpy as np
#
# def icon_change():
#     icon_path = "random_funny_stuff/cute_icon.ico"  # Я не знаю как оно работает, если честно, я украл этот код
#
#     icon = ctypes.windll.user32.LoadImageW(0, icon_path, 1, 0, 0, 0x00000010)
#     hwnd = ctypes.windll.user32.FindWindowW(None, "map")
#
#     if hwnd:
#         ctypes.windll.user32.SendMessageW(hwnd, 128, 0, icon)
def replace_ints_in_matrix(matrix):

    replacements = {
        10: 70,
        20: 10,
        32: 33,
        33: 30,
        34: 32,
        41: 7040,
        42: 7041,
        51: 1140,
        52: 1141,
        61: 60,
        62: 63,
        63: 61,
        64: 62,
        71: 7050,
        72: 7052,
        73: 7051,
        74: 7053,
        99: 99
    }

    new_matrix = []
    for row in matrix:
        new_row = []
        for element in row:
            if element in replacements:
                new_row.append(replacements[element])
            else:
                new_row.append(element)
        new_matrix.append(new_row)

    return new_matrix

def ini(img, mat): #вывод объектов на экран
    if mat is not None:
        for i in range(len(mat)): # перебираем каждый элемент матрицы и выводим его
            for j in range(len(mat[i])):
                show_smth(mat[i][j], (i, j), img, mat)
        cv2.imshow("map", cv2.resize(img, (600, 600)))
        cv2.waitKey(1)
    else:
        print("Field mat can't be non type object! \n   Programmer u are dummy ass")

def show_smth(code, cords, object, mat = []):
    # Precompute coordinates first (faster to do multiplication once)
    y_start = 100 * cords[0]
    x_start = 100 * cords[1]
    y_end = y_start + 100
    x_end = x_start + 100

    # Code replacement (simplified condition)
    code = 1141 if code == 1041 else code

    # Try fast path first
    try:
        pic = cv2.imread(f"field_pics/{code}.png", cv2.IMREAD_UNCHANGED)
        if pic is not None and pic.shape[0] == 100 and pic.shape[1] == 100:
            # Direct assignment
            object[y_start:y_end, x_start:x_end] = pic
            return
    except:
        pass

    # Fallback path with boundary checks
    height, width = object.shape[:2]
    y_start = max(0, min(y_start, height - 100))
    x_start = max(0, min(x_start, width - 100))

    # Create red placeholder (slightly faster than full array assignment)
    object[y_start:y_start + 100, x_start:x_start + 100] = (0, 0, 255)

def neighbour_ini(mat):          #определение клеток в которые можно пройти
    #если хочешь что-то менять - помни про инвертированные координаты, i это у, а j это х
    #еще в словаре хранятся координаты вида (y,x) просто так удобнее
    #функция работает с любым размером матрицы который больше 1х1
    #если ты реально собрался что-то менять - good luck)

    neighbour_dict = {}
    for i in range(len(mat)): #для каждого ряда
        for j in range(len(mat[i])): # для каждого элемента каждого ряда
            neighbour_dict[(i, j)] = [] #создание пустого списка клеток в которые можно пройти из конкретной клетки
            if mat[i][j] == 70: #если клетка из которой идем - первый этаж

                if i + 1 < len(mat) and ((mat[i + 1][j] == 70) or (mat[i + 1][j] == 30)): #если при попытке пройти в + по у мы не выйдем за пределы поля и клетка в которую идем - элемент первого этажа или рампа направленная в нужную сторону то записываем ее в список
                    # print("success")
                    neighbour_dict[(i, j)].append((i + 1, j)) #добавляем в список возможных клеток исходную с измененной координатой

                if i - 1 > -1 and (mat[i - 1][j] == 70 or mat[i - 1][j] == 31):
                    # действуем по аналогии с первым случаем, только рампа в этом случае будет другая тк идем в другую сторону
                    neighbour_dict[(i, j)].append((i - 1, j))

                if j - 1 > -1 and (mat[i][j - 1] == 70 or mat[i][j - 1] == 32):
                    # то же самое
                    neighbour_dict[(i, j)].append((i, j - 1))

                if j + 1 < len(mat[i]) and (mat[i][j + 1] == 70 or mat[i][j + 1] == 33):
                    # то же самое
                    neighbour_dict[(i, j)].append((i, j + 1))


            #todo uncomment to move freely on sec floor

            elif int(str(mat[i][j])[0]) == 1: # если клетка из которой мы ищем возможные проходы - второй этаж
                if i + 1 < len(mat) and ((mat[i + 1][j] == 11 or mat[i + 1][j] == 10) or (mat[i + 1][j] == 31)): #не выходим за матрицу и клетка в которую хотим пройти - элемент второго этажа или рампа на съезд
                    # добавляем клетку с измененной координатой
                    neighbour_dict[(i, j)].append((i + 1, j))

                if i - 1 > -1 and ((mat[i - 1][j] == 11 or mat[i - 1][j] == 10) or mat[i - 1][j] == 30):
                    # делаем все тоже
                    neighbour_dict[(i, j)].append((i - 1, j))

                if j - 1 > -1 and ((mat[i][j - 1] == 10 or mat[i][j - 1] == 11) or mat[i][j - 1] == 33):
                    # и тут
                    neighbour_dict[(i, j)].append((i, j - 1))

                if j + 1 < len(mat[i]) and ((mat[i][j + 1] == 11 or mat[i][j + 1] == 10) or mat[i][j + 1] == 32):
                    # этот код достаточно однообразный
                    neighbour_dict[(i, j)].append((i, j + 1))


            #todo comment this piece if u gonna move freely on sec floor
            #todo start

            # elif int(str(mat[i][j])) == 10: # если клетка из которой мы ищем возможные проходы - второй этаж
            #
            #     if j - 1 > -1 and ((mat[i][j - 1] == 10) or mat[i][j - 1] == 33):
            #         # и тут
            #         neighbour_dict[(i, j)].append((i, j - 1))
            #
            #     if j + 1 < 8 and ((mat[i][j + 1] == 10) or mat[i][j + 1] == 32):
            #         # этот код достаточно однообразный
            #         neighbour_dict[(i, j)].append((i, j + 1))
            #
            #
            # elif int(str(mat[i][j])) == 11: # если клетка из которой мы ищем возможные проходы - второй этаж
            #
            #     if i + 1 < 8 and ((mat[i + 1][j] == 11) or (mat[i + 1][j] == 31)): #не выходим за матрицу и клетка в которую хотим пройти - элемент второго этажа или рампа на съезд
            #         # добавляем клетку с измененной координатой
            #         neighbour_dict[(i, j)].append((i + 1, j))
            #
            #     if i - 1 > -1 and ((mat[i - 1][j] == 11) or mat[i - 1][j] == 30):
            #         # делаем все тоже
            #         neighbour_dict[(i, j)].append((i - 1, j))


            #todo end


            elif int(str(mat[i][j])[0]) == 3: #если рампа
                # я не придумал ничего лучше рассматривания частных случаев, где можно проехать либо на второй этаж либо на другую рампу
                if mat[i][j] == 30:
                    if i+1 < len(mat) and (mat[i + 1][j] == 10 or mat[i + 1][j] == 11 or mat[i + 1][j] == 31):
                        neighbour_dict[(i, j)].append((i + 1, j))

                    if i - 1 > -1 and (mat[i - 1][j] == 70 or mat[i - 1][j] == 31):
                        neighbour_dict[(i, j)].append((i - 1, j))


                elif mat[i][j] == 31: # я реально рассматриваю все 4 рампы
                    if i + 1 < len(mat) and (mat[i + 1][j] == 70 or mat[i + 1][j] == 30):
                        neighbour_dict[(i, j)].append((i + 1, j))

                    if i - 1 > -1 and (mat[i - 1][j] == 10 or mat[i - 1][j] == 11 or mat[i - 1][j] == 30):
                        neighbour_dict[(i, j)].append((i - 1, j))

                elif mat[i][j] == 32: #это немного неэффективно
                    if j + 1 < len(mat[0]) and (mat[i][j + 1] == 70 or mat[i][j + 1] == 33):
                        neighbour_dict[(i, j)].append((i, j + 1))

                    if j - 1 > -1 and (mat[i][j - 1] == 10 or mat[i][j - 1] == 11 or mat[i][j - 1] == 11 or mat[i][j - 1] == 33):
                        neighbour_dict[(i, j)].append((i, j - 1))

                elif mat[i][j] == 33: #но в принципе пофиг
                    if j - 1 > -1 and (mat[i][j - 1] == 70 or mat[i][j - 1] == 32):
                        neighbour_dict[(i, j)].append((i, j - 1))

                    if j + 1 < len(mat[0]) and (mat[i][j + 1] == 10 or mat[i][j + 1] == 11 or mat[i][j + 1] == 11 or mat[i][j + 1] == 32):
                        neighbour_dict[(i, j)].append((i, j + 1))





    return (neighbour_dict)

def interpolate_color(t):
    if (t < 1 or t == 1) and (t > 0 or t ==0):
        #переводит значение от нуля до единицы в цвет от красного до синего, думаю мне не нужно это объяснять
        light_blue = (75, 120, 230)
        bright_red = (255, 0, 0)
        t = t - 0.05
        red = int(light_blue[0] + (bright_red[0] - light_blue[0]) * t)
        green = 0
        blue = int(light_blue[2] + (bright_red[2] - light_blue[2]) * t)

        return red, green, blue
    else:
        print("Fail during colour interpolation! arg can't be > 1 or < 0 !  \n arg:", t)
        return None

def wave_frame_displaying(cords, w_num, max_w_num, object, toggle_ramk = 1, toggle_mycolor = None, custom_num = 0,line_smth = (3,0.8), mat = []):
    #эта штука выводит один квадрат сетки волн + цифру
    add = 20
    if not toggle_mycolor:
        w_to_map = max_w_num - w_num #тк 1 - синий, а 0 - красный нам нужно инвертировать номер волны
        w_mapped = scale_value(w_to_map, 0, max_w_num, 0, 1) #маппинг номера волны от 0 до одного
        add = 20 #добавления отступа для двухзначных чисел
        if len(str(w_num)) == 2:
            add = 5

    if toggle_ramk:
        if not toggle_mycolor:
            cv2.rectangle(object, (cords[1] * 100, cords[0] * 100), (cords[1] * 100 + 100, cords[0] * 100 + 100),
                          interpolate_color(w_mapped), line_smth[0]) #рисуем прямоугольник
        if toggle_mycolor:
            cv2.rectangle(object, (cords[1] * 100, cords[0] * 100), (cords[1] * 100 + 100, cords[0] * 100 + 100),
                          toggle_mycolor, line_smth[0])  # рисуем прямоугольник

    if not toggle_mycolor:
        cv2.putText(object, str(w_num), ((cords[1] - 1) * 100 + 160 + add, cords[0] * 100 + 90), cv2.FONT_HERSHEY_SIMPLEX, line_smth[1],
                    interpolate_color(w_mapped), 2) #рисуем текст (числа после плюса подобраны вручную хд)

    else:
        cv2.putText(object, str(custom_num), ((cords[1] - 1) * 100 + 90 + add, cords[0] * 100 + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0,250,0),2) #рисуем текст (числа после плюса подобраны вручную хд)

def scale_value(value, from_min, from_max, to_min, to_max):
    normalized_value = (value - from_min) / (from_max - from_min)  # map() из ардуино но в питоне

    scaled_value = to_min + normalized_value * (to_max - to_min)

    return scaled_value

def wave_ini(p_start, connections_dict):
    # построение волны
    waves = [[p_start]]

    while len(waves[-1]) != 0: #пока длина последней построенной волны не равна 0
        waves.append([]) #добавляем к списку с волнами пустой список

        for i in range(len(waves[-2])): # перебираем все точки из предыдущей волны
            all_waves = []

            for k in waves: # создание списка всех точек всех волн, что бы избежать повторения
                for q in k:
                    all_waves.append(q)

            # print(connections_dict[waves[-2][i]])
            for j in range(len(connections_dict[waves[-2][i]])): #для всех точек, в которые можно пройти из выбранной точки предыдущей волны

                if connections_dict[waves[-2][i]][j] not in all_waves: #если точка в которую можно пройти из выбранной точки прошлой волны еще не использована - добавляем ее в текущую волну
                   # ps -2 - индекс прошлой волны, i - индекс конкретного элемента этой волны. Это ключ к элементу словаря,который содержит все клетки в которые можно пройти. j - индекс конкретной клетки в которую можно пройти
                    waves[-1].append(connections_dict[waves[-2][i]][j])
                    # на следующем повторении цикла текущая волна станет прошлой и так пока есть куда идти

    return waves

def wave_visual(wave_list, object):
    for i in range(len(wave_list)): # перебираем все элементы списка с волнами, что бы визуализировать его на картинке
        for j in range(len(wave_list[i])):
            wave_frame_displaying(wave_list[i][j], i, len(wave_list) - 1, object)
    cv2.imshow("map", cv2.resize(object, (600, 600)))


def tuples_to_lists(tuples_list):
  return [list(tup) for tup in tuples_list] #thats dummy...

def wave_back_way(waves, p1, p2, dict, lenght_debugging,object,field_mat, max_lenght = None,):
    # global smth_for_ramps
    smth_for_ramps = True
    print("creating path", p1, p2)

    way = [p2]  # построение обратного маршрута
    all_waves = []
    final_app = 0

    for i in waves: #список всех элементов всех волн
        for j in i:
            all_waves.append(j)


    if p1 == p2:
        if lenght_debugging:
            print("Start and finish points can't be same! \n Points:", p1, p2)
        return [[p1],0]

    if p1 != waves[0][0]:
        if lenght_debugging:
            print("Error! start point of wave and start point of path are not same!", "\n", "start point of wave: ", waves[0][0], " start point of path: " , p1)
        return None

    if p2 not in all_waves:
        if lenght_debugging:
            print("cant find path", "pt 1:", p1, "pt 2:", p2)
        return None

    while 1:
        pre_app = ()
        possible_moves = dict[way[-1]] # берем последний элемент построенного пути и смотрим куда из него можно пройти
        min_num = 1000 #очень надеюсь что будет меньше 1000 волн...

        for i in range(len(possible_moves)): #для каждой возможной клетки
            for j in waves:
                if possible_moves[i] in j: # если клетка в которую можно пройти находится в одной из волн то
                    if waves.index(j) < min_num: # если индекс волны меньше минимального
                        min_num = waves.index(j) #перезаписываем минимальный индекс
                        pre_app = possible_moves[i] #перезаписываем клетку в которую хотим ходить



        if str(field_mat[pre_app[0]][pre_app[1]])[0] == "3": #"реальная" длина (с длиной рамп)
            final_app+=2

        # по итогам цикла получаем клетку с наименьшим номером волны, ее и записываем
        way.append(pre_app)

        if max_lenght: #аргумент из штук с рампами что бы не строить маршрут если он уже длиннее минимального
            if len(way)+final_app >= max_lenght:
                return None

        if way[-1] == p1: #если пришли в исходную точку (маршрут построен)
            imposters = [] #рампы

            if final_app != 0 and smth_for_ramps == False: #никакой рекурсии!)

                if lenght_debugging == 2:
                    print("Seems like theres ramps on our way... \n Lets try to reconstruct it!")
                    print("current lenght:", len(way)+final_app)

                smth_for_ramps = True
                way_with_ramps = ramp_security_control(imposters,lenght_debugging,len(way)+final_app,dict,object,p1,p2,field_mat) #вызываем функцию ре-маршрутизации

                if way_with_ramps: #если она что-то вернула
                    if lenght_debugging == 2:
                        print("Path recreated successfully p1:", p1, " ", "p2: ", p2, "\n          ", "lenght: ",
                              way_with_ramps[1])
                    return way_with_ramps

            if lenght_debugging == 2:
                print("Path created successfully p1:", p1, " ", "p2: ", p2, "\n          ", "lenght: ", str(len(way)+final_app))

            if way:
                way = way[::-1] #инвертирование пути тк строим от обратного
                return [way, len(way)+final_app]

            else:
                return None #по идее такого случая не может быть, но мало ли

def ramp_security_control(ramps,debugging,current_len,dict,object,p1,p2,field_mat):
        #этот прикол надо бы оптимизировать
        #если в рампу нельзя проехать, ее стоит не учитывать
        #если рампы стоят рядом друг с другом - аля спуск-подъем тогда берем их за один элемент
        #надо добавить рекурсию промежуточных маршрутов - если есть рампы которых нет в списке перебираемых - запускаем эту же функцию, но с новыми рампами а то есть варианты когда эта штука может не сработать но шанс этого просто мегамаленький
        #еще нужна макс длина маршрута в качестве аргумента, что бы по достижении ее wave_back_way переставал считать дальше
        ramps = []
        max_lenght = 1000
        #print(current_len)

        # while 1:
        #     print("hehe")

        for i in range(8):
            for j in range(8):
                if list(str(field_mat[i][j]))[0] == "3":
                    ramps.append((i,j))

        global smth_for_ramps

        dict_to_change = copy.deepcopy(dict) #очень странная штука, copy.copy не работало а deepcopy работает (i have no clue why)
        all_path_dict = {}
        all_len_list = []


        ramps_combinations = all_combinations(ramps) #все комбинации из рамп маршрута, вообще можно было бы сделать комбинацию из всех рамп на поле, но питон не вывозит
        for i in range(len(ramps_combinations)): #для всех комбинаций рамп
            for j in range(len(ramps_combinations[i])): #для всех рамп в комбинации
                for k in range(8): #для всей
                    for m in range(8): #матрицы
                        for n in range(len(dict_to_change[(k,m)])): #для всех клеток в которые можно пройти из конкретной клетки матрицы
                            if ramps_combinations[i][j] in dict_to_change[(k,m)]: #если в рампу из комбинации можно пройти то
                                dict_to_change[(k,m)].remove(ramps_combinations[i][j]) #теперь в нее нельзя пройти хехе

            wave_list = wave_ini(p1,dict_to_change)

            way = wave_back_way(wave_list,p1,p2,dict_to_change,0,object,field_mat, max_lenght) #ищем путь, но с забанеными рампами
            dict_to_change = copy.deepcopy(dict) #возвращаем словарь с клетками куда можно пройти к нормальному виду

            if way: #если путь существует

                if way[1] < max_lenght:
                    max_lenght = way[1]

                final_app = 0 #считаем "настоящую длину" (с учетом рамп)

                for z in range(len(way)):
                    if list(str(field_mat[way[0][z][0]][way[0][z][1]]))[0] == "3": #эти индексы...
                        #print("appended")
                        final_app += 2

                all_path_dict[way[1]+final_app] = way[0] #добавляем путь в словарь всех путей (пофигу что пути с одинаковой длиной будут перезаписываться)
                all_len_list.append(way[1]+final_app)

        smth_for_ramps = False #перед ретерном возвращаем "предохранитель" от бесконечной рекурсии

        if len(all_len_list) > 0 and min(all_len_list) < current_len: #если новый маршрут короче старого: а то мало ли что там создалось
            if debugging:
                ini(object,field_mat) #рисуем крутой маршрут
                whats_that = wave_ini(p1,dict)
                wave_visual(whats_that,object)
            return all_path_dict[min(all_len_list)], min(all_len_list) #return маршрута (инвертированного) + длины (его же)

        else:
            ini(object, field_mat) #если нет, возвращаем ничего и функция вейв бек все поймет и отрисует начальный маршрут
            whats_that = wave_ini(p1, dict)
            wave_visual(whats_that, object)
            return None

def way_visualisation(object, way, funny_sound, anim, color = (0,255,0), thickness = 10,delta = 0,field_mat = []):
    if way:
        for i in range(len(way)-1):
            cv2.line(object,(way[i][1]*100 + 30 + delta*10, way[i][0]*100 + 30+delta*10 ),(way[i+1][1]*100 + 30+delta*10 , way[i+1][0]*100 + 30+ delta*10),color,thickness)
            cv2.imshow("map", cv2.resize(object, (600, 600)))
            cv2.waitKey(1)

        if anim:
            dir = 0
            for j in range(len(way) - 1):

                if way[j][1] == way[j + 1][1] + 1:
                    dir = 3

                elif way[j][1] == way[j + 1][1] - 1:
                    dir = 2

                elif way[j][0] == way[j + 1][0] + 1:
                    dir = 0

                elif way[j][0] == way[j + 1][0] - 1:
                    dir = 1

                if j > 0:
                    show_smth(field_mat[way[j-1][0]][way[j-1][1]],way[j-1],object)

                show_smth("705"+str(dir),way[j],object)
                cv2.imshow("map", cv2.resize(object, (600, 600)))
                cv2.waitKey(1)


                time.sleep(0.08)

            show_smth(field_mat[way[-2][0]][way[-2][1]], way[-2], object)
            show_smth("705" + str(dir), way[-1], object)
            cv2.imshow("map", cv2.resize(object, (600, 600)))
            cv2.waitKey(1)


def all_combinations(elements):
    combinations = []

    for r in range(1, len(elements) + 1):
        combinations.extend(itertools.combinations(elements, r))

    return combinations

def all_permutations(elements):
  # Генерация всех перестановок
  permutations = list(itertools.permutations(elements))
  return permutations

def get_colors(option):
  if option == 1: #что бы финальный маршрут был нагляднее
    return 0, 0, 255
  elif option == 2:
    return  0, 255, 255
  elif option == 3:
    return 192, 192, 0
  else:
    return 255, 0, 0

def print_colored(text, color='white'):
  # ANSI escape codes for text coloring
  #если честно, я не знаю как это работает
  colors = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m', # Reset to default color
  }
  color_code = colors.get(color, colors['white'])
  print(f"{color_code}{text}{colors['reset']}")

def remove_duplicates(input_list):
  seen = set()
  result = []
  for item in input_list:
    if item not in seen:
      seen.add(item)
      result.append(item)
  return result

def clear():
    # for windows the name is 'nt'
    if name == 'nt':
        _ = system('cls')

    # and for mac and linux, the os.name is 'posix'
    else:
        _ = system('clear')

def robot_pos_finder(field_mat, remove_robot = True):
    # ---------------pos detecting ------------------#
    print(field_mat)

    my_pos = []
    for i in range(len(field_mat)):
        for j in range(len(field_mat[0])):

            if str(field_mat[i][j])[-2] == "5":

                if str(field_mat[i][j])[0] == "7":
                    my_pos = (i, j)
                    if remove_robot:
                        field_mat[i][j] = 70
                    print_colored(my_pos,"red")

                    return my_pos

                else:
                    print_colored("Dont ready for robot on second floor!1", "red")
                print_colored("\n\n         FAILED", "red")

    print_colored("Cant solve cause no robot", "red")

def pick_up_points_find(field_mat, waves_all):
    # --------------tubes pick up points finding------------------#
    cells_to_tubes_dict = {}
    tubes = []
    cell_to_tube = []
    for i in range(len(field_mat)):  # поиск клеток из которых можно забрать трубы (записывается в словарь вида труба - список клеток)
        for j in range(len(field_mat[0])):
            # PS str(field_mat[i][j])[0] == str(field_mat[i][j-1])[0] - проверка на этажность. Если есть идеи как сделать проще то было бы славно

            if list(str(field_mat[i][j]))[-2] == "4": #если клетка - труба

                cells_to_tubes_dict[(i, j)] = []
                tubes.append((i, j))

                if list(str(field_mat[i][j]))[-1] == "1":  # смотрим куда повернута труба
                    # print((i,j),1)
                    # print(waves_all)

                    if j + 1 < len(field_mat[0]) and str(field_mat[i][j])[0] == str(field_mat[i][j + 1])[0] and (i, j + 1) in waves_all:
                        cell_to_tube.append((i, j + 1))

                    if j - 1 > -1 and str(field_mat[i][j])[0] == str(field_mat[i][j - 1])[0] and (i, j - 1) in waves_all:  # если на том же этаже и есть в волнах, то считаем что с этой клетки можно забрать
                        cell_to_tube.append((i, j - 1))

                    # ---------------picking up from ramps-----------------#
                    if j - 1 > -1 and str(field_mat[i][j - 1]) == "33" and (i, j - 1) in waves_all: #все равно на россию переписывать...(
                        cell_to_tube.append((i, j - 1))

                    if j + 1 < len(field_mat[0]) and str(field_mat[i][j + 1]) == "32" and (i, j + 1) in waves_all:
                        cell_to_tube.append((i, j + 1))



                elif list(str(field_mat[i][j]))[-1] == "0":
                    print("found")

                    if i - 1 > -1 and str(field_mat[i][j])[0] == str(field_mat[i - 1][j])[0] and (
                    i - 1, j) in waves_all:
                        cell_to_tube.append((i - 1, j))

                    if i + 1 < len(field_mat) and str(field_mat[i][j])[0] == str(field_mat[i + 1][j])[0] and (
                    i + 1, j) in waves_all:
                        cell_to_tube.append((i + 1, j))

                    # ---------------picking up from ramps-----------------#
                    if i + 1 < len(field_mat) and str(field_mat[i + 1][j]) == "30" and (i + 1, j) in waves_all:
                        cell_to_tube.append((i + 1, j))

                    if i - 1 > -1 and str(field_mat[i - 1][j]) == "31" and (i - 1, j) in waves_all:
                        cell_to_tube.append((i - 1, j))

            if cell_to_tube:
                cells_to_tubes_dict[(i, j)].append(cell_to_tube)
                cell_to_tube = []
    # print_colored(waves_all,"blue")
    return cells_to_tubes_dict, tubes

def find_points_to_unload(field_mat):

    # --------------tubes unload up points finding------------------#

    unload_cells_dict = {}
    unload_cords = []
    unload_cells = []

    for z in range(len(field_mat)):
        for ov in range(len(field_mat[0])):  # клетки из которых можно разгрузить трубы
            if str(field_mat[z][ov])[0] == "6":  # если нашли точку разгрузки

                unload_cords.append((z, ov))
                unload_cells_dict[unload_cords[-1]] = []

                if str(field_mat[z][ov])[-1] == "0" or str(field_mat[z][ov])[
                    -1] == "1":  # если направление места разгрузки - 0 или 1

                    if z + 1 < len(field_mat) and str(
                            field_mat[z + 1][ov]) == "70":  # разгружать можно только с первого этажа
                        unload_cells_dict[unload_cords[-1]].append((z + 1, ov))
                        unload_cells.append((z + 1, ov))

                    if z - 1 > -1 and str(field_mat[z - 1][ov]) == "70":
                        unload_cells_dict[unload_cords[-1]].append((z - 1, ov))
                        unload_cells.append((z - 1, ov))

                if str(field_mat[z][ov])[-1] == "2" or str(field_mat[z][ov])[-1] == "3":

                    if ov + 1 < len(field_mat[0]) and field_mat[z][ov + 1] == 70:
                        unload_cells_dict[unload_cords[-1]].append((z, ov + 1))
                        unload_cells.append((z, ov + 1))

                    if ov - 1 > -1 and field_mat[z][ov - 1] == 70:
                        unload_cells_dict[unload_cords[-1]].append((z, ov - 1))
                        unload_cells.append((z, ov - 1))

    if unload_cords:
        return unload_cords, unload_cells

    if not unload_cords:


        print("Cant build path, no unload points!1!")
        print_colored("\n\n         FAILED", "red")
        return None

def final_roadmap(obj,field_mat,ramp_checkment = False,skip_all_cv = False):
    global smth_for_ramps
    smth_for_ramps = not ramp_checkment


    print_colored("          Let the procedure begin...","magenta")
    real_all_paths_no_joke = {} #all possible tubes picking ways, storing like [path lenght] = [ways of path list]
    way_lenghts = [] #war to store all ways lenght (keys to real_all_paths_no_joke)
    waves_all = [] #all waves to prevent adding unreachable cells to cells_to_tubes_dict


    my_pos = robot_pos_finder(field_mat) #возвращает позицию и заменяет робота на элемент первого этажа

    #-------------------waves building--------------------#

    dictionary = neighbour_ini(field_mat)
    p1_tmp = copy.deepcopy(my_pos) #variable for my pos storing (can be replaced with way[0][-1] but i don't care
    waves = wave_ini(my_pos,dictionary) #creating waves

    # print_colored(field_mat,"red")

    for k in waves:  # создание списка всех точек всех волн, что бы избежать повторения
        for q in k:
            waves_all.append(q)


    cells_to_tubes_dict, tubes = pick_up_points_find(field_mat,waves_all)#возвращает трубы и точки с которых можно забрать

    unload_cords, unload_cells = find_points_to_unload(field_mat) #cords - cords of tube holders, cells - cells to unload from

    for i in range(len(tubes)): #Проверка того, что в каждую трубу можно доехать, иначе маршрут нельзя построить
        if not cells_to_tubes_dict[tubes[i]]:
            wave_frame_displaying(tubes[i],0,0,obj,1,(0,0,255),"ERR",(6,0.8))
            print("Cant create path! Unreachable tube found:", tubes[i])
            print_colored("\n\n\n\n         FAILED", "red")
            return None


    tubes = all_permutations(tubes) #все варианты сбора труб
    tubes = tuples_to_lists(tubes) #all_permutations возвращает картежи, а не списки, что несомненно грустно

    cells_to_tubes_dict[unload_cords[0]] = [unload_cells] #добавление поинтов разгрузки труб


    for m in range(len(tubes)): #добавляем точку выгрузки к каждому маршруту
        tubes[m].append(unload_cords[0])


    for i in range(len(tubes)): #для всех вариантов сбора

        path_to_all = []
        way_lenght = 0
        p1_tmp = deepcopy(my_pos)

        for j in range(len(tubes[i])): #для всех труб в вариантах сбора

            ways_to_tube_dict = {}
            ways_to_tube = []


            for q in range(len(cells_to_tubes_dict[tubes[i][j]][0])): #для всех клеток с которых можно забрать конкретную трубу

                #16.11.24 в 20:25 я пофиксил тупейший баг, но об этом никто не узнает

                # print("pstart", p1_tmp)
                waves = wave_ini(p1_tmp,dictionary) #строим волну со старта
                if skip_all_cv:
                    wave_visual(waves,obj)

                way = wave_back_way(waves,p1_tmp,cells_to_tubes_dict[(tubes[i][j])][0][q],dictionary,0,obj,field_mat) #маршрут к одной из клеток из которой можно забрать трубу

                if way: #если путь есть, то записываем его в словарь с путями
                    progress_bar(round(( (1/len(tubes))*i + ((1/len(tubes))/len(tubes[i])*(j+1) ) )*100)) #nvm
                    #print(round(( (1/len(tubes))*(i+1) + ((1/len(tubes))/len(tubes[i])*j ) )*100))
                    ways_to_tube_dict[way[1]] = way[0] #way[0] - way cords list, way[1] - way lenght with ramps
                    ways_to_tube.append(way[1])
                else:
                    pass
                    # print("Failed while creating one of final ways. \n Seems like field was scanned incorrectly", "\n p1:", p1_tmp, "p2:", cells_to_tubes_dict[(tubes[i][j])][0][q])

            if not ways_to_tube: #если к одной из труб совсем никак нельзя проехать
                print("One of tubes is completely unreachable!")
                print(ways_to_tube_dict)
                wave_frame_displaying(tubes[i][j], 0, 0, obj, 1, (0, 0, 255), "ERR", (6, 0.8))
                print_colored("\n\n         FAILED", "red")
                return None

            # print(ways_to_tube_dict)
            path_to_all.append(ways_to_tube_dict[min(ways_to_tube)]) #список путей для одного из возможных маршрутов

            way_lenght += min(ways_to_tube)
            p1_tmp = ways_to_tube_dict[min(ways_to_tube)][-1]
        real_all_paths_no_joke[way_lenght] = path_to_all #как только закончился цикл - записываем получившийся маршрут
        way_lenghts.append(way_lenght) #и его длину (я не умею работать с ключами словаря(()

        # print(real_all_paths_no_joke[min(way_lenghts)])

        if skip_all_cv:
            ini(obj,field_mat)
        waves = wave_ini(p1_tmp, dictionary)

        if skip_all_cv:
            wave_visual(waves, obj)

        if skip_all_cv:
            for help_me in range(len(real_all_paths_no_joke[min(way_lenghts)])): #рисуем один из возможных маршрутов
                way_visualisation(obj, path_to_all[help_me], 0, 0, get_colors(help_me + 1))
                cv2.imshow("map", cv2.resize(obj, (600, 600)))
                cv2.waitKey(1)
            #time.sleep(0.1)

    if skip_all_cv:
        #как только все маршруты построены
        ini(obj,field_mat)
        waves = wave_ini(p1_tmp, dictionary)
        wave_visual(waves, obj)

        for g in range(len(real_all_paths_no_joke[min(way_lenghts)])):

            way_visualisation(obj, real_all_paths_no_joke[min(way_lenghts)][g], 0, 0, get_colors(g), 10, g, field_mat)
            wave_frame_displaying(real_all_paths_no_joke[min(way_lenghts)][g][-1], 0, 0, obj, 0, 1,g + 1)  # рисуем номер в клетке с которой забираем трубу
            cv2.imshow("map", cv2.resize(obj, (600, 600)))
            cv2.waitKey(0)

        for g in range(len(real_all_paths_no_joke[min(way_lenghts)])):
            if len(real_all_paths_no_joke[min(way_lenghts)][g]) > 1:
                way_visualisation(obj, real_all_paths_no_joke[min(way_lenghts)][g], 0, 1, get_colors(g),10,g,field_mat)
            wave_frame_displaying(real_all_paths_no_joke[min(way_lenghts)][g][-1],0,0,obj,0,1,g+1) #рисуем номер в клетке с которой забираем трубу
            cv2.imshow("map", cv2.resize(obj, (600, 600)))
            cv2.waitKey(1)
            time.sleep(0.2)

        way_lenghts = remove_duplicates(way_lenghts) #для красивого вывода

        print_colored("\n\n\npossible paths lenghts:" + "  " + str([i for i in way_lenghts]), "blue")
        print_colored("our choice:" + "  " + str(min(way_lenghts)), "blue")


        print_colored("\n\n\n\n\n\n\n\n      WAY DONE", "green")

    # print(real_all_paths_no_joke[min(way_lenghts)])
    return real_all_paths_no_joke[min(way_lenghts)]

def progress_bar(value):
  clear()
  if 0 <= value <= 100:


    bar_length = 20
    filled_length = int(bar_length * value / 100)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    print(f"Progress: [{bar}] {value:.0f}%")
  else:
    pass

def get_relative_direction(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    # Проверка на соседние клетки
    if abs(x1 - x2) + abs(y1 - y2) != 1:
        return None

    if x1 == x2:  # Изменение по оси Y (горизонтальное)
        return "R" if y2 > y1 else "L"
    else:  # Изменение по оси X (вертикальное)
        return "D" if x2 > x1 else "U"

def way_to_commands(path,field_mat):
    used_tubes = []
    rob_dir = "U"
    res = []
    field_mat = np.array(field_mat)
    # print(field_mat)

    waves_all = []
    waves = wave_ini(path[0][0], neighbour_ini(field_mat))
    for i in waves:
        waves_all+=i

    tubes_cords = pick_up_points_find(field_mat, waves_all)[0]
    tubes_cords = list(tubes_cords.keys())


    for i in range(len(path)):
        if i == len(path)-1: to_tube = 0
        else: to_tube = 1
        if len(path[i]) > 1:
            s_way = way_to_commands_single(path[i], field_mat, rob_dir, to_tube)

            res += s_way[0]
            rob_dir = s_way[1]

        if i != len(path) - 1:

            for j in tubes_cords:
                if math.dist(j, path[i][-1]) <= 1 and j not in used_tubes:
                    cell_with_tube = j
                    used_tubes.append(j)
                    break

            rel_pos = get_relative_direction(path[i][-1],cell_with_tube)
            move_to_pick = get_rotation_direction(rob_dir,rel_pos)

            if move_to_pick != "skip":
                res.append(move_to_pick)
            res.append("G0")

            rob_dir = rel_pos

    print(res)
    return res, rob_dir

def create_path(mat,enable_visual = 0):
    unload_dict = {"r":["P1","R1","X1","L1","P1","R1","X1","L1","P1"],"l":["P1","L1","X1","R1","P1","L1","X1","R1","P1"], "c":["L1","X1","R1","P1","R1","X1","L1","P1","R1","X1","L1","P1"]}
    mat_to_change = replace_ints_in_matrix(mat)
    start_time = time.time()

    obj = cv2.imread("white_picture.jpg")  # картинка для фона
    smth_for_ramps = True  # анти рекурсия при рамп чекменте


    full_way = final_roadmap(obj, mat_to_change,False, enable_visual)
    print(full_way)
    # cv2.waitKey(0)
    commands = way_to_commands(full_way,mat_to_change)
    type_u = detect_unload_type(full_way[-1][-1],mat_to_change, 2, commands[1])
    print(type_u)
    if type_u[1] != "skip":
        commands[0].append(str(type_u[1]))

    if enable_visual:
        cv2.imshow("map", cv2.resize(obj, (600, 600)))

    # ---------------------trash---------------------#
    end_time = time.time()
    execution_time = end_time - start_time
    print_colored(f"\nTaken time to find path\n    {execution_time:.6f} sec", "cyan")
    cv2.waitKey(1)

    return commands[0] + unload_dict[type_u[0]]

def ini_for_nerds(mat):
    obj = cv2.imread("white_picture.jpg")  # картинка для фона
    ini(obj, mat)
    cv2.imshow("map", cv2.resize(obj, (600, 600)))
    cv2.waitKey(0)

def tg_ini(mat):
    obj = cv2.imread("white_picture.jpg")  # картинка для фона
    if mat:
        for i in range(len(mat)):  # перебираем каждый элемент матрицы и выводим его
            for j in range(len(mat[i])):
                show_smth(mat[i][j], (i, j), obj)
    else:
        print("Field mat can't be non type object! \n   Programmer u are dummy ass")
    return obj

def split_string_into_pairs(input_string):
  """
  Splits a string into a list of two-character substrings.

  Args:
    input_string: The string to split.

  Returns:
    A list of two-character substrings, or an empty list if the input
    string is empty or has an odd number of characters.
  """
  if not input_string:
    return []

  pattern = r"[a-zA-Z0-9]{2}"  # Matches two alphanumeric characters

  matches = re.findall(pattern, input_string)

  return matches

def get_rotation_direction(current_direction, target_direction):

    directions = ["U", "R", "D", "L"]
    current_direction = current_direction.upper() # normalize the input
    target_direction = target_direction.upper()  # normalize the input

    if current_direction not in directions or target_direction not in directions:
        print_colored(current_direction, "blue")
        print_colored(target_direction, "blue")
        return None  # Invalid direction input



    current_index = directions.index(current_direction)
    target_index = directions.index(target_direction)

    # Calculate the difference in indices
    diff = (target_index - current_index) % 4  # Use modulo to handle wrap-around

    if diff == 0:
        return "skip"
    elif diff == 1:
        return "R1"  # Rotate right
    elif diff == 2:
        return "R2"  # Rotate back 180 degrees
    elif diff == 3:
        return "L1"  # Rotate left
    else:
        # print("fail")
        return None  # Should not happen, but handle it anyway

def detect_unload_type(pos, mat, debugging=1, dir_list=None):
    if debugging:
        print(pos)

    robot_dir = dir_list
    dir = ""
    tube_dir = ""

    # Check for tube in each direction and determine approach direction
    # Down check
    if pos[0] != len(mat)-1 and mat[pos[0] + 1][pos[1]] // 10 == 6:
        if debugging:
            print("down")
        tube_dir = "D"

        # Check right side (relative to tube)
        if pos[1] != len(mat[0])-1 and mat[pos[0] + 1][pos[1] + 1] // 10 != 6:
            dir = "r"
        # Check left side (relative to tube)
        elif pos[1] != 0 and mat[pos[0] + 1][pos[1] - 1] // 10 != 6:
            dir = "l"
        else:
            dir = "c"

    # Right check
    elif pos[1] != len(mat[0])-1 and mat[pos[0]][pos[1] + 1] // 10 == 6:
        if debugging:
            print("right")
        tube_dir = "R"

        # Check down side (relative to tube)
        if pos[0] != len(mat)-1 and mat[pos[0] + 1][pos[1] + 1] // 10 != 6:
            dir = "l"
        # Check up side (relative to tube)
        elif pos[0] != 0 and mat[pos[0] - 1][pos[1] + 1] // 10 != 6:
            dir = "r"
        else:
            dir = "c"

    # Up check
    elif pos[0] != 0 and mat[pos[0] - 1][pos[1]] // 10 == 6:
        if debugging:
            print("up")
        tube_dir = "U"

        # Check left side (relative to tube)
        if pos[1] != 0 and mat[pos[0] + 1][pos[1] + 1] // 10 != 6:
            dir = "l"
        # Check right side (relative to tube)
        elif pos[1] != len(mat[0])-1 and mat[pos[0] + 1][pos[1] - 1] // 10 != 6:
            dir = "r"
        else:
            dir = "c"

    # Left check
    elif pos[1] != 0 and mat[pos[0]][pos[1] - 1] // 10 == 6:
        if debugging:
            print("left")
        tube_dir = "L"

        # Check up side (relative to tube)
        if pos[0] != 0 and mat[pos[0] - 1][pos[1] - 1] // 10 != 6:
            dir = "l"
        # Check down side (relative to tube)
        elif pos[0] != len(mat)-1 and mat[pos[0] + 1][pos[1] - 1] // 10 != 6:
            dir = "r"
        else:
            dir = "c"

    if debugging:
        print(f"Direction: {dir}, Tube direction: {tube_dir}")
    return dir, get_rotation_direction(robot_dir, tube_dir)

def way_to_commands_single(path,mat,my_dir, to_tube = 0):
    mat  = np.array(mat)
    res = []
    floor = 1 if mat[path[0]] == 70 else 2

    for i in range(len(path)):

        # if i == len(path) - 2 and to_tube and len(path) > 2:
        #     tubes_codes = [1141,1140,7041,7040]
        #     # print(my_dir)
        #     my_y = path[-1][0]
        #     my_x = path[-1][1]
        #
        #
        #     if res[-1][-1] in ["L","R"]:
        #         slice = mat[my_y,my_x-1:my_x+2]
        #         if np.isin(slice,tubes_codes).any():
        #             res.append("Q0")
        #             # print("added pre_load!")
        #
        #     elif res[-1][-1] in ["U","D"]:
        #         slice = mat[my_y-1:my_y+2,my_x]
        #         if np.isin(slice,tubes_codes).any():
        #             res.append("Q0")
        #             # print("added pre_load!")

        res_prev = ""
        current_cell = mat[path[i]]
        if i+1 < len (path):
            next_cell=mat[path[i+1]]

            if current_cell == 70:
                if next_cell == 70:
                    res_prev+="X1"
                elif next_cell//10==3:
                    res_prev+="F1"
                    floor = 2

                else: print("ERROR", current_cell, next_cell)

            if current_cell == 10:
                if next_cell == current_cell:
                    res_prev+="X1"
                elif next_cell//10==3:
                    res_prev+="F0"
                    floor = 1
                else: print("ERROR", current_cell, next_cell)

            if current_cell//10 == 3:
                if next_cell//10 == 3:
                    res_prev +=f'F{2 - floor}'
                    floor = 3-floor
                else:
                    # pass
                    res_prev+="X1"


            if path[i][1] == path[i + 1][1] + 1:  # если некст клетка слева, то едем налево
                res_prev+="L"
            elif path[i][1] == path[i + 1][1] - 1:
                res_prev+="R"
            elif path[i][0] == path[i + 1][0] + 1:
                res_prev+="U"
            elif path[i][0] == path[i + 1][0] - 1:
                res_prev+="D"

        if res_prev != "" and res_prev != None:
            res.append(res_prev)

    # print("res:", res)
    seen = ""
    count = 1
    res_optimized = []
    for i in range(len(res)):
        if seen == "":
            seen = res[i]
        elif res[i] == seen:
            count += 1
        else:
            seen = seen.replace('1',str(count))
            res_optimized.append(seen)
            seen = res[i]
            count = 1
    seen = seen.replace('1', str(count))
    res_optimized.append(seen)

    print("opt:", res_optimized)
    # print("my_dir", my_dir)

    res_relative = []
    for i in res_optimized:
        if i[-1] != my_dir:
            # print("move_to_go", get_rotation_direction(my_dir, i[-1]), my_dir, i[-1])
            res_relative.append(get_rotation_direction(my_dir, i[-1]))
            my_dir = i[-1]

            i = i[0:2]
            res_relative.append(i)

        else:
            i = i[0:2]
            res_relative.append(i)

    print(res_relative)

    return res_relative, my_dir












# def way_to_commands_single(path,mat,my_dir):
#     # print("path:", path)
#     dir_list = []
#     mat = np.array(mat)
#     for i in range(len(path)-1):
#
#         if str(mat[path[i]])[0] == "3":
#             # print("ramping")
#             if len(dir_list) > 2 and (dir_list[-2])[0] != "3":
#                 dir_list.pop(-1)
#
#             if mat[path[i + 1]] == 70 or str(mat[path[i + 1]])[0] =="3": #если следующая клетка маршрута - первый этаж
#                 dir_list.append("sd")  # means ramp down
#             else:
#                 dir_list.append("su")  # means ramp up
#
#             if path[i][1] == path[i + 1][1] + 1:  # если некст клетка слева, то едем налево
#                 dir = "l"
#             elif path[i][1] == path[i + 1][1] - 1:
#                 dir = "r"
#             elif path[i][0] == path[i + 1][0] + 1:
#                 dir = "u"
#             elif path[i][0] == path[i + 1][0] - 1:
#                 dir = "d"
#             dir_list.append(dir)
#             continue
#
#         if path[i][1] == path[i + 1][1] + 1: # если некст клетка слева, то едем налево
#             dir = "L"
#         elif path[i][1] == path[i + 1][1] - 1:
#             dir = "R"
#         elif path[i][0] == path[i + 1][0] + 1:
#             dir = "U"
#         elif path[i][0] == path[i + 1][0] - 1:
#             dir = "D"
#         dir_list.append(dir)
#
#     print("abs:", dir_list)
#     res = []
#     u = 0
#     for i in dir_list:
#         #обработка рамп
#         if i in ["u", "d", "r", "l"]:
#             continue
#
#         if i == "su" or i == "sd": #проезд - рампа - проезд
#             r_dir = dir_list[u+1].upper()
#             dir_to_r = get_rotation_direction(my_dir, r_dir)
#
#             # print(r_dir, my_dir)
#             if dir_to_r != "skip":
#                 res.append(dir_to_r)
#
#             res.append("F1" if i == "su" else "F0")
#
#             if dir_list[u+1] != "su" and dir_list[u+1] != "sd":
#                 res.append("X1")
#
#             print("r_dir:", r_dir)
#             my_dir = r_dir
#
#             continue
#
#         if i == my_dir: #едем вперед если направление то же
#             res.append("X1")
#             continue
#
#         else:
#             # print(my_dir,i)
#             res.append(get_rotation_direction(my_dir,i)) #делаем поворот и едем вперед при смене направления
#             res.append("X1")
#             my_dir = i
#         u += 1
#     print("res:",res)
#     return res, my_dir







#bugs: 2 tubes with same pickup point (breaks everything)
#fix: check if next pickup point = previous => add empty point list => break current cycle => profit
#we need to create unload path thing. because our def returns only path to closest unload thing. So we still have some things to do

# print(get_rotation_direction("L","R"))

#24.02.25 1:45 everything almost done. All I have left is an unload type detection. But it is really easy. Transforming way to commands was harder than I expected tbh

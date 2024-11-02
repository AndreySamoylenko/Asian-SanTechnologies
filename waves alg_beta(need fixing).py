import time

matrix = [ [0,0,0,0],
           [0,0,0,0],
           [0,0,"un",0],
           [0,0,0,0],
           ]

def shortest_way(p1,p2,mat):
    waves = [[]]
    p1_real = (p1[1],p1[0])
    waves[0].append(p1_real)
    possible_cells = 1
    waves_num = 0
    while possible_cells != 0:
        waves.append([])

        for i in range(len(waves[-2])):
            waves_all = []


            for j in waves:
                for k in j:
                    waves_all.append(k)


            if mat[waves[-2][i][1]][waves[-2][i][0]] == 0:

                if waves[-2][i][0]+1 < len(mat) and mat[waves[-2][i][1]][waves[-2][i][0]+1] == 0 and (waves[-2][i][1],waves[-2][i][0]+1) not in waves_all :
                    waves[-1].append((waves[-2][i][1],waves[-2][i][0]+1))

                if mat[waves[-2][i][1]][waves[-2][i][0]-1] == 0 and (waves[-2][i][1],waves[-2][i][0]-1) not in waves_all and waves[-2][i][0]-1 > -1:
                    waves[-1].append((waves[-2][i][1],waves[-2][i][0]-1))

                if mat[waves[-2][i][1]-1][waves[-2][i][0]] == 0 and (waves[-2][i][1]-1,waves[-2][i][0]) not in waves_all and  waves[-2][i][1] - 1 > -1:
                    waves[-1].append((waves[-2][i][1]-1,waves[-2][i][0]))

                if waves[-2][i][1]+1 < len(mat) and mat[waves[-2][i][1]+1][waves[-2][i][0]] == 0 and (waves[-2][i][1]+1,waves[-2][i][0]) not in waves_all:
                    waves[-1].append((waves[-2][i][1]+1,waves[-2][i][0]))

        if len(waves[-1]) == 0:
            possible_cells = 0
            waves.pop(-1)
            print(waves)

            for l in range(len(waves)):
                for u in range(len(waves[l])):
                    mat[waves[l][u][1]][waves[l][u][0]] = l
                    print(str(waves[l][u][1])+"   "+str(waves[l][u][0]))
                    print(l)


            print_matrix(mat)
            return("done")

def print_matrix(matrix):
    column_widths = [0] * len(matrix[0])

    for row in matrix:
        for idx, element in enumerate(row):
            column_widths[idx] = max(column_widths[idx], len(str(element)))

    # Выводим матрицу с выравниванием
    for row in matrix:
        formatted_row = " ".join(f"{str(element):<{column_widths[idx]}}" for idx, element in enumerate(row))
        print(formatted_row)

shortest_way((0,0),(2,2),matrix)



import math

tubes_cords = [[(2,4),1],[(3,1),2],[(5,6),1]] #cords / floor
field_matrix = [
               [0,1,0,0,0,0,0,0], #possible values: 0 - empty
               [0,0,1,1,1,0,0,0],  #1 - second floor module, 2x - ramp, can be 23 24 25 26, last symbol means direction
               [0,0,1,1,1,0,0,0],  #3x up-down ramps, can be 37,38 - last symbols - also direction
               [0,0,0,0,0,1,1,1],
               [1,1,0,0,0,0,0,0],
               [0,0,0,0,1,0,34,1],
               [1,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,1]
                ]

def unreachable_sec_floor_segments_detection(mat):
    dead_cells = []
    cells_lifesavers = []
    for i in range(0,len(mat)):
        for j in range(0,len(mat[i])):
            if mat[j][i] == 1:
                if vector_to_nearest(1,(j,i),mat)[0] > 1 and vector_to_nearest(3,(j,i),mat)[0] > 1:
                    dead_cells.append((j,i))

                elif vector_to_nearest(3,(j,i),mat)[0] <= 1:
                    cells_lifesavers.append((j,i))

                elif vector_to_nearest(1,(j,i),mat)[0] <= 1:
                    pass #по идее надо выявлять 2 этажи которые стоят около рамп и искать связь с такими секторами но мне лень

    return dead_cells
def vector_to_nearest(type,cords,mat):
    objects_list = find_coordinates(mat,type)
    min_dist = 50
    cords_of_nearest = []
    for i in objects_list:
        if math.dist(i,cords) < min_dist and math.dist(i,cords) != 0:
            min_dist = math.dist(i,cords)
            cords_of_nearest = [i]
    return [min_dist,cords_of_nearest]
def find_coordinates(mat, obj):
    coordinates = []
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if str(obj) in str(mat[i][j]):
                coordinates.append((i, j))
    return coordinates


print(unreachable_sec_floor_segments_detection(field_matrix))

#print(vector_to_nearest(3,(7,7),field_matrix))

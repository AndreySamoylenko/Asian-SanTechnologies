import math

tubes_cords = [[(2,4),1],[(3,1),2],[(5,6),1]] #cords / floor
field_matrix = [
               [0,1,0,0,0,0,0,0], #possible values: 0 - empty
               [0,0,1,1,1,0,0,0],  #1 - second floor module, 2x - ramp, can be 23 24 25 26, last symbol means direction
               [0,0,1,1,1,0,32,0],  #3x up-down ramps, can be 37,38 - last symbols - also direction
               [0,0,0,35,0,1,1,1],
               [1,1,0,0,0,0,0,0],
               [0,0,0,0,1,0,34,1],
               [1,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]
                ]

def unreachable_sec_floor_segments_detection(mat):
    dead_cells = []
    cells_lifesavers = []
    maybe_cells = []
    for i in range(0,len(mat)):
        for j in range(0,len(mat[i])):
            if mat[j][i] == 1:
                if vector_to_nearest(1,(j,i),mat)[0] > 1 and vector_to_nearest(3,(j,i),mat)[0] > 1:
                    dead_cells.append((j,i))

                elif vector_to_nearest(3,(j,i),mat)[0] <= 1:
                    cells_lifesavers.append((j,i))

                elif vector_to_nearest(1,(j,i),mat)[0] <= 1:
                    maybe_cells.append((j,i))

    for i in range(100):
        for i in cells_lifesavers:
            for j in maybe_cells:
                if math.dist(i,j) == 1 and math.dist(i,j) != 0:
                    cells_lifesavers.append(j)
                    maybe_cells.remove(j)

    for i in range(len(maybe_cells)):
        dead_cells.append(maybe_cells[i])

    return dead_cells,cells_lifesavers
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


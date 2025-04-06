import cv2
import copy
from Future_engeneers_path_creation_new import create_path, ini_for_nerds, replace_ints_in_matrix

mat = [[31, 10, 52, 20, 10, 10, 10, 10], [20, 10, 20, 20, 20, 34, 10, 41], [20, 10, 20, 20, 20, 34, 71, 31], [33, 34, 32, 10, 10, 10, 10, 20], [20, 20, 34, 10, 20, 10, 10, 20], [20, 10, 42, 10, 20, 10, 10, 20], [10, 10, 10, 10, 20, 20, 10, 33], [63, 63, 63, 10, 33, 10, 10, 10]][[31, 10, 52, 20, 10, 10, 10, 10], [20, 10, 20, 20, 20, 34, 10, 41], [20, 10, 20, 20, 20, 34, 71, 31], [33, 34, 32, 10, 10, 10, 10, 20], [20, 20, 34, 10, 20, 10, 10, 20], [20, 10, 42, 10, 20, 10, 10, 20], [10, 10, 10, 10, 20, 20, 10, 33], [63, 63, 63, 10, 33, 10, 10, 10]]
way = create_path(mat,1)
# print((0,0) == [0,0])
# print(replace_ints_in_matrix(mat))
ini_for_nerds(replace_ints_in_matrix(mat))
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
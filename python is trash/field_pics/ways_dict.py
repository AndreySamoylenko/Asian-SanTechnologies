import cv2

field_mat = [ [7041, 70, 70, 70, 70, 70, 70, 70],
	         [ 11, 30, 10, 10, 10, 32, 70 , 30],
	         [ 70, 31, 70, 70, 11, 70, 70, 11],
	         [ 11, 70, 70, 70, 70, 70, 11, 1140],
	         [7041, 70 ,11, 30, 70, 70, 11, 11],
	         [70, 70, 11, 31, 70, 70, 31, 31 ],
	         [70, 11, 11, 70, 70, 70, 70, 70],
	         [70 , 70,  70, 70 , 70 , 7060, 7060, 7060] ]
obj = cv2.imread("white_picture.jpg")

def ini(img,mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            show_smth(mat[i][j],(i,j),obj)
def show_smth(code,cords,object):
        pic = cv2.imread(f"field_pics/{code}.jpg")
        object[100 * cords[0]:100 * cords[0] + 100, 100 * cords[1]: 100 * cords[1] + 100] = pic






def print_matrix(matrix):
    if not matrix:
        print("programmer ur dummy")
        return

    max_width = max(len(f"{value}") for row in matrix for value in row)

    for row in matrix:
        formatted_row = " | ".join(f"{value:<{max_width}}" for value in row)
        print("| " + formatted_row + " |")
def neighbour_ini(mat):
    neighbour_dict = {}
    for i in range(len(mat)):
            for j in range(len(mat[i])):
                neighbour_dict[(i,j)] = []

                if len(mat[i][j]) == 2:
                    if mat[i][j][-1] == 0:
                        pass


ini(obj, field_mat)

cv2.imshow("map",cv2.resize(obj,(600,600)))
cv2.waitKey()




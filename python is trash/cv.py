import cv2
import numpy as np

field_mat = [
    [42, 10, 10, 10, 10, 10, 10, 10],
    [20, 33, 20, 20, 20, 34, 10, 33],
    [10, 31, 10, 10, 20, 10, 10, 20],
    [10, 10, 10, 10, 10, 10, 20, 51],
    [41, 10, 20, 20, 10, 10, 20, 20],
    [10, 10, 20, 20, 10, 10, 31, 31],
    [10, 20, 10, 31, 10, 10, 10, 10],
    [10, 10, 10, 10, 10, 63, 63, 63],
]

field_map_predv = [[0] * 15] * 15
field_map_predv[8][8] = 71
# print(field_map_predv)

downRed = np.array([0, 90, 0])
upRed = np.array([10, 255, 255])
downRed1 = np.array([170, 90, 0])
upRed1 = np.array([180, 255, 255])

downEdge = np.array([170, 80, 0])
upEdge = np.array([180, 255, 255])
downEdge1 = np.array([0, 80, 0])
upEdge1 = np.array([10, 255, 255])

downBlue = np.array([104, 44, 82])
upBlue = np.array([117, 255, 255])

downGreen = np.array([58, 114, 0])
upGreen = np.array([88, 255, 255])

downWhite = np.array([0, 0, 130])
upWhite = np.array([180, 70, 255])

corner_l = [[0, 120], [110, 210]]
corner_r = [[640, 120], [530, 210]]

edge_cords = {1: (((220, 105), (420, 135)), ((170, 215), (470, 245)), ((200, 440), (440, 480))),
              2: (((220, 105), (420, 135)), ((170, 215), (470, 245)), ((200, 440), (440, 480)))}

interest_zones = {"higher": [[[[0, 190], [160, 360]], [[180, 170], [460, 350]], [[480, 190], [640, 360]]],
                             [[[90, 95], [215, 150]], [[240, 100], [400, 180]], [[425, 95], [550, 150]]]],
                  "same": [[[[20, 230], [180, 420]], [[200, 240], [440, 450]], [[460, 230], [620, 420]]],
                           [[[100, 125], [230, 220]], [[230, 120], [410, 220]], [[410, 125], [540, 220]]]],
                  "lower": [[[[20, 250], [200, 450]], [[200, 250], [440, 480]], [[440, 250], [620, 450]]],
                            [[[100, 155], [230, 250]], [[230, 140], [410, 250]], [[410, 155], [540, 250]]]]}

cords_for_white = {1: [[[[20, 210], [200, 400]], [[200, 210], [440, 430]], [[440, 210], [620, 400]]],
                       [[[100, 115], [215, 160]], [[0, 0], [0, 0]], [[440, 115], [550, 160]]]],
                   2: [[[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]],
                       [[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]]]}

for i in range(len(cords_for_white[1])):
    for j in range(len(cords_for_white[1][i])):
        for k in range(len(cords_for_white[1][i][j])):
            for l in range(len(cords_for_white[1][i][j][k])):
                if cords_for_white[1][i][j][k][l] == 0:
                    cords_for_white[1][i][j][k][l] = int((interest_zones["higher"][i][j][k][l] + interest_zones["same"][i][j][k][l]) / 2)
                if cords_for_white[2][i][j][k][l] == 0:
                    cords_for_white[2][i][j][k][l] = int((interest_zones["lower"][i][j][k][l] + interest_zones["same"][i][j][k][l]) / 2)


def from_cords_to_slice(frame_, massive2x2):
    return frame_[massive2x2[0][1]:massive2x2[1][1], massive2x2[0][0]:massive2x2[1][0]]


def count_white(massive):
    summa = 0
    summb = 0
    for row in range(0, len(massive), 5):
        for pixel in range(0, len(massive[row]), 5):
            if massive[row][pixel] > 0:
                summa += 1
            else:
                summb += 1
    return summa, summb


def searchForColor(frame_, minhsv, maxhsv, min_area=50):
    if minhsv[0] == downRed[0]:
        mask1 = cv2.inRange(frame_, downRed, upRed)
        mask2 = cv2.inRange(frame_, downRed1, upRed1)
        mask = cv2.bitwise_or(mask1, mask2)
    elif minhsv[0] == downEdge[0]:
        mask1 = cv2.inRange(frame_, downEdge, upEdge)
        mask2 = cv2.inRange(frame_, downEdge1, upEdge1)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(frame_, minhsv, maxhsv)

    contours, k = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = 0, 0, 0, 0
    for cont in contours:
        area = cv2.contourArea(cont)
        if area > min_area:
            x1, y1, w1, h1 = cv2.boundingRect(cont)
            if w1 * h1 > w * h:
                x, y, w, h = x1, y1, w1, h1

    return x, y, w, h


def isTileWhite(tile):
    hsv = cv2.cvtColor(tile, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, downWhite, upWhite)
    white_dots, black_dots = count_white(mask)
    return white_dots > black_dots


def checkFloor(frame):
    local_frame = from_cords_to_slice(frame, [[200, 240], [440, 450]])
    res, _ = lookAtTile(local_frame, isTileWhite(local_frame))
    if res == 10 or res == 31:
        return 1
    elif res == 20 or res == 33:
        return 2


def from_cringe_to_normal(cringe_frame):
    frame_height, frame_width = cringe_frame.shape[:2]
    width, height = 100, 100
    pts1 = np.float32([[0, 0], [frame_width, 0], [frame_width, frame_height], [0, frame_height]])
    pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(cringe_frame, matrix, (width, height))


def edge_check(frame_):
    frame_height, frame_width = frame_.shape[:2]
    frame1 = cv2.blur(frame_, [6, 6])
    ImageHSV = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    xR, yR, wR, hR = searchForColor(ImageHSV, downEdge, upEdge, 20)
    if wR >= frame_width * 0.7:
        return 1
    return 0


def analyse_edges(frame_, floor):
    result = []
    for i in range(len(edge_cords[1])):
        result.append( edge_check(from_cords_to_slice(frame_, edge_cords[floor][i])))
    return result[::-1]


def rotate_matrix(mat_, turn_value):
    mat1 = mat_
    mat_res = []
    # print(mat_res.shape)
    for turn in range(turn_value):
        mat_res = np.array(mat_)
        for i in range(len(mat1)):
            for j in range(len(mat1[0])):
                direction = 0
                direction = mat1[j][i] % 10
                mat1[j][i] -= direction
                if direction:
                    if 5 >= mat1[j][i] // 10 >= 4:
                        direction = direction % 2 + 1
                    else:
                        direction = direction % 4 + 1

                mat_res[i, len(mat1[0]) - 1 - j] = mat1[j][i] + direction

        mat1 = mat_res
    return mat_res


def from_15x15_to_15x8(m15x15, position, orientation, distance_to_edge):
    m15x8 = np.array([[[0] * 15] * 8])
    tile_under_robot = int(m15x15[position[1]][position[0]])
    m15x15[position[1]][position[0]] = 70
    if orientation != 1:
        m15x15 = rotate_matrix(m15x15, 5 - orientation)
    new_pos = []
    for i in range(15):
        for j in range(15):
            if m15x15[i][j] == 70:
                new_pos = [i, j]
                break

    m15x8 = m15x15[new_pos[0] - distance_to_edge:(new_pos[0] - distance_to_edge) + 8, 0:15]
    orientation = 1
    m15x8[distance_to_edge][new_pos[1]] = tile_under_robot
    new_pos = [new_pos[1], distance_to_edge]
    return m15x8, new_pos, orientation


def from_15x8_to_8x8(m15x8, position, orientation, distance_to_edge):
    if orientation % 2 == 0:
        m8x8 = []
        if orientation == 2:
            m8x8 = m15x8[0:8, position[0] + distance_to_edge - 7:position[0] + distance_to_edge + 1]
            return m8x8
        elif orientation == 4:
            m8x8 = m15x8[0:8, position[0] - distance_to_edge:position[0] - distance_to_edge + 8]
            return m8x8
        else:
            print('oh no, wrong direction')
    else:
        print('opa, wrong direction')


def lookAtTile(frame_, white_flag):
    message = "none"
    frame_height, frame_width = frame_.shape[:2]
    min_area = frame_height * frame_width * 0.04
    frame_ = cv2.blur(frame_, [11, 11])

    ImageHSV = cv2.cvtColor(frame_, cv2.COLOR_BGR2HSV)

    if white_flag:  # если клетка белая
        xR, yR, wR, hR = searchForColor(ImageHSV, downRed, upRed, min_area)
        xG, yG, wG, hG = searchForColor(ImageHSV, downGreen, upGreen, min_area)

        if wG * hG > 0:
            # зеленая труба
            if wG > hG:
                if (yG + hG / 2) > frame_height / 2:
                    result = 61
                else:
                    result = 63  # это вроде невозможный вариант (мы не можем такое увидеть)
            else:
                if (xG + wG / 2) > frame_width / 2:
                    result = 62
                else:
                    result = 64
            message = "stand " + str(result - 60)
        elif wR * hR > 0:
            # трубы красные
            if wR < hR:  # vertical
                result = 42
            else:  # horizontal
                result = 41
            message = "tube " + str(result - 40)
        else:
            result = 10
            message = 'lower X'
    else:  # если клетка черная
        min_area = frame_height * frame_width * 0.02

        xB, yB, wB, hB = searchForColor(ImageHSV, downBlue, upBlue, min_area * 0.5)
        xR, yR, wR, hR = searchForColor(ImageHSV, downRed, upRed, min_area)

        if wB * hB > 0:
            # пандусы(рампы)
            deltx = xB - xR
            delty = yB - yR
            x, y, w, h = xB, yB, wB, hB

            if abs(deltx) < abs(delty):
                if delty < 0:
                    result = 34  # рампа направо (синий ближе к роботу)
                else:
                    result = 32  # рампа налево (красный ближе к роботу)
            else:
                if deltx < 0:
                    result = 33  # рампа назад (верх ближе к роботу)
                else:
                    result = 31  # рампа вперед (низ ближе к роботу)
            message = "ramp " + str(result - 30)
        elif wR * hR > 0:
            # трубы красные
            if wR < hR:  # vertical
                result = 52
            else:  # horizontal
                result = 51
            message = "tube " + str(result - 40)
        else:
            result = 20
            message = 'upper X'

    return result, message


keys_ = ['lower', 'same', 'higher']


def scanTheFrame(frame, elevation):
    results = [[0, 0, 0], [0, 0, 0]]
    messages = [['a', 'b', 'c'], ['d', 'e', 'f']]
    c_l, c_r = 0, 0
    elevation_differences = [[0, 0, 0], [0, 0, 0]]

    whites = [[0, 0, 0], [0, 0, 0]]
    edges = analyse_edges(frame, elevation)
    strokes_to_scan = 2 - edges[0]

    for i in range(strokes_to_scan):
        for j in range(len(elevation_differences[0])):
            # print(cords_for_white[elevation][i][j])
            local_frame = from_cords_to_slice(frame, cords_for_white[elevation][i][j])
            _, __, wb, hb = searchForColor(
                cv2.cvtColor(from_cords_to_slice(frame, interest_zones[keys_[2 - elevation]][i][j]), cv2.COLOR_BGR2HSV), downBlue, upBlue)
            whites[i][j] = isTileWhite(local_frame)
            if wb * hb > 0:
                elevation_differences[i][j] = 2 - elevation
                results[i][j], messages[i][j] = lookAtTile(
                    from_cords_to_slice(frame, interest_zones[keys_[elevation_differences[i][j]]][i][j]), 0)

            else:
                elevation_differences[i][j] = 3 - (elevation + whites[i][j])
                results[i][j], messages[i][j] = lookAtTile(
                    from_cords_to_slice(frame, interest_zones[keys_[elevation_differences[i][j]]][i][j]), whites[i][j])

    return results, messages, elevation_differences

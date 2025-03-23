import RPi.GPIO as GPIO
import serial

# Configure the serial port

ser = serial.Serial('/dev/ttyS0', 9600)
ser.flush()  # очищаем буфер
# print ("Serial port opened correctly")

# Choose the correct GPIO numbering scheme (BCM is recommended)
GPIO.setmode(GPIO.BCM)
# Define the GPIO pin you're using
GPIO_PIN = 23
GPIO.setup(GPIO_PIN, GPIO.IN)


def send(message):
    data_to_send = message + "\n"  # Data to send (must be bytes)
    ser.write(data_to_send.encode('utf-8'))
    # print(f"Sent: {data_to_send.strip()}") # вот тут надо будет использовать телеметрию


def digitalRead():
    return GPIO.input(GPIO_PIN)


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

field_map_predv = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

field_map_predv1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

field_map_predv2 = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

field_map_predv[8][8] = 71

current_position = [8, 8]
current_orientation = 1



def print_mat(mat):
    for i in mat:
        print(i)

def isTileValid(code, elevation):
    if elevation == 1:
        if code == 31 or code == 10:
            return True
    elif elevation == 2:
        if code == 20:
            return True
    else:
        return False


def findFirstNotNull(matrix):
    for i in range(0, 8):
        for j in range(0, 8):
            if matrix[i][j] != 0:
                return i, j
    return 8, 8


def countInMatrix(code, matrix):
    result = 0
    for i in matrix:
        for j in i:
            if j == code:
                result += 1
    return result


def updateMap(new_tiles, field_map_predv, cords, direction):
    cords_of_tiles_on_map = [0, 0]
    if direction == 1:
        cords_of_tiles_on_map = [cords[0] - 2, cords[1] - 1]
    elif direction == 2:
        cords_of_tiles_on_map = [cords[0] - 1, cords[1] + 1]
    elif direction == 3:
        cords_of_tiles_on_map = [cords[0] + 1, cords[1] - 1]
    elif direction == 4:
        cords_of_tiles_on_map = [cords[0] - 1, cords[1] - 2]

    height_of_new_tiles = 2
    width_of_new_tiles = 3
    if len(new_tiles) == 2 and len(new_tiles[0]) == 3:
        for i in range(height_of_new_tiles):
            for j in range(width_of_new_tiles):
                if 0 <= cords_of_tiles_on_map[0] + 2 < 15 and 0 <= cords_of_tiles_on_map[1] + 2 < 15:
                    # поворот клетки перед записью в матрицу
                    direction_of_map_object = new_tiles[i][j] % 10
                    if direction_of_map_object:
                        new_tiles[i][j] -= direction_of_map_object
                        if 40 <= new_tiles[i][j] < 53:
                            new_tiles[i][j] += direction_of_map_object % 2 + 1
                        else:
                            new_tiles[i][j] += (direction_of_map_object + direction - 1 - 1) % 4 + 1
                    # поворот зоны вставки
                    if direction == 1:
                        field_map_predv[cords_of_tiles_on_map[0] + i][cords_of_tiles_on_map[1] + j] = new_tiles[i][j]
                    elif direction == 2:
                        field_map_predv[cords_of_tiles_on_map[0] + j][cords_of_tiles_on_map[1] + (1 - i)] = new_tiles[i][j]
                    elif direction == 3:
                        field_map_predv[cords_of_tiles_on_map[0] + (1 - i)][cords_of_tiles_on_map[1] + (2 - j)] = new_tiles[i][j]
                    elif direction == 4:
                        field_map_predv[cords_of_tiles_on_map[0] + (2 - j)][cords_of_tiles_on_map[1] + i] = new_tiles[i][j]
                    else:
                        print("wrong direction")
    else:
        print("new_tiles wrong parameter")

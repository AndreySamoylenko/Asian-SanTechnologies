import time

import RPi.GPIO as GPIO
import cv2
import serial

import RobotAPI as rapi

# from cv import *


# создаём объект для работы с камерой робота
robot = rapi.RobotAPI()
robot.set_camera(100, 640, 480)

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


def objectRecognition(frame):
    pass


fps = 0
fps_count = 0
t = time.time()

list_of_motions = ["x3","l1","OO","F1","x1","l1","x1","F0","x1","l1"]
counter = -1

state = "button wait"
timer_actions = 0
while 1:
    frame = robot.get_frame(wait_new_frame=1)

    if state == "button wait":
        send("99")
        if digitalRead():
            send("B0")
            state = "string reading"
            timer_actions = time.time()

    if state == "string reading":
        if time.time() - timer_actions > 0.5:
            timer_actions = time.time()
            counter %= len(list_of_motions)
            send(list_of_motions[counter])

        if digitalRead():
            send("  ")
            state = "wait for action to end"

    if state == "wait for action to end":
        if not digitalRead():
            state = "string reading"
            counter += 1

    fps_count += 1
    if time.time() > t + 1:
        fps = fps_count
        fps_count = 0
        t = time.time()
    cv2.rectangle(frame, (0, 0), (430, 30), (0, 0, 0), -1)
    robot.text_to_frame(frame, str(state), 20, 20)
    robot.set_frame(frame, 40)

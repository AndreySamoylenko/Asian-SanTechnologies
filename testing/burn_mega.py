#!/usr/bin/env python3
import os
import subprocess
import glob
from pathlib import Path

# Конфигурация (Mega 2560)
ARDUINO_CLI = "/home/pi/bin/arduino-cli"  # или полный путь, например, "/home/pi/bin/arduino-cli"
ARDUINO_BOARD = "arduino:avr:mega"  # <-- Используем Mega 2560
SKETCH_DIR = "/home/pi/robot/arduino"  # Путь к папке с .ino-файлом


def find_ino_file(directory):
    """Находит .ino файл в указанной директории."""
    return "RRO_2025_DOWN.ino"


def detect_arduino_port():
    """Автоматически определяет порт Arduino."""
    # possible_ports = glob.glob("/dev/ttyACM*") + glob.glob("/dev/ttyUSB*")
    #
    # if not possible_ports:
    #     raise Exception("No Arduino port found! Check if Arduino is connected.")
    #
    # for port in possible_ports:
    #     try:
    #         cmd = [ARDUINO_CLI, "board", "list", "--format", "json"]
    #         result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    #
    #         if port in result.stdout:
    #             print(f"🔌 Found Arduino on port: {port}")
    #             return port
    #     except subprocess.TimeoutExpired:
    #         continue
    #
    # raise Exception(f"Arduino not detected on any port. Tried: {possible_ports}")
    return "ttyUSB0"


def upload_sketch(sketch_path, board, port):
    """Загружает скетч на Arduino."""
    cmd = [
        ARDUINO_CLI,
        "compile",
        "--fqbn", board,
        sketch_path,
        "--upload",
        "-p", port
    ]
    print(f"🚀 Uploading {sketch_path} to {board} on {port}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Upload failed!")
        print(result.stderr)
    else:
        print("✅ Upload successful!")
        print(result.stdout)


if __name__ == "__main__":
    try:
        sketch_dir = find_ino_file(SKETCH_DIR)
        arduino_port = detect_arduino_port()
        upload_sketch(sketch_dir, ARDUINO_BOARD, arduino_port)
    except Exception as e:
        print(f"❌ Error: {e}")
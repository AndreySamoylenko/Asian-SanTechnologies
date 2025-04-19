import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class DistortionCorrector:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Коррекция дисторсии")

        # Загрузка изображения
        self.original_image = cv2.imread(image_path)
        if self.original_image is None:
            raise ValueError("Не удалось загрузить изображение!")

        # Параметры камеры (примерные)
        self.height, self.width = self.original_image.shape[:2]
        self.camera_matrix = np.array([
            [1000, 0, self.width / 2],
            [0, 1000, self.height / 2],
            [0, 0, 1]
        ], dtype=np.float32)

        # Инициализация коэффициентов
        self.dist_coeffs = np.array([-0.1, 0.01, 0.001, 0.001, 0], dtype=np.float32)

        # Создание интерфейса
        self.create_widgets()
        self.update_image()

    def create_widgets(self):
        # Canvas для отображения изображения
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(side=tk.LEFT)

        # Фрейм для ползунков
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Создание ползунков для каждого коэффициента
        self.sliders = []
        params = [
            ("k1 (Радиальное)", -1.0, 1.0, self.dist_coeffs[0]),
            ("k2 (Радиальное)", -0.5, 0.5, self.dist_coeffs[1]),
            ("p1 (Тангенц.)", -0.01, 0.01, self.dist_coeffs[2]),
            ("p2 (Тангенц.)", -0.01, 0.01, self.dist_coeffs[3]),
            ("k3 (Радиальное)", -0.5, 0.5, self.dist_coeffs[4])
        ]

        for i, (text, min_val, max_val, init_val) in enumerate(params):
            label = tk.Label(control_frame, text=text)
            label.grid(row=i, column=0, sticky="w")

            slider = ttk.Scale(
                control_frame,
                from_=min_val,
                to=max_val,
                value=init_val,
                command=lambda val, idx=i: self.on_slider_change(val, idx),
                length=200
            )
            slider.grid(row=i, column=1)
            self.sliders.append(slider)

            # Отображение текущего значения
            value_label = tk.Label(control_frame, text=f"{init_val:.4f}")
            value_label.grid(row=i, column=2)
            self.sliders.append(value_label)  # Сохраняем ссылку на label

    def on_slider_change(self, val, idx):
        # Обновляем коэффициент
        self.dist_coeffs[idx] = float(val)

        # Обновляем отображение значения
        self.sliders[idx * 2 + 1].config(text=f"{float(val):.4f}")

        # Обновляем изображение
        self.update_image()

    def update_image(self):
        # Коррекция искажения
        undistorted = cv2.undistort(
            self.original_image,
            self.camera_matrix,
            self.dist_coeffs
        )

        # Конвертация для tkinter
        image_rgb = cv2.cvtColor(undistorted, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        tk_image = ImageTk.PhotoImage(pil_image)

        # Обновление изображения на canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.canvas.image = tk_image  # Сохраняем ссылку


# Запуск приложени
root = tk.Tk()
try:
    app = DistortionCorrector(root, "pole.jpg")
    root.mainloop()
except Exception as e:
    print(f"Ошибка: {e}")
    root.destroy()


def get_3x2_area_safe(matrix, center_x, center_y, direction):
    """
    Возвращает область 3x2 из матрицы, заменяя отсутствующие клетки на 0

    Параметры:
        matrix: входная матрица (2D список/массив)
        center_x, center_y: центральные координаты
        direction: направление (1 - вверх, 2 - вправо, 3 - вниз, 4 - влево)

    Возвращает:
        Список списков - область 3x2, где отсутствующие клетки заменены на 0
    """
    rows = len(matrix)
    if rows == 0:
        return [[0] * 3, [0] * 3] if direction in [1, 3] else [[0] * 2] * 3

    cols = len(matrix[0])
    result = []

    # Определяем смещения для разных направлений
    if direction == 1:  # Вверх
        offsets = [(-2, -1), (-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1)]
        row_len = 3
    elif direction == 2:  # Вправо
        offsets = [(-1, 1), (0, 1), (1, 1), (-1, 2), (0, 2), (1, 2)]
        row_len = 2
    elif direction == 3:  # Вниз
        offsets = [(1, -1), (1, 0), (1, 1), (2, -1), (2, 0), (2, 1)]
        row_len = 3
    elif direction == 4:  # Влево
        offsets = [(-1, -2), (0, -2), (1, -2), (-1, -1), (0, -1), (1, -1)]
        row_len = 2
    else:
        raise ValueError("Направление должно быть от 1 до 4")

    # Собираем данные с проверкой границ
    values = []
    for dy, dx in offsets:
        y = center_y + dy
        x = center_x + dx
        if 0 <= y < rows and 0 <= x < cols:
            values.append(matrix[y][x])
        else:
            values.append(0)

    # Формируем результат в виде строк
    if direction in [1, 3]:  # Для вверх/вниз - 2 строки по 3 элемента
        return [values[:3], values[3:]]
    else:  # Для вправо/влево - 3 строки по 2 элемента
        return [values[i:i + 2] for i in range(0, 6, 2)]

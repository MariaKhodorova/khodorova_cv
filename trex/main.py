import cv2 
from mss import mss
import numpy as np
import pyautogui
import time

bounding_box = {'top': 250, 'left': 100, 'width': 700, 'height': 200}
sct = mss()

dino_position = 100

# Функция для определения расстояния прыжка в зависимости от времени игры
def get_jump_distance(score):
    if score < 100:
        return 120
    elif score < 500:
        return 140
    else:
        return 160

# Функция для проверки наличия двойного препятствия
def is_double_obstacle(cnts, first_obstacle_x):
    for cnt in cnts:
        x, _, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        if w < 60 and h < 40 or aspect_ratio > 1.0:
            continue
        # Если следующее препятствие находится слишком близко к первому, считаем их двойным
        if x > first_obstacle_x and (x - first_obstacle_x) < 100:
            return True
    return False

pyautogui.press("space")  # Начинаем игру
score = 0
start_time = time.time()

while True:
    image = sct.grab(bounding_box)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    (thresh, image) = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    cnts, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])  # Сортируем контуры по их положению по оси X

    # Определяем положение ближайшего препятствия
    for i, cnt in enumerate(cnts):
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)

        if w < 60 and h < 40 or aspect_ratio > 1.0:
            continue
        obstacle_position = x
        # Обновляем счет в зависимости от времени игры
        current_time = time.time()
        score = int((current_time - start_time) * 10)

        jump_distance = get_jump_distance(score)
        if obstacle_position > dino_position and (obstacle_position - dino_position) < jump_distance:
            pyautogui.press("space")  # Прыгаем, если препятствие достаточно близко
            # Проверяем, есть ли следующее препятствие
            if is_double_obstacle(cnts[i+1:], x):
                time.sleep(0.1)  # Короткая пауза перед вторым прыжком
                pyautogui.press("space")
            time.sleep(0.3)  # Пауза, чтобы избежать множественных прыжков
            break

    cv2.imshow('Image', image)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

# max - 575
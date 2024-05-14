import cv2
from mss import mss
import numpy as np
import pyautogui

bounding_box = {'top': 250, 'left': 100, 'width': 700, 'height': 200}
sct = mss()

# Начальное положение динозавра (может потребоваться настройка)
dino_position = 100

pyautogui.press("space")  # Начинаем игру
       
while True:
    image = sct.grab(bounding_box)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    (thresh, image) = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    
    cnts, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
              
    # Определяем положение ближайшего препятствия
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 60 and h < 30:  # Игнорируем маленькие контуры, которые не являются препятствиями
            continue
        obstacle_position = x
        if obstacle_position > dino_position and (obstacle_position - dino_position) < 150:
            pyautogui.press("space")  # Прыгаем, если препятствие достаточно близко
            break  # Выходим из цикла, чтобы избежать множественных прыжков
    
    cv2.imshow('Image', image)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break 


    # max - 208
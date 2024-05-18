import cv2 
from mss import mss
import numpy as np
from time import sleep, time
import pyautogui 
from skimage.morphology import closing,disk
  
trex = cv2.imread("trex/trex.png")
trex = cv2.cvtColor(trex, cv2.COLOR_RGB2GRAY)
  
   
bbox = {'top': 250, 'left': 100, 'width': 700, 'height': 200}
    
frame_rate = 120
frame_duration = 1.0 / frame_rate
  
with mss() as sct:    
    pyautogui.press("space")
    sleep(2) 
  
    # Захват изображ ения
    img = np.array(sct.grab(bbox)) 
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  
    # Ищем динозаврика
    _, _, t_min_loc, t_max_loc = cv2.minMaxLoc(cv2.matchTemplate(img, trex, cv2.TM_SQDIFF_NORMED))
    bbox = { 
        "top": t_min_loc[1] - 96,
        "left": t_min_loc[0] - 4,
        "width": 300,
        "height": 150,
    }
  
    img = np.array(sct.grab(bbox))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    _, thrash, t_min_loc, t_max_loc = cv2.minMaxLoc(cv2.matchTemplate(img, trex, cv2.TM_SQDIFF_NORMED))

    start = time()
    timer = 0

    while True:
        frame_start_time = time()

        image = np.array(sct.grab(bbox))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        _, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

        enemy = image[:, int(image.shape[1] * 0.3) :]
        enemy = enemy[: int(enemy.shape[0] * 0.855), :]
        enemy = closing(enemy, disk(3))

        contours, _ = cv2.findContours(enemy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Получаем координаты ограничивающего прямоугольника для текущего контура
            x, y, w, h = cv2.boundingRect(contour)

            if time() - start < 45: agr = 30
            else: agr = 45
   
            timer = min(time() - start, 330)

            if x <= agr:
                if y + h - t_min_loc[1] - 20 > 0:
                    sleeper = (w) * 25 / (1000 + timer * 40)
 
                    if y - t_min_loc[1] >= -10:
                        sleeper += 0.1

                    pyautogui.press("up")
                    sleep(sleeper/4)
                    pyautogui.keyDown("down")
                    sleep(0.015)
                    pyautogui.keyUp("down")
                else:
                    pyautogui.keyDown("down")
                    sleep(abs(sleeper-0.03))
                    pyautogui.keyUp("down")
  
          
        frame_end_time = time()
        elapsed_time = frame_end_time - frame_start_time

        if elapsed_time < frame_duration:
            sleep(frame_duration - elapsed_time)  

        if cv2.waitKey(1) == ord("q"):
            break
       
        cv2.imshow('Image', enemy)
 
cv2.destroyAllWindows()

# max - 6728
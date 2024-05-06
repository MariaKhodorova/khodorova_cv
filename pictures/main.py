import cv2
import numpy as np
from skimage.measure import label, regionprops

#image = cv2.imread("pictures/Khodorova.png")
cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

video = cv2.VideoCapture("pictures/pictures.avi")
count = 0

while True:
    _, image = video.read()
    if  not _:
        break
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)


    cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = cv2.contourArea(cnts[0])

    if area > 121000 and area < 123000 :
        count += 1


    # cv2.putText(image, f"Number of my images = {count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (127, 255, 0))
    # cv2.putText(image, f"Area = {area}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (127, 255, 0))

    # cv2.imshow("Image", image)
    # cv2.imshow("Mask", thresh)
    
    # key = cv2.waitKey(1)
    # if key == ord('q'):
    #     break    

print(f"Final number of my images = {count}")
video.release()
cv2.destroyAllWindows()
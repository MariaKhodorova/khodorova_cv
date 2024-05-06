import cv2

video = cv2.VideoCapture('pictures/pictures.avi')

count = 0
while video.isOpened():
    _, image = video.read()
    if not _:
        break

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) != 1:
        continue
    if (cv2.arcLength(cnts[0], True) - cv2.arcLength(cnts[0], False) == 1):
        count += 1

    cv2.putText(image, f"Number of my images = {count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (127, 255, 0))

    cv2.imshow("Image", image)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break   
    

print(f"Final number of my images = {count}")
video.release()
cv2.destroyAllWindows()

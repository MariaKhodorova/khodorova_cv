import cv2
import numpy as np
import zmq

#method Canny

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_GUI_NORMAL)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5055
socket.connect(f"tcp://192.168.0.113:{port}")
n = 0

lower = 100
upper = 200

def lower_update(value):
    global lower
    lower = value

def upper_update(value):
    global upper
    upper = value

cv2.createTrackbar("Lower", "Mask", lower, 255, lower_update)
cv2.createTrackbar("Upper", "Mask", upper, 255, upper_update)


while True:
    image = cv2.imread("list/out.png")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    mask = cv2.Canny(gray, lower, upper)
    cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, cnts, -1, (255, 0, 0), 3)


    eps = 0.005 * cv2.arcLength(cnts[0], True)
    approx = cv2.approxPolyDP(cnts[0], eps, True)
    for p in approx:
        cv2.circle(image, tuple(*p), 6, (0, 255, 0), 4)
    #print(approx)


    pts = np.float32([[640, 0], [0, 0], [0, 640], [640, 877]])
    M = cv2.getPerspectiveTransform(approx[:, 0, :].astype("float32"), pts)
    agg = cv2.warpPerspective(image, M, (640, 480))

    cv2.putText(agg, "World", (130, 360), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    M = cv2.getPerspectiveTransform(pts, approx[:, 0, :].astype("float32"))
    list = cv2.warpPerspective(agg, M, (640, 480))
    list[np.all(list < 150, axis=2)] = image[np.all(list < 150, axis=2)]

    key = cv2.waitKey(10)
    if key == ord("q"):
        break

    cv2.imshow("Image", list)

cv2.destroyAllWindows()
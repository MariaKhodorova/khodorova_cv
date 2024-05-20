# ping  192.168.0.113
import cv2
import zmq
import numpy as np
from skimage.measure import regionprops


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
img = cv2.imread("count_objects/out.png")

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

port = 5055
ip = "192.168.0.113"

socket.connect(f"tcp://{ip}:{port}")

n = 0
while True:
    bts = socket.recv()
    n += 1
    arr = np.frombuffer(bts, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    _, binary = cv2.threshold(hsv[:,:,1], 55, 255, cv2.THRESH_BINARY)

    dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
    dist = cv2.normalize(dist, None, 0, 1, cv2.NORM_MINMAX)

    _, dist_tresh = cv2.threshold(dist, 0.45 * np.max(dist), 255, cv2.THRESH_BINARY)

    confuse = cv2.subtract(binary, dist_tresh.astype("uint8"))
    
    _, markers = cv2.connectedComponents(dist_tresh.astype("uint8"))
    markers += 1
    markers[confuse==255] = 0
    
    segments = cv2.watershed(image, markers)
    contours, hierrachy = cv2.findContours(segments, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        if hierrachy[0][i][3] == -1:
            cv2.drawContours(image, contours, i, (0, 255, 0), 2)

    features = []
    for i, region in enumerate(regionprops(segments)):
        features.append((region.eccentricity, (region.area/region.image.size)))


    objects = markers.max()-1
    balls, cubes = 0, 0
    for i in features:
        if i[0] < 0.43 and i[1] > 0.5:
            cubes += 1

    balls = objects - cubes

    key = cv2.waitKey(10)
    if key == ord("q"):
        break

    cv2.putText(image, f"Image: {n}", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
    cv2.putText(image, f"Cubes: {cubes}, Balls: {balls}", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
    cv2.putText(image, f"Objects: {objects}", (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (127, 0, 255))
    cv2.imshow("Image", image.astype("uint8"))
    cv2.imshow("Image1", segments.astype("uint8"))

cv2.destroyAllWindows()


# ping  192.168.0.113
import cv2
import zmq
import numpy as np
from skimage.measure import regionprops


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
img = cv2.imread("count_objects/out.png")


blured = cv2.GaussianBlur(img, (11, 11), 0)
hsv = cv2.cvtColor(blured, cv2.COLOR_BGR2HSV)
_, binary = cv2.threshold(hsv[:,:,1], 55, 255, cv2.THRESH_BINARY)

dist = cv2.distanceTransform(binary, cv2.DIST_L2, 5)
dist = cv2.normalize(dist, None, 0, 1, cv2.NORM_MINMAX)

_, dist_tresh = cv2.threshold(dist, 0.45 * np.max(dist), 255, cv2.THRESH_BINARY)

confuse = cv2.subtract(binary, dist_tresh.astype("uint8"))
    
_, markers = cv2.connectedComponents(dist_tresh.astype("uint8"))
markers += 1
markers[confuse==255] = 0
    
segments = cv2.watershed(img, markers)
contours, hierrachy = cv2.findContours(segments, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    if hierrachy[0][i][3] == -1:
        cv2.drawContours(img, contours, i, (0, 255, 0), 2)

features = []
for i, region in enumerate(regionprops(segments)):
    features.append((region.eccentricity, (region.area/region.image.size)))


num_objects = markers.max()-1
balls, cubes = 0, 0
for i in features:
    if i[0] < 0.43 and i[1] > 0.5:
        cubes += 1

balls = num_objects - cubes

cv2.putText(img, f"Cubes: {cubes}, Balls: {balls}", (10, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))
cv2.putText(img, f"Count of objects: {num_objects}", (10, 90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255))
cv2.imshow("Image", img)
cv2.imshow("Image1", segments.astype("uint8"))

key = cv2.waitKey(0)
cv2.destroyAllWindows()

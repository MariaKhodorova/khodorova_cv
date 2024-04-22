import cv2
import numpy as np
from skimage.measure import label, regionprops
from collections import defaultdict

def get_shapes(regions):
    shapes = defaultdict(lambda: 0)

    for index, region in enumerate(regions):
        key = ''
        eccent = region.eccentricity

        if eccent == 0:
            key = 'circle'
        else:
            key = 'rectangle'

        shapes[key] += 1

    return shapes

image = cv2.imread("figures_and_colors/balls_and_rects.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

labeled = label(gray)
print(f"Total figures: {labeled.max()}")

regions = regionprops(labeled)
shapes = get_shapes(regions)

for cur_key in shapes:
    print(f'{cur_key}s: {shapes[cur_key]}')


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Image", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()


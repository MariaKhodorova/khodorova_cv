import numpy as np
import matplotlib.pyplot as plt
from skimage import color, filters
from skimage.measure import label, regionprops

def hue2colors(img):
    c = np.unique(image[:, :, 0])
    colors = []
    e = np.diff(c).mean()
    prev_color = -1
    a = []

    for i in c:
        if prev_color == -1:
            a.append(i)
        elif np.abs(i - prev_color) >= e:
            mean = np.mean(a)
            if mean != 0.0:
                colors.append(mean)
            a = [i]
        else:
            a.append(i)
        prev_color = i

    colors.append(np.mean(a))
    return colors


def get_color(color: np.array, colors: np.array):
    max_abs = 1
    original_color = 0
    col = color[-1]
    for i in range(len(colors)):
        if abs(colors[i] - col) < max_abs:
            max_abs = abs(colors[i]-col)
            original_color = abs(colors[i])
    return original_color


rectangle_count, circle_count = 0, 0
figures_colors = {'rectangle': {}, 'circle': {}}

image = plt.imread("figures_and_colors/balls_and_rects.png")
image = color.rgb2hsv(image)
binary = np.mean(image, 2)
binary[binary < filters.threshold_otsu(binary)] = 0
binary[binary > 0] = 1

labeled = label(binary)
regions = regionprops(labeled)
colors = hue2colors(image)

for region in regions:
    (x, y, w, h) = region.bbox
    region_image = image[x:w, y:h]

    region_colors = np.unique(region_image[:, :, 0])
    color = str(get_color(region_colors, colors))

    if region.extent == 1:
        rectangle_count += 1

        if color in figures_colors['rectangle']:
            figures_colors['rectangle'][color] += 1
        else:
            figures_colors['rectangle'][color] = 1

    else:
        circle_count += 1

        if color in figures_colors['circle']:
            figures_colors['circle'][color] += 1
        else:
            figures_colors['circle'][color] = 1

print(f"Total figures: {rectangle_count + circle_count}")
print(f"Total rectangles: {rectangle_count}")
print(f"Total circles: {circle_count}")
print(f"Rectangles by colors: {figures_colors['rectangle']}")
print(f"Circles by colors: {figures_colors['circle']}")
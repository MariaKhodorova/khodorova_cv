import numpy as np
import matplotlib.pyplot as plt

def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1

size = 100
image = np.zeros((size, size, 3), dtype="uint8")
assert image.shape[0] == image.shape[1]

color1 = [255, 0, 127]
color2 = [255, 255, 51]

for y in range(image.shape[0]):
    for x in range(image.shape[1]):
        v = (x + y) / (size + size - 2)
        r = lerp(color2[0], color1[0], v)
        g = lerp(color2[1], color1[1], v) 
        b = lerp(color2[2], color1[2], v) 
        image[y, x] = [r, g, b]

plt.figure(1)
plt.imshow(image)
plt.show()
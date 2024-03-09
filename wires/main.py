from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np

image = np.load("wires/wires1.npy.txt")
r = label(image)

labels = np.unique(r)

for i in range(1, r.max() + 1):
    result = label(r == i)
    parts = binary_erosion(result)
    result1 = label(parts)
    #print(result1.max())
    count = result1.max()
    if  count == 1:
        print('провод не порван')
    elif count == 0:
        print('провод не существует')
    else:
        print(count)




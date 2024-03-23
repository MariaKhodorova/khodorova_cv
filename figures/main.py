from skimage.measure import label
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np

data = np.load("figures/ps.npy.txt")

labeled = label(data)

print(f'Общее количество фигур: {labeled.max()}')

struct_1 = np.array([[1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]])

struct_2 = np.array([[1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [0, 0, 1, 1, 0, 0],
                    [0, 0, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0]])

struct_3 = np.array([[1, 1, 0, 0, 1, 1],
                    [1, 1, 0, 0, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]])

struct_4 = np.array([[1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1],
                    [1, 1, 0, 0, 1, 1],
                    [1, 1, 0, 0, 1, 1],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]])

struct_5 = np.array([[1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [1, 1, 0, 0, 0, 0],
                    [1, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 0],
                    [1, 1, 1, 1, 0, 0]])

all_structures = [
    struct_1,
    struct_2,
    struct_3,
    struct_4,
    struct_5
]

for i, struct in enumerate(all_structures, 1):
    result = binary_dilation(binary_erosion(data, struct), struct)
    print(f'Фигура {i}: {label(result).max()}')
    data -= result

plt.imshow(data)
plt.show()
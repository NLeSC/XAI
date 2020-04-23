import numpy as np
from skimage.morphology import disk, diamond, square
import matplotlib.pyplot as plt

def my_square(radius, dtype):
    return square(radius*2+1, dtype)

SHAPES = [disk, diamond, my_square]

def generate_image(img_size, shapes, allow_occlusion=2):
    img = np.zeros((img_size, img_size), bool)
    i = 0
    while i < len(shapes):
        shape, radius = shapes[i]
        shape = SHAPES[shape]
        shape = shape(radius, bool)
        shape_area = np.sum(shape)
        x, y = np.random.randint(radius, img_size-radius, 2)
        xi, xf = x-radius, x+radius+1
        yi, yf = y-radius, y+radius+1

        ori = img[xi:xf, yi:yf]
        res = np.logical_or(ori, shape)
        if np.sum(res)-np.sum(ori) >= shape_area - allow_occlusion:
            img[xi:xf, yi:yf] = res
            i += 1
    return img

if __name__ == '__main__':
    NMIN, NMAX = 1, 10  # nbr of shapes
    RMIN, RMAX = 2, 12  # shape radius

    n = int(np.random.randint(NMIN, NMAX+1))
    shapes = [(np.random.randint(len(SHAPES)), np.random.randint(RMIN, RMAX))
              for i in range(n)]

    img = generate_image(126, shapes)
    plt.imshow(img)
    plt.title('n = %d' % n)
    plt.show()

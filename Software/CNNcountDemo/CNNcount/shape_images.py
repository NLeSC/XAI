import numpy as np
from skimage.morphology import disk, diamond, square
import matplotlib.pyplot as plt

# type of shapes (morphological SE from skimage)
def my_square(radius, dtype):
    return square(radius*2+1, dtype)

SHAPES = [disk, diamond, my_square]

# generating a single binary shape image
def generate_image(img_size, shapes, allow_occlusion=2):
    img = np.zeros((img_size, img_size), bool)
    i = 0
    while i < len(shapes):
        shape_type_ind, radius = shapes[i]
        shape_type = SHAPES[shape_type_ind]
        shape = shape_type(radius, bool)
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

# plot 12 random shape images
def plot_12images(images, labels):
    j=0
    nim = len(labels)
    for _ in range(12):
        ind=int(np.random.randint(1,nim))
        img=images[ind,:,:]
        img=np.reshape(img,(64,64))
        label=labels[ind]
        j = j+1
        plt.subplot(3, 4, j)
        plt.imshow(img,cmap='binary')
        plt.xticks([])
        plt.yticks([])
        plt.title('n=%d' %(label))
           
    plt.show()
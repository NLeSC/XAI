import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

TRAIN = 0.7
VALID = 0.2

# generating a single binary shape image
# def generate_image(img_size, shapes, allow_occlusion=2):
#     img = np.zeros((img_size, img_size), bool)
#     i = 0
#     while i < len(shapes):
#         shape_type_ind, radius = shapes[i]
#         shape_type = SHAPES[shape_type_ind]
#         shape = shape_type(radius, bool)
#         shape_area = np.sum(shape)
#         x, y = np.random.randint(radius, img_size-radius, 2)
#         xi, xf = x-radius, x+radius+1
#         yi, yf = y-radius, y+radius+1

#         ori = img[xi:xf, yi:yf]
#         res = np.logical_or(ori, shape)
#         if np.sum(res)-np.sum(ori) >= shape_area - allow_occlusion:
#             img[xi:xf, yi:yf] = res
#             i += 1
#     return img

# split to training, test and validaiton data
def split_data(images, labels):
    
    # split      
    nim = len(labels)
    ntr = int(TRAIN*nim)
    nval = int(VALID*nim)
   # ntst = nim - (ntr + nval)
   # print("#train, #validation and #test: ", ntr, nval, ntst)
    
    end_train_ind = ntr 
    #print("start train ind: beginning",",  end train ind: ", end_train_ind)
    images_train = images[:end_train_ind]
    labels_train = labels[:end_train_ind]
    
    start_val_ind = end_train_ind 
    end_val_ind = start_val_ind + nval
    #print("start valid ind: ", start_val_ind, ", end valid ind: ", end_val_ind)
    images_val = images[start_val_ind:end_val_ind]    
    labels_val = labels[start_val_ind:end_val_ind]
    
    start_test_ind = end_val_ind
    #print("start test ind:", start_test_ind, ", end test ind: end")
    images_test = images[start_test_ind:]
    labels_test = labels[start_test_ind:]
    
    return images_train, images_val, images_test, labels_train, labels_val, labels_test

# plot 12 random shape images
def plot_12images(images, labels, figsize=None):
    j=0
    nim = len(labels)
    if figsize is None:
        figsize = (8, 6)
    plt.figure(figsize=figsize)
    for _ in range(12):
        ind=int(np.random.randint(1,nim))
        img=images[ind,:]
        img=np.reshape(img,(64,64))
        label=labels[ind]
        j = j+1
        plt.subplot(3, 4, j)
        plt.imshow(img*255,cmap=cm.gray, vmin=0, vmax=255)
        plt.xticks([])
        plt.yticks([])
        plt.title('n=%d' %(label))
           
    plt.show()
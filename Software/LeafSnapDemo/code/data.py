import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

TRAIN = 0.7
VALID = 0.2


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
    
    return images_train, images_val, images_test, labels_train, labels_val, labels_test, end_train_ind, end_val_ind 

# plot 12 random leaf images
def plot_12images(images, labels=None, predictions = None, sources = None, figsize=None):
    j=0
    nim = np.shape(images)[0]
        
    if figsize is None:
        figsize = (8, 6)
    plt.figure(figsize=figsize)
    for _ in range(12):
        ind=int(np.random.randint(1,nim-12))
        img=images[ind,:]
        img=np.reshape(img,(64,64,3))
        if labels is not None:
            if isinstance(labels,(np.ndarray)):
                label=labels[ind]
            elif isinstance(labels, pd.core.series.Series):
                label = labels.iloc[ind]
        else:
            label = ''
        if predictions is not None:
            if isinstance(predictions,(np.ndarray)):
                prediction=predictions[ind]
                #print("predictions is an array!") 
            elif isinstance(predictions, pd.core.series.Series):
                #print("predictions is a series from a DataFrame!")   
                prediction = predictions.iloc[ind]
        else:
            prediction = ''  
        #print("prediction: ", prediction)    
        if sources is not None:
            if isinstance(sources, pd.core.series.Series):
                source = ', ' + sources.iloc[ind]            
        else:
            source = ''
        j = j+1
        plt.subplot(3, 4, j)
        plt.imshow(img) #,cmap=cm.gray, vmin=0, vmax=255)
        plt.xticks([])
        plt.yticks([])
        text = label + source
        plt.title('label: %s' %(text))
        if prediction:
            plt.xlabel('prediction: %s' %(prediction))
           
    plt.show()
    
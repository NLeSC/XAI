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
def plot_12images(images, labels=None, predictions = None, sources = None, unique_species_names = None, figsize=None):
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
                label_numeric = labels[ind]
                label = unique_species_names[label_numeric]
            elif isinstance(labels, pd.core.series.Series):
                label_numeric = labels.iloc[ind]
                label = unique_species_names.iloc[label_numeric]
            else:
                label = ''
        if predictions is not None:
            if isinstance(predictions,(np.ndarray)):
                prediction_numeric = predictions[ind]
                prediction=unique_species_names[prediction_numeric]
                
            elif isinstance(predictions, pd.core.series.Series): 
                prediction_numeric = predictions.iloc[ind]
                prediction = unique_species_names.iloc[prediction_numeric]
        else:
            prediction = ''     
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
        text = '%d, ' %(label_numeric) + label + source
        plt.title(text)
        if prediction:
            plt.xlabel('prediction: %d, %s' %(prediction_numeric, prediction))
           
    plt.show()
    
# plot 12 sequential leaf images
def plot_12seqimages(images, labels=None, predictions = None, sources = None, unique_species_names=None, start_ind = 0, figsize=None):
    j=0
        
    if figsize is None:
        figsize = (8, 6)
    plt.figure(figsize=figsize)
    for i in range(12):
        ind=start_ind + i
        img=images[ind,:]
        img=np.reshape(img,(64,64,3))
        if labels is not None:
            if isinstance(labels,(np.ndarray)):
                label_numeric = labels[ind]
                label = unique_species_names[label_numeric]
            elif isinstance(labels, pd.core.series.Series):
                label_numeric = labels.iloc[ind]
                label = unique_species_names.iloc[label_numeric]
        else:
            label = ''
        if predictions is not None:
            if isinstance(predictions,(np.ndarray)):
                prediction_numeric = predictions[ind]
                prediction=unique_species_names[prediction_numeric]
            elif isinstance(predictions, pd.core.series.Series):
                prediction_numeric = predictions.iloc[ind]
                prediction = unique_species_names.iloc[prediction_numeric]
        else:
            prediction = '' 
              
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
        text = '%d, ' %(label_numeric) + label + source
        plt.title(text)
        if prediction:
            plt.xlabel('prediction: %d, %s' %(prediction_numeric, prediction))
           
    plt.show()
        
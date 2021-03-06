# imports
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


# generate the model
def generate_model(input_shape, num_classes):
    # inninvestigate complains about defaut layer names, so give the layers explicit names
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(5, 5), 
                     strides=(1, 1), 
                     activation='relu',
                     input_shape=input_shape,
                     name='conv2d_layer1'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='maxpooling2d_layer1'))
    model.add(Conv2D(64, (5, 5), activation='relu', name='conv2d_layer2'))
    model.add(MaxPooling2D(pool_size=(2, 2), name='maxpooling2d_layer2'))
    model.add(Dropout(0.7, name='dropout_layer1'))
    model.add(Flatten(name='flatten_layer1'))
    model.add(Dense(1000, activation='relu', name='dense_layer1'))
    model.add(Dropout(0.7, name='dropout_layer2'))
    model.add(Dense(num_classes, activation='softmax', name='dense_layer2'))
    
    return model

# generate a very simple model
def generate_simpler_model(input_shape, num_classes):
    # inninvestigate complains about defaut layer names, so give the layers explicit names
    model = Sequential()
    model.add(Conv2D(12, kernel_size=(5, 5), 
                     strides=(1, 1), 
                     activation='relu',
                     input_shape=input_shape,
                     name='conv2d_layer1'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), name='maxpooling2d_layer1'))
    model.add(Conv2D(24, (5, 5), activation='relu', name='conv2d_layer2'))
    model.add(MaxPooling2D(pool_size=(2, 2), name='maxpooling2d_layer2'))
    model.add(Dropout(0.7, name='dropout_layer1'))
    model.add(Flatten(name='flatten_layer1'))
    model.add(Dense(200, activation='relu', name='dense_layer1'))
    model.add(Dropout(0.7, name='dropout_layer2'))
    model.add(Dense(num_classes, activation='softmax', name='dense_layer2'))
    

    return model

# train the model
def train_model(model, images_train, labels_train,images_val, labels_val, batch_size, epochs, best_model):

    model.compile(optimizer=keras.optimizers.Adam(lr=0.0003, 
                                                  beta_1=0.9, beta_2=0.999, 
                                                  epsilon=None, decay=1e-8, amsgrad=False),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    results = model.fit(images_train, labels_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(images_val, labels_val),
              callbacks=[best_model])

    return model, results
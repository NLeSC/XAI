# imports
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


# generate the model
def generate_cnncount_model(input_shape, num_classes):
    model = Sequential()
    # inninvestigate complains about defaut layer names, so give the layers explicit names
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape,
                     name='conv2d_layer1'))
    model.add(Conv2D(64, (3, 3), activation='relu', name='conv2d_layer2'))
    model.add(MaxPooling2D(pool_size=(2, 2), name='maxpooling2d_layer1'))
    model.add(Dropout(0.25, name='dropout_layer1'))
    model.add(Flatten(name='flatten_layer1'))
    model.add(Dense(128, activation='relu', name='dense_layer1'))
    model.add(Dropout(0.5, name='dropout_layer2'))
    model.add(Dense(num_classes, activation='softmax', name='dense_layer2'))
    
    return model

# train the model
def train_cnncount_model(model, images_train, labels_train,images_val, labels_val, batch_size, epochs):

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    
    model.fit(images_train, labels_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(images_val, labels_val))

    return model
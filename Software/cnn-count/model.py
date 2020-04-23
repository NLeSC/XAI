import numpy as np
from gen import generate_image
from keras.models import Sequential
from keras.optimizers import SGD
from keras.layers.core import Flatten, Dense
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
import matplotlib.pyplot as plt
#import sys

m = Sequential([
    Conv2D(32, 5, padding='same', activation='tanh', input_shape=(128, 128, 1)),
    MaxPooling2D(2),
    Conv2D(64, 5, padding='same', activation='tanh'),
    MaxPooling2D(2),
    Flatten(),
    Dense(1000, activation='tanh'),
    Dense(1)
])

print(m.summary())
m.compile(SGD(0.0001), 'MSE')

def generator():
    batch_size = 100
    while True:
        shape = [(0, 5)]
        y = np.random.randint(1, 10+1, batch_size)
        X = np.asarray([
            generate_image(128, shape*n)[:, :, np.newaxis].astype(np.float32)
            for n in y])
        yield X, y

m.fit_generator(generator(), 1, 1000)

for i in range(10):
    n = int(np.random.randint(1, 10+1))
    shapes = [(0, 5) for _ in range(n)]
    img = generate_image(128, shapes)
    
    X = img[np.newaxis, :, :, np.newaxis].astype(np.float32)
    plt.subplot(2, 5, i+1)
    plt.imshow(img)
    plt.title('y=%d ŷ=%.1f' % (n, m.predict(X)))

plt.show()

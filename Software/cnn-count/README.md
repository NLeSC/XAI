# CNN Count
Simple experiment training a CNN to count shapes in synthetic images.

This experiment uses Keras to train a convolutional neural network and scikit-image for the synthetic images.

Just run `model.py`. A feed-forward neural network is trained to count the number of shapes in a image. The current experiment treats the problem as a regression, and the synthethic images are 128x128 featuring from 1 up to 10 circles of the same size.

The code is easily configurable and other experiments can very easily be performed. (They are just very slow in my computer.)

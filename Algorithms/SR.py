import cv2
import numpy
from keras.models import Sequential
from keras.layers import Conv2D
from keras.optimizers import Adam
import cv2
import numpy as np

def model():
    SRCNN = Sequential()

    SRCNN.add(Conv2D(filters=128, kernel_size = (9, 9), kernel_initializer='glorot_uniform',
                     activation='relu', padding='valid', use_bias=True, input_shape=(None, None, 1)))
    SRCNN.add(Conv2D(filters=64, kernel_size = (3, 3), kernel_initializer='glorot_uniform',
                     activation='relu', padding='same', use_bias=True))
    SRCNN.add(Conv2D(filters=1, kernel_size = (5, 5), kernel_initializer='glorot_uniform',
                     activation='linear', padding='valid', use_bias=True))

    adam = Adam(lr=0.0003)

    SRCNN.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])

    return SRCNN

def shave(image, border):
    img = image[border: -border, border: -border]
    return img

def predict(image_path):
    srcnn = model()
    srcnn.load_weights('Algorithms/trained.h5')

    degraded = cv2.imread(image_path)

    h, w, _ = degraded.shape

    temp = cv2.cvtColor(degraded, cv2.COLOR_BGR2YCrCb)

    Y = numpy.zeros((1, temp.shape[0], temp.shape[1], 1), dtype=float)
    Y[0, :, :, 0] = temp[:, :, 0].astype(float) / 255

    pre = srcnn.predict(Y, batch_size=1)

    pre *= 255
    pre[pre[:] > 255] = 255
    pre[pre[:] < 0] = 0
    pre = pre.astype(np.uint8)

    temp = shave(temp, 6)
    temp[:, :, 0] = pre[0, :, :, 0]
    output = cv2.cvtColor(temp, cv2.COLOR_YCrCb2BGR)

    output = cv2.resize(output, (w, h), interpolation = cv2.INTER_LINEAR)

    return output

def SRCNN():
    output = predict('input.png')

    return cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
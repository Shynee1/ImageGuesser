import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from keras.layers import Dense,Flatten, Conv2D
from keras.layers import MaxPooling2D, Dropout
from keras.utils import np_utils
import tensorflow as tf
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint
import pickle
from keras.callbacks import TensorBoard

# Create convolutional neural network with Keras
def keras_model(image_x, image_y):
    num_of_classes = 15
    model = Sequential()
    model.add(Conv2D(32, (5, 5), input_shape=(image_x,image_y,1), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))
    model.add(Conv2D(64,(5, 5), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))

    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.6))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.6))
    model.add(Dense(num_of_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    filepath = "models/QuickDraw.h5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    callbacks_list = [checkpoint]

    return model, callbacks_list

# Loads data from pickle (python data format)
def loadFromPickle():
    with open("features", "rb") as f:
        features = np.array(pickle.load(f))
    with open("labels", "rb") as f:
        labels = np.array(pickle.load(f))

    return features, labels

# Converts labels to one-hot matrix
def prepress_labels(labels):
    labels = np_utils.to_categorical(labels)
    print(labels)
    return labels


def main():
    # Load pre-processed values from json
    features, labels = loadFromPickle()
    # Shuffle data
    features, labels = shuffle(features, labels)
    # Convert to one-hot matrix
    labels = prepress_labels(labels)

    # Split into test/train
    train_x, test_x, train_y, test_y = train_test_split(features, labels, random_state=0,test_size=0.3)

    # Reshape data to match model  
    train_x = train_x.reshape(train_x.shape[0], 28, 28, 1)
    test_x = test_x.reshape(test_x.shape[0], 28, 28, 1)

    model, callback_list = keras_model(28,28)
    model.summary()

    # train model
    model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=3   , batch_size=64,
              callbacks=[TensorBoard(log_dir="QuickDraw")])
    
    model.save('models/QuickDraw.h5')

main()
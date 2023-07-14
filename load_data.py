import numpy as np
import pickle
import os

def store_data(features, labels):
    with open("features", "wb") as f:
        pickle.dump(features, f, protocol=4)
    with open("labels", "wb") as f:
        pickle.dump(labels, f, protocol=4)

def list_data(filepath):
    files = os.listdir(filepath)
    count = 0
    x_load = []
    y_load = []

    for file in files:
        print(file)
        print(count)
        # Load dataset from .npy files
        x = np.load("dataset/" + file)
        # Fit values to 0-1
        x = x.astype('float32') / 255.
        # Limit elements to 50000
        x = x[0:50000, :]
        x_load.append(x)

        # Assign a label to each dataset (0-7)
        y = [count for _ in range(50000)]
        count += 1
        y = np.array(y).astype('float32')
        # Reshape to 1D array
        y = y.reshape(y.shape[0], 1)
        y_load.append(y)

    return x_load, y_load

features, labels = list_data("dataset")
features = np.array(features).astype('float32')
labels = np.array(labels).astype('float32')

# Combine smaller datasets into larger dataset
features = features.reshape(features.shape[0] * features.shape[1], features.shape[2])
labels = labels.reshape(labels.shape[0] * labels.shape[1], labels.shape[2])

store_data(features, labels)
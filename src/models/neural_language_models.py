"""
Functions for building and training a neuarl language model

The implementation was adapted from my homework 4 submission.
"""

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.optimizers import SGD
from keras.utils import to_categorical


def build_feedforward_model(output_dim, nodes_per_hidden_layer, lr):
    """Build a feedforward neural network

    Args:
        output_dim (int): Number of nodes in the output layer
        nodes_per_hidden_layer (list[int]): Each element in the list is the number of nodes in that hidden layer
        lr (float): Learning rate

    Returns:
        keras.Sequential: A Keras Sequential feedforward neural network
    """
    model = Sequential()
    for node_count in nodes_per_hidden_layer:
        model.add(Dense(node_count), activation="relu")
    model.add(Dense(output_dim, activation="softmax", name="output"))
    model.compile(loss="categorical_crossentropy", optimizer=SGD(learning_rate=lr))
    return model


def data_generator(X, y, batch_size, num_classes):
    """Build a data generator which produces inputs and labels

    Args:
        X (2d NumPy Array): A matrix of samples, where each row is an input
        y (1d NumPy Array): An array of labels which correspond to the samples in X
        batch_size (int): Number of samples to yield in one batch
        num_classes (int): The number of classes, because `y` is a categorical label

    Yields:
        tuple[2d NumPy Array, 1d NumPy Array]: A batch of inputs and labels
    """
    batch_index = 0
    max_batches = len(y) / batch_size
    while batch_index < max_batches:
        offset = batch_index * batch_size
        yield (X[offset:offset + batch_size],
               np.array(to_categorical(
                   y=y[offset:offset + batch_size],
                   num_classes=num_classes)))
        batch_index += 1

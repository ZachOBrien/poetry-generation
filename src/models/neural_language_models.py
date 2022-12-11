"""
Functions for building and training a neuarl language model

The implementation was adapted from my homework 4 submission.
"""

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam 


def build_character_lstm_model(vocab_size, hidden_layers, lr):
    """Build a character-based LSTM neural language model

    A character-based model predicts the next character in a sequence of characters.
    The model accepts batches of inputs of shape (batch_size, Any, vocab_size). `Any`
    here indicates that a single sequence can be arbitrary length. In the context
    of this project, that is important because poems are arbitrary in length.

    Args:
        vocab_size (PositiveInteger):
            The size of the vocabulary
        hidden_layers (list[PositiveInteger]):
            A list of hidden layers to add to the model
        lr (float): 
            Learning rate

    Returns:
        keras.Sequential: A Keras Sequential neural network which uses an LSTM layer.
    """
    model = Sequential()
    model.add(keras.Input(shape=(None, vocab_size)))  # `None` indicates the sequence is of arbitrary length
    for layer in hidden_layers:
        model.add(layer)
    model.add(Dense(vocab_size, activation="softmax"))
    model.compile(loss="categorical_crossentropy", optimizer=Adam(learning_rate=lr))
    model.build()
    return model


"""
Train an LSTM neural language model on character-tokenized poems

"""
import itertools
import pickle
import random
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress tensorflow debugging info

import pandas as pd
import numpy as np
from keras.utils import timeseries_dataset_from_array
from keras.layers import LSTM, Dropout

from dataprep.neural_lm_preprocessing import (
    Vectorizer,
    preprocess_for_neural_lm,
)
from models.neural_language_models import build_character_lstm_model


# Load the poems from disk
leaves_of_grass_df = pd.read_csv("../data/leaves_of_grass.csv")

# Pull only the poems out of the dataset
poems = list(leaves_of_grass_df["poem"])
poems = [preprocess_for_neural_lm(poem) for poem in poems]

# Fit a vectorizer to the vocabulary of characters
vectorizer = Vectorizer()
vectorizer.fit(itertools.chain(*poems))
# Vectorize all characters
vectorized_poems = [vectorizer.tokens_to_vectors(poem) for poem in poems]

# Randomly shuffle the poems before splitting into training and validation sets
random.shuffle(vectorized_poems)

# Use 70% of the data for training, and 15% for validation 
# during testing, and 15% for final model evaluation
train_set_size = int(0.8 * len(vectorized_poems))
validation_set_size = int(0.15 * len(vectorized_poems))
test_set_size = int(0.15 * len(vectorized_poems))

train_set = vectorized_poems[:train_set_size]
train_set = np.array(list(itertools.chain(*train_set)))

validation_set = vectorized_poems[train_set_size:(train_set_size + validation_set_size)]
validation_set = np.array(list(itertools.chain(*validation_set)))

# Each sample given to the model for training will be a sequence of 100 characters
SEQUENCE_LENGTH = 100
# I do not want to skip any samples, so sampling rate is 1
SAMPLING_RATE = 1
BATCH_SIZE = 4096


# Build timeseries datasets using Keras helpers
train_dataset = timeseries_dataset_from_array(
    data=train_set[:-SEQUENCE_LENGTH],
    targets=train_set[SEQUENCE_LENGTH:],
    sampling_rate=SAMPLING_RATE,
    sequence_length=SEQUENCE_LENGTH,
    batch_size=BATCH_SIZE)

validation_dataset = timeseries_dataset_from_array(
    data=validation_set[:-SEQUENCE_LENGTH],
    targets=validation_set[SEQUENCE_LENGTH:],
    sampling_rate=SAMPLING_RATE,
    sequence_length=SEQUENCE_LENGTH,
    batch_size=BATCH_SIZE)

# Build the model, with LSTM layers for handling the timeseries data
# and Dropout layers to help reduce overfitting
model = build_character_lstm_model(
    vocab_size=vectorizer.vocab_size(),
    hidden_layers=[LSTM(1, return_sequences=True),
                   Dropout(0.3),
                   LSTM(1),
                   Dropout(0.3)],
    lr=0.01)

# Train the model
history = model.fit(train_dataset, epochs=1)

# Save the model, the training metrics every epoch, and the vectorizer (necessary for inference)
model.save("character_based_lm")  # Save in TensorFlow's new SavedModel format
with open("history.pkl", "wb") as outfile:
    pickle.dump(history.history, outfile)
with open("vectorizer.pkl", "wb") as outfile:
    pickle.dump(vectorizer, outfile)

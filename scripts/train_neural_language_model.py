"""
Train an LSTM neural language model on character-tokenized poems

REQUIRES:
    - Training and validation datasets have already been derived.
      Run ./build_character_sequence_datasets.py to create them.
"""
import pickle
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress tensorflow debugging info

import tensorflow as tf
from keras.layers import LSTM, Dropout
from models.neural_language_models import build_character_lstm_model

VECTORIZER_PATH = "../data/vectorizer.pkl"
TRAIN_DATASET_PATH = "../data/training_dataset_tensorflow"
VALIDATION_DATASET_PATH = "../data/validation_dataset_tensorflow"

print("Loading vectorizer...")
with open(VECTORIZER_PATH, "rb") as infile:
    vectorizer = pickle.load(infile)

print("Loading training dataset...")
train_dataset = tf.data.Dataset.load(TRAIN_DATASET_PATH, compression="GZIP")

print("Loading validation dataset...")
validation_dataset = tf.data.Dataset.load(VALIDATION_DATASET_PATH, compression="GZIP")

# Build the model, with LSTM layers for handling the timeseries data
# and Dropout layers to help reduce overfitting
model = build_character_lstm_model(
    vocab_size=vectorizer.vocab_size(),
    hidden_layers=[LSTM(256, return_sequences=True),
                   Dropout(0.3),
                   LSTM(256),
                   Dropout(0.3)],
    lr=0.01)

print("Training model...")
# Train the model
history = model.fit(train_dataset, epochs=30, validation_data=validation_dataset)

# Save the model, the training metrics every epoch, and the vectorizer (necessary for inference)
model.save("character_based_lm")  # Save in TensorFlow's new SavedModel format
with open("history.pkl", "wb") as outfile:
    pickle.dump(history.history, outfile)
with open("vectorizer.pkl", "wb") as outfile:
    pickle.dump(vectorizer, outfile)

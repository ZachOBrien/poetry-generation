"""
Train an LSTM neural language model on character-tokenized poems

"""
import itertools

import pandas as pd
import numpy as np
import keras
from keras.utils import timeseries_dataset_from_array

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


vectorizer = Vectorizer()
vectorizer.fit(itertools.chain(*poems))

vectorized_poems = [vectorizer.tokens_to_vectors(poem) for poem in poems]

train_set_size = int(0.8 * len(poems))
validation_set_size = int(0.1 * len(poems))
test_set_size = int(0.1 * len(poems))


train_set = vectorized_poems[:train_set_size]
train_set = np.array(list(itertools.chain(*train_set)))

validation_set = vectorized_poems[train_set_size:(train_set_size + validation_set_size)]
validation_set = np.array(list(itertools.chain(*validation_set)))

SEQUENCE_LENGTH = 150
BATCH_SIZE = 8192

train_dataset = timeseries_dataset_from_array(
    data=train_set[:-SEQUENCE_LENGTH],
    targets=train_set[SEQUENCE_LENGTH:],
    sequence_length=SEQUENCE_LENGTH,
    batch_size=BATCH_SIZE)

validation_dataset = timeseries_dataset_from_array(
    data=validation_set[:-SEQUENCE_LENGTH],
    targets=validation_set[SEQUENCE_LENGTH:],
    sequence_length=SEQUENCE_LENGTH,
    batch_size=BATCH_SIZE)

#"""
model = build_character_lstm_model(vectorizer.vocab_size(), 32, 0.01)
model.fit(train_dataset, epochs=5)
model.save("my_model")
#"""

"""
model = keras.models.load_model("my_model")

seed = ["i", " ", "s", "i", "n", "g", " ", "a", " ", "s", "o", "n", "g", " ", "o", "f", " ", "m", "y", "s", "e", "l", "f", ".", " "]

for i in range(0, 100):
    vec = vectorizer.tokens_to_vectors(seed).reshape(1, len(seed), vectorizer.vocab_size())
    dist = model(vec)[0].numpy()
    #options = list(range(0, vectorizer.vocab_size()))
    #pred = np.random.choice(options, p=dist)
    char = vectorizer.int_to_token(np.argmax(dist))
    seed.append(char)

print("".join(seed))
"""
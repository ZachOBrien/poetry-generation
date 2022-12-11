"""
Generate poems using a Keras model trained on sequences of characters

"""

import pickle
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress tensorflow debugging info

import keras
import numpy as np

with open("vectorizer.pkl", "rb") as infile:
    vectorizer = pickle.load(infile)
print("loaded vectorizer")

model = keras.models.load_model("../trained_models/1/character_lm_model")
print("loaded model")

seed = ["i", " ", "s", "i", "n", "g", " ", "a", " ", "s", "o", "n", "g", " ", "o", "f", " ", "m", "y", "s", "e", "l", "f", ".", " "]

for i in range(0, 100):
    vec = vectorizer.tokens_to_vectors(seed).reshape(1, len(seed), vectorizer.vocab_size())
    dist = model(vec)[0].numpy()
    options = list(range(0, vectorizer.vocab_size()))
    pred = np.random.choice(options, p=dist)
    char = vectorizer.int_to_token(pred)
    seed.append(char)

print("".join(seed))
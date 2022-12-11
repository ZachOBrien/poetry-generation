"""
Generate poems using a Keras model trained on sequences of characters

"""

import pickle
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Suppress tensorflow debugging info

import keras
import numpy as np

PATH_TO_VECTORIZER = "model/vectorizer.pkl"
PATH_TO_MODEL = "model/character_based_lm"

with open(PATH_TO_VECTORIZER, "rb") as infile:
    vectorizer = pickle.load(infile)
print("loaded vectorizer")

model = keras.models.load_model(PATH_TO_MODEL)
print("loaded model")

seed_phrase = "i sing a song of myself "
seed_phrase_chars = list(seed_phrase)

MAX_POEM_LENGTH = 150  # in case we don't encounter a poem boundary character

for i in range(0, MAX_POEM_LENGTH):
    # Vectorize the seed phrase and give it the shape:
    # (batch_size, seq-length, vocab_size)
    vec = (vectorizer
           .tokens_to_vectors(list(seed_phrase_chars))
           .reshape(1, len(seed_phrase_chars), vectorizer.vocab_size()))
    
    # Ask the model for a prediction on the current seed phrase
    pred_distribution = model(vec)[0].numpy()
    
    # Make a choice over the probability distribution, like in the Shannon method
    options = list(range(0, vectorizer.vocab_size()))
    idx = np.random.choice(options, p=pred_distribution)
    
    # Turn the chosen value into a character and append it to the seed
    char = vectorizer.int_to_token(idx)
    seed_phrase_chars.append(char)
    
    # If the character is one of the poem segmenting symbols, end early
    if char in ["@", "$"]:
        break

print("".join(seed_phrase_chars))
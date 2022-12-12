"""
Builds training, validation, and testing datasets in the Tensorflow format

REQUIRES:
    - data/leaves_of_grass.csv has already been derived
"""

import itertools

from keras.utils import timeseries_dataset_from_array
import pandas as pd
import numpy as np

from dataprep.neural_lm_dataprep import (
    Vectorizer,
    preprocess_for_neural_lm,
)


# Load the poems from disk
leaves_of_grass_df = pd.read_csv("data/leaves_of_grass.csv")

leaves_of_grass_df.head(2)

# Pull only the poems out of the dataset
poems = list(leaves_of_grass_df["poem"])
print("Snippet of original poems:")
print(poems[0][:17])
print()

# Preprocess the poems with the steps outlined above
poems = [preprocess_for_neural_lm(poem) for poem in poems]
print("Snippet after preprocessing:")
print(poems[0][:17], "...")

# Fit a vectorizer to the vocabulary of characters
vectorizer = Vectorizer()
vectorizer.fit(itertools.chain(*poems))
# Vectorize all characters
vectorized_poems = [vectorizer.tokens_to_vectors(poem) for poem in poems]

print("Vocabulary:")
print(vectorizer.vocabulary())

# Use 70% of the poems for training, 15% for validation 
# during testing, and 15% for final model evaluation.
# IMPORTANT: I first split entire *poems* into training, test,
#            and evaluation. I don't want half of a poem to be in one
#            set and the other half to be in another
train_set_size = int(0.7 * len(vectorized_poems))
validation_set_size = int(0.15 * len(vectorized_poems))
test_set_size = int(0.15 * len(vectorized_poems))

train_set = vectorized_poems[:train_set_size]
train_set = np.array(list(itertools.chain(*train_set)))
print(f"# characters in train set:       {len(train_set)}")

validation_set = vectorized_poems[train_set_size:(train_set_size + validation_set_size)]
validation_set = np.array(list(itertools.chain(*validation_set)))
print(f"# characters in validation set:  {len(validation_set)}")

test_set = vectorized_poems[train_set_size+validation_set_size:]
test_set = np.array(list(itertools.chain(*test_set)))
print(f"# characters in test set:        {len(test_set)}")

# Each sample given to the model for training will be a sequence of 100 characters
SEQUENCE_LENGTH = 100
# I do not want to skip any samples, so sampling rate is 1
SAMPLING_RATE = 1
BATCH_SIZE = 4096

# Build timeseries datasets using Keras helpers
print("Building train dataset...")
train_dataset = timeseries_dataset_from_array(
    data=train_set[:-SEQUENCE_LENGTH],
    targets=train_set[SEQUENCE_LENGTH:],
    sampling_rate=SAMPLING_RATE,
    sequence_length=SEQUENCE_LENGTH,
    batch_size=BATCH_SIZE)
train_dataset.save(path="../data/training_dataset_tensorflow/", compression="GZIP")

print("Building validation dataset...")
validation_dataset = timeseries_dataset_from_array(
    data=validation_set[:-SEQUENCE_LENGTH],
    targets=validation_set[SEQUENCE_LENGTH:],
    sampling_rate=SAMPLING_RATE,
    sequence_length=SEQUENCE_LENGTH,
    batch_size=BATCH_SIZE)
validation_dataset.save(path="../data/validation_dataset_tensorflow/", compression="GZIP")

print("Building testing dataset...")
testing_dataset = timeseries_dataset_from_array(
    data=test_set[:-SEQUENCE_LENGTH],
    targets=test_set[SEQUENCE_LENGTH:],
    sampling_rate=SAMPLING_RATE,
    sequence_length=SEQUENCE_LENGTH,
    batch_size=BATCH_SIZE)
testing_dataset.save(path="../data/testing_dataset_tensorflow/", compression="GZIP")

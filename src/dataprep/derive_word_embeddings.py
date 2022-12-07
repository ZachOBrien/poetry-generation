"""
Derive word embeddings

"""

import pandas as pd
from gensim.models.word2vec import Word2Vec

from dataprep.leaves_of_grass_tokenize import tokenize_poem


# Hyperparameters for the Word2Vec model
EMBEDDING_SIZE = 100
WINDOW = 5
TYPE_FREQUENCY_THRESHOLD = 5
WORKERS = 4
SG = 1

leaves_of_grass_df = pd.read_csv("../../data/leaves_of_grass.csv")

tokenized_poems = list(tokenize_poem(poem) for poem in leaves_of_grass_df["poem"])

word2vec_model = Word2Vec(
    tokenized_poems,
    vector_size=EMBEDDING_SIZE,
    window=WINDOW,
    min_count=TYPE_FREQUENCY_THRESHOLD,
    workers=WORKERS,
    sg=SG
)

word2vec_model.wv.save_word2vec_format("embeddings.bin", binary=True)

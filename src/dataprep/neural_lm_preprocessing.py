
"""
Functionality for preprocessing data to be used in neural language models

"""

import numpy as np
from keras.utils import to_categorical


class Vectorizer:
    def __init__(self):
        self.token_to_int_mapping = {}
        self.int_to_token_mapping = {}
    
    def fit(self, tokens):
        """Fit the vectorizer to a vocabulary 

        Args:
            tokens (list[str]): A list of tokens
        """
        for token in tokens:
            if token not in self.token_to_int_mapping:
                self._insert_token(token)
        self.int_to_token_mapping = {v:k for k,v in self.token_to_int_mapping.items()}

    def vocab_size(self):
        """Get the size of the vocabulary

        Returns:
            int: The size of the vocabulary
        """
        return len(self.token_to_int_mapping)

    def tokens_to_vectors(self, tokens):
        """One-hot encode a token in a vector

        Args:
            tokens (list[str]): Tokens to vectorize
        """
        return to_categorical(
            [self.token_to_int(t) for t in tokens], num_classes=self.vocab_size()
        )

    def vectors_to_tokens(self, vectors):
        """Convert one-hot encoded vectors back into tokens

        Args:
            vectors (list[int]): One-hot encoded vectors

        Returns:
            list[str]: A list of tokens
        """
        return [self.int_to_token_mapping[idx] for idx in np.argmax(vectors, axis=1)]

    def token_to_int(self, token):
        """Convert a token into an integer representation based on the fitted vocabulary

        Args:
            token (str): A token

        Returns:
            int: The token's index in the vocbulary
        """
        return self.token_to_int_mapping[token]

    def int_to_token(self, i):
        """Convert an integer into a token in the vocabulary

        Args:
            i (int): An integer

        Returns:
            str: A token in the fitted vocabulary
        """
        return self.int_to_token_mapping[i]

    def _insert_token(self, token):
        """Insert a token into the mapping

        Args:
            token (str): A token
        """
        if self.token_to_int_mapping == {}:
            self.token_to_int_mapping[token] = 0
        else:
            curr_max = max(self.token_to_int_mapping.values())
            self.token_to_int_mapping[token] = curr_max + 1


def preprocess_for_neural_lm(poem):
    """Preprocess a poem for use with a neural language model

    Args:
        poem (str): A single poem
    """
    poem = _lowercase_and_wrap_with_markers(poem)
    poem = _split_into_characters(poem)
    poem = _replace_numeric(poem, " ")
    return poem

def _lowercase_and_wrap_with_markers(poem):
    """Standardize a poem for use in a neural language model

    Standardization involves:
    1. Lowercasing all characters in the poem
    2. Wrapping the poem in start (@) and end ($) characters

    Args:
        poem (str): A poem
    """
    # 1. lowercase the poem
    poem = poem.lower()
    # 2. wrap the poem in a starting "@" and ending "$"
    poem = "@" + poem + "$"
    return poem


def _split_into_characters(s):
    """Split a string into characters

    Args:
        s (str): String to split

    Returns:
        list[str]: The original string's characters
    """
    return list(s)


def _replace_numeric(chars, replace_with):
    """Replace numeric characters in a list of characters

    Args:
        chars (list[str]): A list of characters
    """
    return [c if not c.isnumeric() else replace_with for c in chars]

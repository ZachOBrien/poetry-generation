"""
Unit tests for the ngram langauge model preprocessing module

"""

import pytest
import numpy as np


from dataprep.neural_lm_preprocessing import (
    Vectorizer,
    _lowercase_and_wrap_with_markers,
    _split_into_characters,
    _replace_numeric
) 


class TestCharVectorizer:
    @pytest.fixture(autouse=True)
    def _setup_vectorizer(self):
        self.vec = Vectorizer()
        seq = ["a", "b", "c", "a", "a", "b", "d", "f", "c"]
        self.vec.fit(seq)

    def test_token_to_int(self):
        assert self.vec.token_to_int("a") == 0
        assert self.vec.token_to_int("b") == 1
        assert self.vec.token_to_int("c") == 2
        assert self.vec.token_to_int("d") == 3
        assert self.vec.token_to_int("f") == 4
    
    def test_int_to_token(self):
        assert self.vec.int_to_token(0) == "a"
        assert self.vec.int_to_token(1) == "b"
        assert self.vec.int_to_token(2) == "c"
        assert self.vec.int_to_token(3) == "d"
        assert self.vec.int_to_token(4) == "f"

    def test_vocab_size(self):
        assert self.vec.vocab_size() == 5

    def test_tokens_to_vector(self):
        tokens = ["a", "b", "c", "d", "f"]
        expected = np.array([[1, 0, 0, 0, 0],
                             [0, 1, 0, 0, 0],
                             [0, 0, 1, 0, 0],
                             [0, 0, 0, 1, 0],
                             [0, 0, 0, 0, 1]])
        actual = self.vec.tokens_to_vectors(tokens)
        assert np.array_equal(actual, expected)

    def test_vectors_to_token(self):
        vectors = np.array([[1, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 1]])
        expected = ["a", "b", "c", "d", "f"]
        actual = self.vec.vectors_to_tokens(vectors)
        assert actual == expected

class TestStandardize:
    def test_prepare_poem(self):
        poem = "One's-self I sing. A simple \n separate person."
        expected = "@one's-self i sing. a simple \n separate person.$"
        actual = _lowercase_and_wrap_with_markers(poem)
        assert actual == expected


class TestSplit:
    def test_split_into_characters(self):
        expected = ["o", "n", "e", "'", "s", "-", "s", "e", "l", "f", " ", "i", " ", "s", "i", "n", "g", "."]
        actual = _split_into_characters("one's-self i sing.")
        assert actual == expected


class TestReplaceNumeric:
    def test_replace_numeric(self):
        assert _replace_numeric(["a", "1", "2", "d", "7"], "$") == ["a", "$", "$", "d", "$"]
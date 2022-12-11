"""
Unit tests for the ngram langauge model preprocessing module

"""

from dataprep.ngram_lm_preprocessing import preprocess_for_ngram_lm


class TestTokenizePoem:
    def test_tokenize_poem(self):
        poem = "One's-self I sing. A simple \n separate person."
        expected = ["one's-self", "i", "sing", ".", "a", "simple", "<nl>", "separate", "person", "."]
        actual = preprocess_for_ngram_lm(poem, "<nl>")
        assert actual == expected

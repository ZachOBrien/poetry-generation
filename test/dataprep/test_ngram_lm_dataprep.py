"""
Unit tests for the ngram langauge model preprocessing module

"""

from dataprep.ngram_lm_dataprep import (
    preprocess_for_ngram_lm,
    postprocess_for_ngram_lm
)


class TestPreprocessPoem:
    def test_preprocess_poem(self):
        poem = "One's-self I sing. A simple \n separate person."
        expected = ["one's-self", "i", "sing", ".", "a", "simple", "<nl>", "separate", "person", "."]
        actual = preprocess_for_ngram_lm(poem, "<nl>")
        assert actual == expected


class TestPostprocessPoem:
    def test_postprocess_poem(self):
        poem = "<p><p> hush '   d me ,   NEWLINE i dance with  the <UNK> refrain toward sundown , <nl> thou <UNK> time . </p></p>"
        expected = "hush ' d me , \n i dance with the refrain toward sundown , \n thou time ."
        actual = postprocess_for_ngram_lm(poem)
        print("HI")
        print(actual)
        assert actual == expected

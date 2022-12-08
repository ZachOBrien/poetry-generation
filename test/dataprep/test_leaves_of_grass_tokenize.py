"""
Unit tests for the leaves_of_grass_tokenize module

"""

from dataprep.preprocessing import tokenize_poem


class TestTokenizePoem:
    def test_tokenize_poem(self):
        poem = "One's-self I sing. A simple \n separate person."
        expected = ["one's-self", "i", "sing", ".", "a", "simple", "<nl>", "separate", "person", "."]
        actual = tokenize_poem(poem, "<nl>")
        assert actual == expected

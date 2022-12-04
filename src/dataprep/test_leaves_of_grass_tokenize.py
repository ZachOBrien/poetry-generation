"""
Unit tests for the leaves_of_grass_tokenize module

"""

from leaves_of_grass_tokenize import tokenize_poem


class TestTokenizePoem:
    def test_tokenize_poem(self):
        poem = "One's-self I sing. A simple \n separate person."
        expected = ["<p>", "<p>", "one's-self", "i", "sing", ".", "a", "simple", "<nl>", "separate", "person", ".", "</p>", "</p>"]
        actual = tokenize_poem(poem, 3, "<nl>", "<p>", "</p>")
        assert actual == expected

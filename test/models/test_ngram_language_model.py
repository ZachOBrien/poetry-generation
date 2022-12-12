"""
Unit tests for the ngram language model

"""

from pytest import approx

from models.ngram_language_model import LanguageModel


class TestModelTraining:
    def test_train_iamsam(self):
        bigram_model = LanguageModel(2, False, replacement_threshold=1)
        expected_ngram_frequencies = {
            ("<p>", "one"): 1, 
            ("one", "self"): 1, 
            ("self", "i"): 1, 
            ("i", "sing"): 2, 
            ("sing", "i"): 1, 
            ("sing", "of"): 1, 
            ("of", "</p>"): 1
        }
        bigram_model.train(["<p>", "one", "self", "i", "sing", "i", "sing", "of", "</p>"])
        assert bigram_model.n_gram_frequencies == expected_ngram_frequencies


class TestCountNgramsWithPrefix:
    def test_bigram_model(self):
        bigram_model = LanguageModel(2, False, replacement_threshold=1)
        bigram_model.train(
            ["<p>", "one", "self", "i", "sing", "i", "sing", "of", "</p>",
             "<p>", "i", "sing", "a", "cool", "song", "</p>"]
        )
        assert bigram_model.count_ngrams_with_prefix(("<p>",)) == 2
        assert bigram_model.count_ngrams_with_prefix(("i",)) == 3
        assert bigram_model.count_ngrams_with_prefix(("</p>",)) == 1

    def test_trigram_model(self):
        trigram_model = LanguageModel(3, False, replacement_threshold=1)
        trigram_model.train(
            ["<p>", "one", "self", "i", "sing", "i", "sing", "of", "</p>",
             "<p>", "i", "sing", "a", "cool", "song", "</p>"]
        )
        assert trigram_model.count_ngrams_with_prefix(("<p>", "one")) == 1
        assert trigram_model.count_ngrams_with_prefix(("i", "sing")) == 3
        assert trigram_model.count_ngrams_with_prefix(("</p>", "<p>")) == 1


class TestModelScoring:
    def test_bigramlaplace(self):
        bigram_model = LanguageModel(2, True, replacement_threshold=1)
        bigram_model.train(
            ["<p>", "one", "self", "i", "sing", "i", "sing", "a", "cool", "song", "</p>",
             "<p>", "i", "sing", "a", "cool", "song", "</p>"]
        )
        assert approx(bigram_model.score(("i", "sing"))) == 0.33333333
        assert approx(bigram_model.score(("cool", "song"))) == 0.27272727

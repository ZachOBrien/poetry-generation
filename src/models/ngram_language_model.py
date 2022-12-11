"""
This module implements a basic n-gram language model

The implementation was adapted from my homework 2 submission.
"""

import random

from nltk.util import ngrams
import numpy as np

from dataprep.preprocessing import tokenize_poem


class LanguageModel:
    UNK = "<UNK>"
    REPLACEMENT_THRESHOLD = 2
    POEM_BEGIN = "<p>"
    POEM_END = "</p>"

    def __init__(self, n, is_laplace_smoothing):
        """Initializes an untrained LanguageModel

        Parameters:
            n_gram (int): the n-gram order of the language model to create
            is_laplace_smoothing (bool): whether or not to use Laplace smoothing
        """
        self.n = n
        self.is_laplace_smoothing = is_laplace_smoothing
        self.token_frequency_distribution = None
        self.n_gram_frequencies = None
        self.vocabulary = None

    def train(self, tokens):
        """Trains the language model on tokens

        Parameters:
            tokens (list[str]): Tokens to use for training. Each poem must be wrapped
                                with n-1 POEM_START and POEM_END symbols

        Returns:
          None
        """
        # TODO: Can frequency_distribution just be replaced with Counter() ??
        self.token_frequency_distribution = frequency_distribution(tokens)
        tokens = replace_infrequent_tokens(
            tokens,
            self.token_frequency_distribution,
            threshold=self.REPLACEMENT_THRESHOLD,
            replacement_token=self.UNK,
        )
        self.vocabulary = set(tokens)
        self.n_gram_frequencies = frequency_distribution(
            ngrams(tokens, self.n)
        )

    def score(self, tokens):
        """Calculates the probability score for a given string representing a single poem.

        Parameters:
          tokens (list[str]): A sequence of tokens

        Returns:
          float: the probability value of the given string for this model
        """
        tokens = replace_infrequent_tokens(
            tokens,
            self.token_frequency_distribution,
            threshold=self.REPLACEMENT_THRESHOLD,
            replacement_token=self.UNK,
        )
        n_grams = ngrams(tokens, self.n)
        log_probabilities = [
            self.maximum_likelihood_estimate(ng) for ng in n_grams
        ]
        return np.exp(np.sum(log_probabilities))

    def maximum_likelihood_estimate(self, n_gram):
        """Calculates the MLE as a relative frequency in log probability for a single n_gram.

        If the ngram is: (w_1, w_2, ..., w_n)
        The prefix is:   (w_1, w_2, ..., w_n-1)
        And the relative frequency is:
          C(w_1, w_2, ..., w_n) / C(w_1, w_2, ..., w_n-1)

        Parameters:
          n_gram (tuple[str]): An n_gram

        Returns
          float: the probability value of the given n_gram for this model
        """
        ngram_freq = self.n_gram_frequencies.get(n_gram, 0)
        ngram_prefix_freq = self.count_ngrams_with_prefix(n_gram[:-1])
        if self.is_laplace_smoothing:
            ngram_freq += 1
            ngram_prefix_freq += len(self.vocabulary)

        with np.errstate(divide="ignore"):
            return np.log(ngram_freq / ngram_prefix_freq)

    def generate_poem(self):
        """Generates a single poem from a trained language model using the Shannon technique.

        Returns:
          str: the generated poem
        """
        poem = "<p>" * max(1, (self.n - 1))
        current_prefix = tuple(
            [self.POEM_BEGIN for _ in range((self.n - 1))]
        )
        while True:
            predicted_token = self.sample_token_given_prefix(current_prefix)
            if predicted_token == self.POEM_END:
                poem += self.POEM_END * max(1, (self.n - 1))
                return poem
            else:
                poem += (" " + predicted_token)
                if self.n > 1:
                    current_prefix = current_prefix[1:] + (predicted_token,)

    def sample_token_given_prefix(self, prefix):
        """Samples a token given some prefix sequence of tokens

        Parameters:
            prefix (tuple[str]): An n_gram of length n-1

        Returns:
            token (str): A randomly sampled token given the prefix
        """
        distribution = self.next_token_prob_dist_given_prefix(prefix)
        candidate_tokens = list(distribution.keys())
        choice = random.choices(
            candidate_tokens, weights=distribution.values(), k=1
        )[0]
        return choice

    def next_token_prob_dist_given_prefix(self, prefix):
        """Get the probability distribution for the next token given some sequence of tokens

        Parameters:
            prefix (tuple[str]): An sequence of tokens of length n-1

        Returns:
            dict[str, float]: Probability distribution of tokens that could come after the given sequence
        """
        ngram_prefix_freq = self.count_ngrams_with_prefix(prefix)
        candidate_tokens = [
            ng[-1]
            for ng in self.n_gram_frequencies.keys()
            if (ng[:-1] == prefix) and (ng[-1] != "<s>")
        ]
        prob_dist = dict()
        for token in candidate_tokens:
            ngram_freq = self.n_gram_frequencies.get(prefix + (token,))
            prob_dist[token] = ngram_freq / ngram_prefix_freq
        return prob_dist

    def count_ngrams_with_prefix(self, prefix):
        """Get the number of ngrams which have some prefix

        Parameters:
          prefix (tuple[str]): A prefix which must have length <= self.n_gram

        Returns:
          The numer of ngrams which have the same prefix as the given prefix
        """
        return sum(
            [
                count
                for ng, count in self.n_gram_frequencies.items()
                if ng[0 : len(prefix)] == prefix
            ]
        )

    def generate(self, n):
        """Generates n poems from a trained language model using the Shannon technique.
        Parameters:
          n (int): the number of poems to generate

        Returns:
          list[str]: A list of poems
        """
        return [self.generate_poem() for _ in range(n)]


def replace_infrequent_tokens(
    tokens, frequency_distribution, threshold, replacement_token
):
    """Replaces all tokens which occur with frequency below some threshold

    Parameters:
      tokens (list[str]): A list of tokens
      frequency_distribution (str, int]): Frequency distribution of tokens
      threshold (int): A natural number representing the count necessary
                       for a token to not be replaced
      replacement_token (str): Token which replaces infrequent tokens

    Returns:
      A list of the original tokens, but with each token that occurs
      less frequently than `threshold` replaced with `replacement_token`

    Examples:
      >>> replace_infrequent_tokens(["a", "a", "b", "c", "c", "a", "c"], 2, "<UNK>")
      ["a", "a", "<UNK>", "c", "c", "a", "c"]

    """
    return [
        token
        if frequency_distribution.get(token, 0) >= threshold
        else replacement_token
        for token in tokens
    ]


def frequency_distribution(items):
    """Compute the frequency distribution of items in a list

    Parameters:
      items (list): A list of items to count

    Returns:
      A mapping of {Item -> Count}, or how many times each item
      appeared in `items`
    """
    distribution = {}
    for x in items:
        if x in distribution:
            distribution[x] += 1
        else:
            distribution[x] = 1
    return distribution


def ngram_prefix(n_gram):
    """Get all but the last word in an n_gram

    Parameters:
      n_gram (tuple[str]): An n-gram

    Rreturns:
      tuple[str]: An n-gram which has all but the last token from the given `n_gram`
    """
    return n_gram[0 : len(n_gram) - 1]

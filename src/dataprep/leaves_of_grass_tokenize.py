"""
Functionality for preprocessing data to be used in n-gram language models

"""

from nltk.tokenize import word_tokenize
from nltk.util import pad_sequence


def tokenize_poem(poem, n, newline_sym="<nl>", poem_start_sym="<p>", poem_end_sym="</p>"):
    """Convert a poem into tokens ready to be given to an `n`-gram language model

    Args:
        poem (str): A poem as a single string
        n (int): The `n` in n-gram. If this is 2, the function makes 2-grams
        newline_sym (str): Symbol to replace newline characters with
        poem_start_sym (str): Symbol to pad at the start of the poem
        poem_end_sym (str): Symbol to pad at the end of the poem
    
    Returns:
        list[str]: A list of tokens
    """
    poem = poem.lower()
    poem = poem.replace("\n", "NEWLINE")
    poem = word_tokenize(poem)
    poem = [word if not word == "NEWLINE" else newline_sym for word in poem]
    poem = list(pad_sequence(
        poem,
        pad_left=True, 
        left_pad_symbol=poem_start_sym,
        pad_right=True,
        right_pad_symbol=poem_end_sym,
        n=n
    ))
    return poem
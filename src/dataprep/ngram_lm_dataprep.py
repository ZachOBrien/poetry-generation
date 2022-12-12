"""
Functionality for preprocessing data to be used in n-gram language models

"""

import re
from nltk.tokenize import word_tokenize


def preprocess_for_ngram_lm(poem, newline_sym="<nl>"):
    """Convert a poem into tokens ready to be given to an `n`-gram language model

    Args:
        poem (str): A poem as a single string
        newline_sym (str): Symbol to replace newline characters with
    
    Returns:
        list[str]: A list of tokens
    """
    poem = poem.lower()
    poem = poem.replace("\n", "NEWLINE")
    poem = word_tokenize(poem)
    poem = [word if not word == "NEWLINE" else newline_sym for word in poem]
    return poem


def postprocess_for_ngram_lm(poem):
    """Postprocess a poem produced by the n-gram language model

    Args:
        poem (str): A poem

    Returns:
        str: The poem, postprocessed
    """
    replace_with_single_space = " +"
    replace_with_empty = "<(|p|\/p|UNK|)>"
    replace_with_newline = "<nl>|NEWLINE"

    poem = re.sub(replace_with_empty, "", poem)
    poem = re.sub(replace_with_newline, "\n", poem)
    poem = re.sub(replace_with_single_space, " ", poem)
    poem = poem.strip()

    return poem
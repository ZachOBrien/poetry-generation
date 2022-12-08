"""
Functionality for parsing Project Gutenberg's copy of "Leaves of Grass", by Walt Whitman

"""

import itertools

import pandas as pd

from dataprep.list_utils import (
    remove_leading_and_trailing,
    split_into_blocks
)

   
def is_book_title(line):
    """Is this line a book heading?

    Args:
        line (list[str]): A line of text from the document

    Returns:
        bool: True if the line is a book heading
    """
    return len(line) >= 4 and line[0:4] == "BOOK"


def is_poem_title(line):
    """Is this line a poem title?

    Args:
        line (list[str]): A line of text from the document

    Returns:
        bool: True if the line is a poem title
    """
    # ASSUMPTION: all lines which start with a character in the alphabet and do not mark the beginning of a book are poem titles
    return len(line) > 0 and (not is_book_title(line)) and line[0].isalpha()


def read_poem_body(lines):
    """Read the next poem out of `lines`

    Args:
        lines (list[str]): A list of lines of poetry

    Returns:
        list[str]: A poem, split into lines
    """
    still_in_poem = lambda line: not (is_poem_title(line) or is_book_title(line))
    poem_lines = list(itertools.takewhile(still_in_poem, lines))
    poem_lines = remove_leading_and_trailing(poem_lines, lambda char: char == "\n")
    return poem_lines


def read_book_body(lines):
    """Read the next book out of `lines`

    Args:
        lines (list[str]): A list of lines of poetry

    Returns:
        list[str]: A book, split into lines
    """
    still_in_book = lambda line: not is_book_title(line)
    return list(itertools.takewhile(still_in_book, lines))


def split_into_poems(lines):
    """Split lines of poetry into individual poems

    Args:
        lines (list[str]): A list of lines of poetry

    Returns:
        list[tuple[str, list[str]]]: A list of poems, where each poem is a 2-tuple
                                     with a title and lines of text
    """
    return split_into_blocks(lines, is_poem_title, read_poem_body)
        

def split_into_books(lines):
    """Split lines of poetry into books

    Args:
        lines (list[str]): A list of lines of poetry

    Returns:
        list[tuple[str, list[str]]]: A list of books, where each book is a 2-tuple
                                     with its number/name and lines of text
    """                              
    return split_into_blocks(lines, is_book_title, read_book_body)


def leaves_of_grass_gutenberg_to_df(lines):
    """Convert a leaves of grass copy from Project Gutenberg into a DataFrame of poems

    Args:
        lines (list[str]): Lines from the Project Gutenberg .txt file
    """
    books = split_into_books(lines)
    all_poems = []
    for book_title, book_content in books:
        poems = split_into_poems(book_content)
        for poem_title, poem_content in poems:
            all_poems.append((book_title.strip(), poem_title.strip(), ("".join(poem_content)).strip()))
    return pd.DataFrame(all_poems, columns=["book_title", "poem_title", "poem"])
            
"""
Unit tests for the `list_utils` module

"""

import itertools

from list_utils import (
    remove_leading_and_trailing,
    split_into_blocks
)


class TestRemoveLeadingAndTrailing:
    def test_empty_list(self):
        assert remove_leading_and_trailing([], lambda x: x % 2 == 0) == []

    def test_singleton_list(self):
        assert remove_leading_and_trailing([2], lambda x: x % 2 == 0) == []
    
    def test_list_with_some_items_in_the_middle(self):
        assert remove_leading_and_trailing([2, 2, 1, 1, 1, 2], lambda x: x % 2 == 0) == [1, 1, 1]

    def test_list_with_passing_items_mixed_in(self):
        assert remove_leading_and_trailing([2, 2, 1, 2, 4, 3, 5, 2, 2, 2], lambda x: x % 2 == 0) == [1, 2, 4, 3, 5]

    def test_remove_newlines(self):
        poem = ["\n", "\n", "  what a cool idea.\n", "\n"]
        expected = ["  what a cool idea.\n"]
        actual = remove_leading_and_trailing(poem, lambda x: x == "\n")
        assert actual == expected

    def test_remove_newlines_but_none_to_remove(self):
        poem = ["  what a cool idea.\n", "I like that a lot."]
        expected = ["  what a cool idea.\n", "I like that a lot."]
        actual = remove_leading_and_trailing(poem, lambda x: x == "\n")
        assert actual == expected




def _is_even(x):
    return x % 2 == 0

def _read_evens(lst):
    return list(itertools.takewhile(_is_even, lst))

class TestSplitIntoBlocks:
    def test_split_empty(self):
        expected = []
        actual = split_into_blocks([], _is_even, _read_evens)
        assert actual == expected

    def test_split_small(self):
        expected = [(2, [4])]
        actual = split_into_blocks([2, 4], _is_even, _read_evens)
        assert actual == expected

    def test_split(self):
        expected = [(2, [4, 4]), (6, [8, 8])]
        actual = split_into_blocks([2, 4, 4, 3, 3, 6, 8, 8], _is_even, _read_evens)
        assert actual == expected

    def test_split(self):
        expected = [(2, [4, 4]), (10, []), (6, [8, 8])]
        actual = split_into_blocks([2, 4, 4, 3, 10, 3, 6, 8, 8], _is_even, _read_evens)
        assert actual == expected
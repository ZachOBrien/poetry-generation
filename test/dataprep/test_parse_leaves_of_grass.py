
"""
Unit tests for the `parse_leaves_of_grass` module

"""


from dataprep.parse_leaves_of_grass import (
    is_book_title,
    is_poem_title,
    read_poem_body,
    read_book_body,
    split_into_poems,
    split_into_books
)


class TestIsBookTitle:
    def test_is_book_title(self):
        assert is_book_title("BOOK I. INSCRIPTIONS") is True

    def test_is_not_book_title_empty(self):
        assert is_book_title("") is False

    def test_is_not_book_title_typo(self):
        assert is_book_title("BOK I. INSCRIPTIONS") is False

    def test_is_not_book_title_lowercase(self):
        assert is_book_title("book I. INSCRIPTIONS") is False


class TestIsPoemTitle:
    def test_is_poem_title(self):
        assert is_poem_title("a title here") is True

    def test_is_not_poem_title_empty(self):
        assert is_poem_title("") is False
    
    def test_is_not_poem_title_newline(self):
        assert is_poem_title("\n") is False

    def test_is_not_poem_title_spaces(self):
        assert is_poem_title(" not a title here") is False


class TestReadPoem:
    def test_read_poem_cutoff_by_another_poem(self):
        lines = ["  what a\n", "  beautiful day\n", "  it was that day.", "next poem"]
        expected = ["  what a\n", "  beautiful day\n", "  it was that day."]
        actual = read_poem_body(lines)
        assert actual == expected

    def test_read_poem_cutoff_by_next_book(self):
        lines = ["  what a\n", "  beautiful day\n", "  it was that day.", "BOOK II."]
        expected = ["  what a\n", "  beautiful day\n", "  it was that day."]
        actual = read_poem_body(lines)
        assert actual == expected


class TestReadBook:
    def test_read_book(self):
        lines = ["\n", "some book", "  body", "BOOK II."]
        expected = ["\n", "some book", "  body"]
        actual = read_book_body(lines)
        assert actual == expected


class TestSplitIntoPoems:
    def test_split_into_poems(self):
        lines = [
            "One's-Self I Sing",
            "  One's-self I sing, a simple separate person,",
            "  Yet utter the word Democratic, the word En-Masse.",
            "As I Ponder'd in Silence",
            "  As I ponder'd in silence,",
            "  Returning upon my poems, considering, lingering long,",
            "BOOK II."
        ]
        expected = [
            (
                "One's-Self I Sing",
                [
                    "  One's-self I sing, a simple separate person,",
                    "  Yet utter the word Democratic, the word En-Masse.",
                ]
            ),
            (
                "As I Ponder'd in Silence",
                [
                    "  As I ponder'd in silence,",
                    "  Returning upon my poems, considering, lingering long,"
                ]
            )
        ]
        actual = split_into_poems(lines)
        assert actual == expected

class TestSplitIntoBooks:
    def test_split_book(self):
        book_lines = [
            "BOOK I.  INSCRIPTIONS",
            "\n",
            "some cool poetry here",
            "\n",
            "  yada yada",
            "  and whatnot",
            "\n",
            "\n",
            "BOOK II. SOMETHING ELSE",
            "some more cool poetry",
            "  and something genius",
        ]
        expected = [
            (
                "BOOK I.  INSCRIPTIONS",
                ["\n", "some cool poetry here", "\n", "  yada yada",
                 "  and whatnot", "\n", "\n"]
            ),
            (
                "BOOK II. SOMETHING ELSE",
                ["some more cool poetry", "  and something genius"]
            )
        ]
        actual = split_into_books(book_lines)
        assert actual == expected
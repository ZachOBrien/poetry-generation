"""
Derive cleaned leaves of grass data

"""

import pandas as pd

from parse_leaves_of_grass import split_into_poems, split_into_books

with open("../../data/leaves-of-grass.txt") as f:
    lines = f.readlines()

books = split_into_books(lines)

all_poems = []
for book_title, book_content in books:
    poems = split_into_poems(book_content)
    for poem_title, poem_content in poems:
        all_poems.append((book_title.strip(), poem_title.strip(), ("".join(poem_content)).strip()))

df = pd.DataFrame(all_poems, columns=["book_title", "poem_title", "poem"])
df.to_csv("../../data/leaves_of_grass.csv")

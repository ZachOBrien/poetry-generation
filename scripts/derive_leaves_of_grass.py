"""
Derive cleaned leaves of grass data

"""

from dataprep.parse_leaves_of_grass import leaves_of_grass_gutenberg_to_df


with open("../data/leaves-of-grass.txt") as f:
    lines = f.readlines()
    leaves_of_grass_gutenberg_to_df(lines).to_csv("../data/leaves_of_grass.csv")

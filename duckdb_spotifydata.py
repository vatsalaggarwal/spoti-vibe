import duckdb
from tqdm import tqdm

# read from a file using fully auto-detected settings
lyrics = duckdb.read_csv("/Users/vatsalaggarwal/Downloads/ds2.csv")

# print(len(lyrics))

# lyrics.columns
["title", "tag", "artist", "year", "views", "features", "lyrics", "id"]

all_data = duckdb.sql("SELECT title, artist, lyrics, id FROM lyrics").fetchall()

titles, artists, lyrics, ids = [], [], [], []
for row in tqdm(all_data):
    titles.append(row[0])
    artists.append(row[1])
    lyrics.append(row[2])
    ids.append(row[3])

import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="lyrics")

new_ids = collection.add(
    documents=lyrics,
    metadatas=[
        {"title": title, "artist": artist}
        for title, artist in tqdm(zip(titles, artists))
    ],
    ids=[str(x) for x in ids],
)

results = collection.query(
    query_texts=["This is a sad song."],
    n_results=2,
)

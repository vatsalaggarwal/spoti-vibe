import duckdb
import tiktoken
from chromadb.config import Settings
from tqdm import tqdm

# read from a file using fully auto-detected settings
lyrics = duckdb.read_csv("/Users/vatsalaggarwal/Downloads/ds2.csv")

# print(len(lyrics))

# lyrics.columns
# ["title", "tag", "artist", "year", "views", "features", "lyrics", "id"]

all_data = duckdb.sql("SELECT title, artist, lyrics, id FROM lyrics").fetchall()

titles, artists, lyrics, ids = [], [], [], []
for row in tqdm(all_data):
    titles.append(row[0])
    artists.append(row[1])
    lyrics.append(row[2])
    ids.append(row[3])

# TOTAL = 1000

# titles, artists, lyrics, ids = titles[:TOTAL], artists[:TOTAL], lyrics[:TOTAL], ids[:TOTAL]

import chromadb

chroma_client = chromadb.Client(
    Settings(chroma_db_impl="duckdb+parquet", persist_directory="chrome_db/")
)

collection = chroma_client.create_collection(name="lyrics")
enc = tiktoken.encoding_for_model("text-embedding-ada-002")

import math
import random

# def calculate_tokens(text):
#     return len(enc.encode(text))
# Use encode_batch instead?
from tqdm import tqdm

# lyrics_random_sample = random.sample(lyrics, len(lyrics) // 10)
# token_lens = [
#     len(x) for x in tqdm(enc.encode_batch(lyrics_random_sample, num_threads=16))
# ]
# total_tokens = sum(token_lens) * len(lyrics) / len(token_lens)
# total_tokens_k = math.ceil(total_tokens) / 1000  # for 1K tokens calc
# total_cost = total_tokens_k * 0.0004

# token_lens = [len(enc.encode(x)) for x in tqdm(lyrics)]

new_ids = collection.add(
    documents=lyrics,
    metadatas=[
        {"title": title, "artist": artist}
        for title, artist in tqdm(zip(titles, artists))
    ],
    ids=[str(x) for x in ids],
)

# results = collection.query(
#     query_texts=["This is a sad song."],
#     n_results=2,
# )

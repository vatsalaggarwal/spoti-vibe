#!/usr/bin/env python3
from typing import List

from fastapi import FastAPI

from gateway import (Song, init, query_chain_with_text, query_with_embedding,
                     query_with_text)

app = FastAPI()
init("chroma_db/")


@app.post("/recommendations/")
async def get_recommendations(embedding: List[float]) -> List[Song]:
    return query_with_embedding(embedding)


@app.get("/search/{query_text}")
async def search_songs(query_text: str) -> List[Song]:
    return query_with_text(query_text)


# TODO: get a chain of recommendations from a query_text
@app.get("/search_chain/{query_text}")
async def search_songs_chain(query_text: str) -> List[Song]:
    return query_chain_with_text(query_text)

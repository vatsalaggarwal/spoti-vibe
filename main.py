#!/usr/bin/env python3
from fastapi import FastAPI
from typing import List
from gateway import init, query_with_embedding, query_with_text, Song


app = FastAPI()
init('chrome_db/')

@app.post("/recommendations/")
async def get_recommendations(embedding: List[float]) -> List[Song]:
    return query_with_embedding(embedding)

@app.get("/search/{query_text}")
async def search_songs(query_text: str) -> List[Song]:
    return query_with_text(query_text)

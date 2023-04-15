#!/usr/bin/env python3
from typing import List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from gateway import Song, init, query_chain_with_text, query_with_text

app = FastAPI()
app.mount("/.well-known", StaticFiles(directory="static"), name=".well-known")
init("my_chrome_db/")


@app.get("/search/{query_text}")
async def search_songs(query_text: str) -> List[Song]:
    return query_with_text(query_text)


# TODO: get a chain of recommendations from a query_text
@app.get("/search_chain/{query_text}")
async def search_songs_chain(query_text: str) -> List[Song]:
    return query_chain_with_text(query_text)

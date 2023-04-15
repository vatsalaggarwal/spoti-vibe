import requests
import chromadb
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from chromadb.config import Settings
from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    title: str
    artist: str
    youtube_url: str
    youtube_embed_code: str

YOUTUBE_API_KEY = 'AIzaSyCTEtqkIWKZzohXIQl9wwGP9xbqMrfHv9Y'
SPOTIFY_CLIENT_ID = '85b26ec8abec40b5ac0f7f68151c55d4'
SPOTIFY_CLIENT_SECRET = '6f81ebd168ee4ce6a90a6853f733c762'

chroma_client = None
sp = None

def init(chroma_dir):
    global chroma_client
    chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=chroma_dir))
    auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
    global sp
    sp = spotipy.Spotify(auth_manager=auth_manager)
    # return chroma_client, sp


def get_track_artist_from_spotify(title, artist):
    if title and artist:
        query = f"{title} {artist}"
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_url = track['external_urls']['spotify']
            track_id = track['id']
            embed_code = f'<iframe src="https://open.spotify.com/embed/track/{track_id}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'

            return track_url, embed_code
        else:
            print(f"No results found for {query}")
    else:
        print("Please provide both title and artist")

def get_youtube_url(song_title, artist):
    search_query = f"{song_title} {artist}"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&type=video&key={YOUTUBE_API_KEY}"
    
    response = requests.get(url)
    json_data = response.json()
    
    if 'items' in json_data:
        video_id = json_data['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        embed_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        return video_url, embed_code
    else:
        return "No results found", "No embed code found"

def _get_song(m: dict, use_youtube=True) -> Song:
    if use_youtube:
        url, embed = get_youtube_url(m['title'], m['artist'])
    else:
        url, embed = get_track_artist_from_spotify(m['title'], m['artist'])
    return Song(title=m['title'], artist=m['artist'], youtube_url=url, youtube_embed_code=embed)

def query_with_embedding(embedding: List[float], k: int = 5) -> List[Song]:
    collection = chroma_client.get_collection('lyrics')
    res = collection.query(query_embeddings=[embedding], n_results=k)
    return [_get_song(m) for m in res['metadatas'][0]]

def query_with_text(query_text: str, k: int = 5) -> List[Song]:
    collection = chroma_client.get_collection('lyrics')
    res = collection.query(query_texts=[query_text], n_results=k)
    return [_get_song(m) for m in res['metadatas'][0]]

# song_title = "Bohemian Rhapsody"
# artist = "Queen"

# url, embed_code = get_youtube_url(song_title, artist)
# print(f"URL: {url}\n\nEmbedded code:\n{embed_code}\n\n")

# url, embed_code = get_track_artist_from_spotify(song_title, artist)
# print(f"URL: {url}\n\nEmbedded code:\n{embed_code}")

if __name__ == "__main__":

    init(chroma_dir="/Users/rajatbansal/Documents/git/spoti-vibe/storage")
    results, metadatas = query_with_text("This is a sad song.", k=2)
    print(results)
    print(metadatas)

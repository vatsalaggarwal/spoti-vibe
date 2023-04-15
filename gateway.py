import requests

YOUTUBE_API_KEY = 'AIzaSyCTEtqkIWKZzohXIQl9wwGP9xbqMrfHv9Y'

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

# # Replace 'YOUR_API_KEY' with your actual YouTube Data API key
# song_title = "Bohemian Rhapsody"
# artist = "Queen"

# url, embed_code = get_youtube_url(song_title, artist)
# print(f"URL: {url}\n\nEmbedded code:\n{embed_code}")

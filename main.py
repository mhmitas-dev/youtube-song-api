from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from ytmusicapi import YTMusic
from typing import List, Dict

app = FastAPI(title="YouTube Song Search API - Simple Version")

# Initialize YouTube Music search
ytmusic = YTMusic()

@app.get("/search")
async def search_songs(
    q: str = Query(..., description="Song name or artist + song"),
    limit: int = Query(5, ge=1, le=10, description="Number of results")
):
    """
    Search songs on YouTube Music and return playable YouTube URLs.
    Example: /search?q=blinding lights the weeknd&limit=3
    """
    try:
        # Search only for songs
        results = ytmusic.search(q, filter="songs", limit=limit * 2)

        songs = []
        for item in results:
            if item.get('resultType') != 'song':
                continue

            video_id = item.get('videoId')
            if not video_id:
                continue

            song_data = {
                "title": item.get('title', 'Unknown Title'),
                "artist": item.get('artists')[0]['name'] if item.get('artists') else "Unknown Artist",
                "duration": item.get('duration', 'N/A'),
                "videoId": video_id,
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",      # Main link (most chatbots auto-play this)
            }
            songs.append(song_data)

            if len(songs) >= limit:
                break

        return songs

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Something went wrong. Please try again later."}
        )


@app.get("/top")
async def search_top_song(q: str = Query(..., description="Song name or artist + song")):
    """Returns only the best matching song - perfect for chatbots"""
    try:
        results = ytmusic.search(q, filter="songs", limit=5)
        
        for item in results:
            if item.get('resultType') == 'song' and item.get('videoId'):
                video_id = item['videoId']
                return {
                    "title": item.get('title', 'Unknown'),
                    "artist": item.get('artists')[0]['name'] if item.get('artists') else "Unknown",
                    "duration": item.get('duration', 'N/A'),
                    "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                }
        
        return {"error": "No song found"}
        
    except Exception:
        return {"error": "Something went wrong"}
        

@app.get("/")
async def root():
    return {
        "message": "YouTube Song Search API is running!",
        "how_to_use": "Go to /search?q=your song name"
    }
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from ytmusicapi import YTMusic

app = FastAPI(title="YouTube Song Search API")

# Using India as default - good balance for global availability
ytmusic = YTMusic(location="IN")

@app.get("/search")
async def search_songs(
    q: str = Query(..., description="Song name or artist + song"),
    limit: int = Query(5, ge=1, le=10)
):
    try:
        results = ytmusic.search(q, filter="songs", limit=limit * 2)
        songs = []

        for item in results:
            if item.get('resultType') != 'song' or not item.get('videoId'):
                continue

            song_data = {
                "title": item.get('title', 'Unknown Title'),
                "artist": item.get('artists')[0]['name'] if item.get('artists') else "Unknown Artist",
                "duration": item.get('duration', 'N/A'),
                "videoId": item.get('videoId'),
                "youtube_url": f"https://www.youtube.com/watch?v={item.get('videoId')}"
            }
            songs.append(song_data)

            if len(songs) >= limit:
                break

        return songs

    except Exception:
        return JSONResponse(status_code=500, content={"error": "Something went wrong"})


@app.get("/top")
async def search_top_song(q: str = Query(..., description="Song name or artist + song")):
    try:
        results = ytmusic.search(q, filter="songs", limit=8)

        for item in results:
            if item.get('resultType') == 'song' and item.get('videoId'):
                video_id = item['videoId']
                return {
                    "title": item.get('title', 'Unknown'),
                    "artist": item.get('artists')[0]['name'] if item.get('artists') else "Unknown Artist",
                    "duration": item.get('duration', 'N/A'),
                    "videoId": video_id,
                    "youtube_url": f"https://www.youtube.com/watch?v={video_id}"
                }
        
        return {"error": "No song found"}

    except Exception:
        return {"error": "Something went wrong"}


@app.get("/")
async def root():
    return {"message": "YouTube Song Search API running (using India region)"}
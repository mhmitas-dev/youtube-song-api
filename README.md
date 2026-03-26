### YouTube Song Search API

**Live URL:** https://yt-song-search.onrender.com

This API allows you to search for songs on YouTube and get clean, playable YouTube links.

#### Available Endpoints

1. **Search Multiple Songs**  
   **Endpoint:** `GET /search`

   **Parameters:**
   - `q` → Song name or artist + song (required)
   - `limit` → Number of results (optional, default = 5, max = 10)

   **Example Requests:**
   ```
   https://yt-song-search.onrender.com/search?q=APT ROSÉ
   https://yt-song-search.onrender.com/search?q=blinding lights the weeknd&limit=3
   ```

   **Response:** Array of songs (JSON)
   ```json
   [
     {
       "title": "APT.",
       "artist": "ROSÉ",
       "duration": "2:50",
       "videoId": "DiTd771WumE",
       "youtube_url": "https://www.youtube.com/watch?v=DiTd771WumE"
     },
     {
       "title": "Love Again",
       "artist": "Dua Lipa",
       "duration": "4:19",
       "videoId": "IkL-RjXJLv0",
       "youtube_url": "https://www.youtube.com/watch?v=IkL-RjXJLv0"
     }
   ]
   ```

2. **Search Top (Single Best) Song**  
   **Endpoint:** `GET /top`  
   *(Recommended for chatbots – returns only 1 result)*

   **Parameters:**
   - `q` → Song name or artist + song (required)

   **Example Request:**
   ```
   https://yt-song-search.onrender.com/top?q=APT ROSÉ
   https://yt-song-search.onrender.com/top?q=shape of you ed sheeran
   ```

   **Response:** Single song object (JSON)
   ```json
   {
     "title": "APT.",
     "artist": "ROSÉ",
     "duration": "2:50",
     "videoId": "DiTd771WumE",
     "youtube_url": "https://www.youtube.com/watch?v=DiTd771WumE"
   }
   ```

   If no song is found, it returns:
   ```json
   {"error": "No song found"}
   ```

#### How to Use in Your Chatbot
1. Send a request to `/search` or `/top` with the user's song query.
2. Take the `youtube_url` from the response.
3. Send that URL to the user → most chat apps (Telegram, WhatsApp, Discord, etc.) will automatically show a playable video preview with thumbnail and play button.

#### Root Page
Visit https://yt-song-search.onrender.com to check if the API is running.
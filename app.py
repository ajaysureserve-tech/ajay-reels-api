from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI()

# 1. Sabse pehle CORS handle karte hain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Sabhi websites se connection allow karega
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    # Jab aap link open karoge toh ye dikhega
    return {"message": "Backend is Ready!", "status": "Success"}

# --- Stream Route (Reels/Audio ke liye) ---
@app.get("/stream")
async def stream_audio(url: str):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
        # Ye seedha audio link par bhej dega
        return RedirectResponse(url=audio_url)
    except Exception as e:
        return {"error": str(e)}

# --- Download Route ---
@app.get("/download")
async def download_video(url: str):
    try:
        # Vercel par file save karne ke liye /tmp folder use karna padta hai
        output_path = "/tmp/video.mp4" 
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return FileResponse(output_path, media_type="video/mp4", filename="downloaded_video.mp4")
    except Exception as e:
        return {"error": str(e)}

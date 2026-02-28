from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI()

# CORS allow karna zaroori hai taaki Vercel se Render par request aaye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Backend is Ready!"}

# --- Naya Stream Route (Background Play ke liye) ---
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
        return RedirectResponse(url=audio_url)
    except Exception as e:
        return {"error": str(e)}

# --- Download Route ---
@app.get("/download")
async def download_video(url: str):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return FileResponse("video.mp4", media_type="video/mp4", filename="downloaded_video.mp4")
    except Exception as e:
        return {"error": str(e)}

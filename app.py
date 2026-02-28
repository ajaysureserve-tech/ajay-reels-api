from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

# 1. FastAPI App Initialize
app = FastAPI()

# 2. CORS Setting: Isse frontend se connection block nahi hoga
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Home Route: Check karne ke liye ki backend live hai
@app.get("/")
async def root():
    return {
        "message": "Backend is Ready!", 
        "status": "Success",
        "owner": "Ajay"
    }

# 4. Stream Route: Reels ya Audio ko background mein chalane ke liye
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
        # Ye seedha real streaming link par redirect kar dega
        return RedirectResponse(url=audio_url)
    except Exception as e:
        return {"error": str(e)}

# 5. Download Route: Video file download karne ke liye
@app.get("/download")
async def download_video(url: str):
    try:
        # Vercel par sirf /tmp folder mein hi file save ho sakti hai
        output_path = "/tmp/video.mp4" 
        
        # Purani file delete karna (agar exist karti ho)
        if os.path.exists(output_path):
            os.remove(output_path)
            
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'noplaylist': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return FileResponse(
            output_path, 
            media_type="video/mp4", 
            filename="ajay_reels_video.mp4"
        )
    except Exception as e:
        return {"error": str(e)}

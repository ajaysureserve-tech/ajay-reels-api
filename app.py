from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "YouTube Backend Ready!"}

# --- Naya Route: Video ki saari Qualities nikaalne ke liye ---
@app.get("/info")
async def get_video_info(url: str):
    try:
        ydl_opts = {'quiet': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Sirf kaam ki info bhej rahe hain
            formats = []
            for f in info.get('formats', []):
                # Sirf wo format le rahe hain jisme video+audio dono ho ya sirf video
                if f.get('height'):
                    formats.append({
                        'format_id': f['format_id'],
                        'resolution': f'{f["height"]}p',
                        'ext': f['ext'],
                        'url': f['url']
                    })
            return {"title": info.get('title'), "formats": formats}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download")
async def download_video(url: str):
    try:
        output_path = "/tmp/video.mp4"
        if os.path.exists(output_path): os.remove(output_path)
        ydl_opts = {'format': 'best', 'outtmpl': output_path}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return FileResponse(output_path, filename="video.mp4")
    except Exception as e:
        return {"error": str(e)}

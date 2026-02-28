@app.get("/stream")
async def stream_audio(url: str):
    # yt-dlp ka use karke sirf audio link nikaal kar redirect karein
    ydl_opts = {'format': 'bestaudio/best', 'noplaylist': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
    return RedirectResponse(url=audio_url)

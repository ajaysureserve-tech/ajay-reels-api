from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['GET'])
def download_video():
video_url = request.args.get('url')
if not video_url:
return jsonify({"error": "URL is required"}), 400

try:
# Ye settings Instagram, YouTube aur Facebook sabke liye kaam karegi
ydl_opts = {
'format': 'best',
'quiet': True,
'no_warnings': True,
'check_formats': True,
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
info = ydl.extract_info(video_url, download=False)
download_url = info.get('url')

# Agar multiple formats mil rahe hain toh best wala chunne ke liye
if not download_url and 'formats' in info:
download_url = info['formats'][-1]['url']

return jsonify({
"status": "success",
"platform": info.get('extractor_key'),
"title": info.get('title'),
"download_url": download_url
})
except Exception as e:
return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)


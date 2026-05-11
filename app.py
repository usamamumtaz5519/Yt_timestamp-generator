from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask(__name__)

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    chapters = ""
    if request.method == 'POST':
        url = request.form.get('url')
        video_id = get_video_id(url)
        if video_id:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                for entry in transcript:
                    if int(entry['start']) % 60 == 0:
                        minutes = int(entry['start'] // 60)
                        seconds = int(entry['start'] % 60)
                        chapters += f"{minutes:02d}:{seconds:02d} - {entry['text'][:40]}...\n"
                if not chapters:
                    chapters = "No exact minute marks found, but transcript is available!"
            except Exception as e:
                chapters = "Error: Is video ke liye transcript band hai ya link galat hai."
    
    return f'''
    <html>
        <head><title>YT Timestamp Generator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>body{{font-family:sans-serif; text-align:center; padding:20px; background:#f4f4f4;}} 
        input{{width:80%; padding:10px; margin:10px; border-radius:5px; border:1px solid #ccc;}}
        button{{padding:10px 20px; background:#ff0000; color:white; border:none; border-radius:5px; cursor:pointer;}}
        pre{{text-align:left; background:white; padding:15px; border-radius:5px; max-width:500px; margin:20px auto; white-space:pre-wrap;}}</style>
        </head>
        <body>
            <h1>🚀 YouTube Timestamp Maker</h1>
            <p>Paste link and get chapters instantly!</p>
            <form method="post">
                <input type="text" name="url" placeholder="https://www.youtube.com/watch?v=..." required>
                <br><button type="submit">Generate Timestamps</button>
            </form>
            {f"<h3>Your Timestamps:</h3><pre>{chapters}</pre>" if chapters else ""}
        </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

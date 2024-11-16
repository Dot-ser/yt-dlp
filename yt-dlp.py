from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_song(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    output_directory = 'downloads'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    download_song(url, output_directory)
    
    # Find the downloaded file
    for file_name in os.listdir(output_directory):
        if file_name.endswith('.mp3'):
            return send_file(os.path.join(output_directory, file_name), as_attachment=True)
    
    return 'Download failed', 500

if __name__ == "__main__":
    app.run(debug=True)

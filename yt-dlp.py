from flask import Flask, request, send_from_directory, escape
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    songs = os.listdir('static/songs')
    song_list = ''.join(f'<li><a href="/download/{escape(song)}">{escape(song)}</a></li>' for song in songs)
    return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Song Download</title>
        </head>
        <body>
            <h1>Download Songs</h1>
            <form action="/download" method="post">
                <input type="text" name="url" placeholder="Enter YouTube URL">
                <button type="submit">Download</button>
            </form>
            <ul>
                {song_list}
            </ul>
        </body>
        </html>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'static/songs/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'Download complete!'

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('static/songs', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

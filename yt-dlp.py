from flask import Flask, request, jsonify
import yt_dlp
import os
import random
import time

app = Flask(__name__)

def get_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        # Add more user agents as needed
    ]
    return random.choice(user_agents)

@app.route('/download_song', methods=['GET'])
def download_song():
    song_name = request.args.get('name')
    if not song_name:
        return jsonify({'error': 'Name parameter is missing'}), 400

    try:
        # Define the download directory
        download_dir = 'downloads'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Set a random IP address and user agent in the headers
        random_ip = get_random_ip()
        random_user_agent = get_random_user_agent()
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'http_headers': {
                'X-Forwarded-For': random_ip,
                'User-Agent': random_user_agent,
            },
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_result = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            audio_file = ydl.prepare_filename(search_result['entries'][0]).replace('.webm', '.mp3')

        # Introduce a random delay to mimic natural usage
        time.sleep(random.uniform(1, 5))

        return jsonify({'audio_file': audio_file, 'ip_used': random_ip, 'user_agent': random_user_agent}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    

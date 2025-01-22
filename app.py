import os
import base64
from flask import Flask, request, jsonify
import yt_dlp
from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv(dotenv_path='.env.local')

app = Flask(__name__)

def fetch_combined_stream(formats):
    """Extract the combined audio+video URL."""
    return next((f['url'] for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none'), None)

def create_cookies_file():
    """Create cookies file from base64 encoded cookies in the environment variable."""
    cookies_base64 = os.getenv("YOUTUBE_COOKIES_BASE64")
    if cookies_base64:
        # Decode the base64 encoded cookies
        cookies_data = base64.b64decode(cookies_base64).decode('utf-8')
        cookies_dir = './temp'
        
        if not os.path.exists(cookies_dir):
            os.makedirs(cookies_dir)
        
        # Write the decoded cookies to the cookies.txt file
        with open(os.path.join(cookies_dir, 'cookies.txt'), 'w') as f:
            f.write(cookies_data)
        print("Cookies file created successfully.")
    else:
        print("No YOUTUBE_COOKIES_BASE64 environment variable found.")

# Create cookies file if it doesn't exist when the app starts
cookies_path = './temp/cookies.txt'
if not os.path.exists(cookies_path):
    create_cookies_file()

@app.route('/api/info', methods=['GET'])
def get_video_info():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Invalid YouTube ID"}), 400

    ydl_opts = {
        'cookies': cookies_path,  # Use only the provided cookies file
        'quiet': True,  # Suppress additional output
        'noplaylist': True,  # Don't download playlists, only the single video
        'no_check_certificate': True,  # Disable SSL certificate checks to avoid issues
        'force_generic_extractor': True,  # Use a generic extractor in case YouTube is not detected correctly
        'username': None,  # Ensure no username is passed (prevents other authentication)
        'password': None,  # Ensure no password is passed
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            title = info_dict.get('title')
            formats = info_dict.get('formats', [])
           
            combined_stream = fetch_combined_stream(formats)

            response = {
                "video_id": video_id,
                "title": title,
                "video_stream_url": combined_stream,
            }
            return jsonify(response)

    except yt_dlp.utils.DownloadError as e:
        if "Video unavailable" in str(e):
            return jsonify({"error": "Video unavailable"}), 404
        return jsonify({"error": f"Error processing video: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import yt_dlp


from flask_cors import CORS  # Import CORS


# Enable CORS for all routes


app = Flask(__name__)
CORS(app, origins="http://localhost:3000") 


# def fetch_best_audio(formats):
#     """Extract the best audio-only URL."""
#     return next((f['url'] for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), None)

def fetch_combined_stream(formats):
    """Extract the combined audio+video URL."""
    return next((f['url'] for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none'), None)

@app.route('/api/info', methods=['GET'])
def get_video_info():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Invalid YouTube ID"}), 400

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            title = info_dict.get('title')
            formats = info_dict.get('formats', [])

            # Run audio and combined URL fetching in parallel
           
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
from flask import Flask, request, jsonify
from flask_cors import CORS
from pytubefix import YouTube

app = Flask(__name__)
cors = CORS(app)

def fetch_combined_stream(yt):
    """Extract the highest resolution stream with both audio and video."""
    stream = yt.streams.filter(progressive=True).order_by("resolution").desc().first()
    return stream.url if stream else None

@app.route('/')
def app_status():
    """Default route to show the app's status."""
    return jsonify({"status": "App is up and running!"})

@app.route('/api/info', methods=['GET'])
def get_video_info():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Invalid YouTube ID"}), 400
    
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        title = yt.title
        combined_stream = fetch_combined_stream(yt)

        response = {
            "video_id": video_id,
            "title": title,
            "video_stream_url": combined_stream,
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False)

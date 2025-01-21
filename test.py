import yt_dlp

def fetch_combined_stream(formats):
    """Extract the combined audio+video URL."""
    return next((f['url'] for f in formats if f.get('vcodec') != 'none' and f.get('acodec') != 'none'), None)

def get_video_info(video_id):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'format': 'bestvideo+bestaudio',  # Extract best video + audio stream
        'geo_bypass': True,  # To bypass geographical restrictions
        'force_generic_extractor': True,  # Force generic extraction (useful for sites like YouTube)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            title = info_dict.get('title')
            formats = info_dict.get('formats', [])
            combined_stream = fetch_combined_stream(formats)

            return {
                "video_id": video_id,
                "title": title,
                "video_stream_url": combined_stream,
            }
    except yt_dlp.utils.DownloadError as e:
        return {"error": f"Error processing video: {str(e)}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

# Example usage
video_id = "dQw4w9WgXcQ"  # Replace with actual video ID
result = get_video_info(video_id)
print(result)

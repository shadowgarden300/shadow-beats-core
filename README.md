# Shadow Beats Core

Shadow Beats Core is a prerequisite service for the [Shadow Beats](https://github.com/shadowgarden300/shadow-beats-web) Web application. It is responsible for fetching streaming URLs using [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Prerequisites

- Python 3.13 or later
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Installation and Setup

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd shadow-beats-core
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python app.py
   ```

## API Endpoints

### Health Check
- **Endpoint:** `/`
- **Method:** `GET`
- **Description:** Returns a simple response to verify that the service is running.

### Get Streaming URL
- **Endpoint:** `/api/info`
- **Method:** `GET`
- **Query Parameter:** `id=YOUTUBE_VIDEO_ID`
- **Description:** Fetches the streaming URL for a given YouTube video ID.

## License

This project is open-source and available under the applicable license.

---

For any issues or contributions, feel free to submit a pull request or create an issue in the repository.


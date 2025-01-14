---

# TikTok Downloader Web App

A web application built with Flask that allows users to download TikTok videos or playlists by providing a URL. The app processes the URL, downloads the requested content, and provides the file for download. It also includes robust cleanup mechanisms to manage temporary files.

---

## Features
- Download **single TikTok videos** or **entire playlists** by providing the URL.
- Automatically compresses playlists into ZIP files for easy download.
- User-friendly web interface with real-time feedback during processing.
- Robust cleanup of temporary files:
  - **Immediate cleanup** when the user leaves the page without downloading.
  - **Periodic cleanup** of stale files after a defined time.

---

---

## Usage

1. Enter the TikTok video or playlist URL in the text input field.
2. Click the **Download** button to start processing.
3. Wait for the success page to appear.
4. Click **Download Now** to download the video or playlist (ZIP).


![webapp-gif](https://github.com/user-attachments/assets/4a780a89-35b7-4197-b7c2-24a822fd81c0)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/tiktok-downloader.git
   cd tiktok-downloader
   ```

2. Install dependencies using **Poetry**:
   ```bash
   poetry install
   ```

   Or, if using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app locally:
   ```bash
   poetry run waitress-serve --port=8000 index:app
   ```

   Or with `python` (development mode):
   ```bash
   python index.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

---

## Deployment

To deploy the app to production:

1. **Render**:
   - Add your project to Render from GitHub.
   - Use the following start command:
     ```bash
     gunicorn index:app
     ```
   - Push all changes to the `pyproject.toml`, and `index.py`.

2. **Alternative Hosting**:
   - Follow similar steps for platforms like Railway, Deta, or Fly.io.

---

## Project Structure

```
tiktok-downloader/
│
├── static/                 # Static files (CSS)
│   └── styles.css          # Styling for the web interface
│
├── templates/              # HTML templates for the app
│   ├── index.html          # Main page for input
│   └── success.html        # Success page after processing
│
├── app.py                  # Core TikTok download logic
├── index.py                # Web server and route handling
├── pyproject.toml          # Poetry dependency configuration
├── requirements.txt        # Dependencies (for non-Poetry users)
├── poetry.lock             # Lock file for dependencies
└── README.md               # Project documentation (this file)
```

---

## Environment Variables

To securely configure the app (e.g., in production), use environment variables. Create a `.env` file or configure your host environment with:

- `SECRET_KEY`: Flask secret key for session management.

---

## Known Issues

- **Gunicorn on Windows**: Use **Waitress** locally instead of Gunicorn, as Gunicorn doesn’t support Windows.
- **Large Files**: Depending on hosting and Flask configurations, large playlists may exceed upload/download limits.

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/).
- Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).

---

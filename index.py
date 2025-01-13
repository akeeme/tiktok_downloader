from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
import os
import uuid
import shutil
import tempfile
import zipfile
import time
import threading
from dotenv import load_dotenv
from app import download_tiktok_video, download_tiktok_playlist, is_playlist
# Load environment variables from .env file
load_dotenv()





app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Dictionary to track file paths and timestamps: { file_id: { "path": "/path/to/file", "timestamp": 1671234567 } }
DOWNLOADS = {}

# Cleanup configuration
CLEANUP_INTERVAL = 60  # Check for stale files every 60 seconds
FILE_EXPIRATION_TIME = 600  # expire files after 10 minutes (600 seconds)


### Periodic Cleanup Task ###
def cleanup_stale_files():
    """
    Periodically checks the DOWNLOADS dictionary for stale files and removes them.
    """
    while True:
        current_time = time.time()
        stale_files = []

        # Find files older than FILE_EXPIRATION_TIME
        for file_id, data in list(DOWNLOADS.items()):
            if current_time - data["timestamp"] > FILE_EXPIRATION_TIME:
                stale_files.append((file_id, data["path"]))

        # Remove stale files and their parent directories
        for file_id, path in stale_files:
            temp_dir = os.path.dirname(path)
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
                print(f"Stale file cleaned up: {path}")
            DOWNLOADS.pop(file_id, None)

        # Sleep until the next cleanup cycle
        time.sleep(CLEANUP_INTERVAL)


# Start the cleanup task in a background thread
threading.Thread(target=cleanup_stale_files, daemon=True).start()


@app.route("/", methods=["GET"])
def index():
    """
    Renders the main page with the URL input.
    """
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process_download():
    """
    Processes the TikTok download request:
      - Downloads the video(s) to a temp folder,
      - If it's a playlist, zips the files,
      - Returns a JSON response with file_id or an error message.
    """
    try:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "No URL provided"}), 400

        url = data["url"]
        temp_folder = tempfile.mkdtemp(prefix="tiktok_")

        if is_playlist(url):
            # Handle playlist
            playlist_title = download_tiktok_playlist(url, output_dir=temp_folder)

            # Zip the playlist
            zip_filename = os.path.join(temp_folder, f"{playlist_title}.zip")
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_folder):
                    for f in files:
                        if f == f"{playlist_title}.zip":
                            continue
                        full_path = os.path.join(root, f)
                        arcname = os.path.relpath(full_path, temp_folder)
                        zf.write(full_path, arcname)
            final_file = zip_filename
        else:
            # Handle single video
            download_tiktok_video(url, output=temp_folder)
            files_in_temp = os.listdir(temp_folder)
            if not files_in_temp:
                shutil.rmtree(temp_folder, ignore_errors=True)
                return jsonify({"error": "No file was downloaded"}), 500
            final_file = os.path.join(temp_folder, files_in_temp[0])

        # Generate unique ID and store file path + timestamp
        unique_id = str(uuid.uuid4())
        DOWNLOADS[unique_id] = {"path": final_file, "timestamp": time.time()}

        return jsonify({"file_id": unique_id, "error": None}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/success/<file_id>", methods=["GET"])
def success_page(file_id):
    """
    Renders the success page with a "Download Now" link.
    """
    if file_id not in DOWNLOADS:
        return "File not found or already removed.", 404
    return render_template("success.html", file_id=file_id)


@app.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    """
    Sends the file to the user and removes it from the server afterward.
    """
    if file_id not in DOWNLOADS:
        return "File not found or already removed.", 404

    final_file = DOWNLOADS[file_id]["path"]
    temp_dir = os.path.dirname(final_file)

    # Remove from dictionary so the file can't be re-downloaded
    DOWNLOADS.pop(file_id, None)

    def cleanup_file(response):
        """
        Deletes the temp folder after sending the file.
        """
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"Cleaned up: {temp_dir}")
        return response

    return cleanup_file(send_file(final_file, as_attachment=True))


@app.route("/cleanup/<file_id>", methods=["POST"])
def cleanup_immediate(file_id):
    """
    Cleans up the file and folder if the user leaves the page without downloading.
    """
    time.sleep(300) # Wait for 5 minutes before cleaning up
    if file_id not in DOWNLOADS:
        return jsonify({"error": "File not found or already removed."}), 404

    final_file = DOWNLOADS[file_id]["path"]
    temp_dir = os.path.dirname(final_file)

    # Remove file and its folder
    DOWNLOADS.pop(file_id, None)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"Immediate cleanup: {temp_dir}")

    return jsonify({"message": "File cleaned up immediately."}), 200


if __name__ == "__main__":
    app.run()

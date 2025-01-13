from flask import Flask, request, send_file, render_template, g
from app import download_tiktok_video, download_tiktok_playlist, is_playlist
import os
import shutil
import tempfile
import zipfile

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.before_request
def create_temp_folder():
    """
    Before each request, if it's a POST, create a unique temp folder and store
    it in the request context 'g' so we can access it in the route.
    """
    if request.method == "POST":
        g.temp_folder = tempfile.mkdtemp(prefix="tiktok_")
        print(f"Created temp folder: {g.temp_folder}")

@app.after_request
def remove_temp_folder(response):
    """
    After the request finishes, remove the temp folder we created if it exists.
    This ensures cleanup even if an error occurred or send_file was used.
    """
    temp_folder = getattr(g, "temp_folder", None)
    if temp_folder and os.path.exists(temp_folder):
        try:
            shutil.rmtree(temp_folder, ignore_errors=True)
            print(f"Cleanup successful: Removed temporary folder {temp_folder}")
        except Exception as e:
            print(f"Cleanup failed for {temp_folder}: {e}")
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "No URL provided.", 400

        # Retrieve the per-request folder from g
        temp_folder = g.temp_folder

        if is_playlist(url):
            # Download entire playlist into temp_folder
            playlist_title = download_tiktok_playlist(url, output_dir=temp_folder)

            # Zip up the playlist
            zip_filename = os.path.join(temp_folder, f"{playlist_title}.zip")
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_folder):
                    for f in files:
                        # Skip the zip itself
                        if f == f"{playlist_title}.zip":
                            continue
                        full_path = os.path.join(root, f)
                        arcname = os.path.relpath(full_path, temp_folder)
                        zf.write(full_path, arcname)

            return send_file(zip_filename, as_attachment=True)

        else:
            # Single video logic
            download_tiktok_video(url, output=temp_folder)

            # Grab the first file in temp_folder
            files_in_temp = os.listdir(temp_folder)
            if not files_in_temp:
                return "No file was downloaded.", 500

            video_filename = os.path.join(temp_folder, files_in_temp[0])
            return send_file(video_filename, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

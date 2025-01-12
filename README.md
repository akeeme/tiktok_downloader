---

# TikTok Downloader

A Python script to download TikTok videos or playlists using **yt_dlp**, with dependency management handled via **Poetry**.

## Features
- **Single Video Download**: Downloads a single TikTok video and ensures unique filenames.
- **Playlist Download**: Downloads all videos in a playlist or user profile, saving them in organized folders.
- **Custom Output Paths**: Specify where to save downloaded files.
- **Dependency Management**: Uses Poetry for clean dependency management and virtual environments.

## Requirements
- **Python 3.9+**
- **Poetry**: [Installation Guide](https://python-poetry.org/docs/#installation)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Poetry**:
   ```bash
   pip install poetry
   ```

3. **Install Dependencies**:
   ```bash
   poetry install
   ```

## Usage

1. **Run the Script**:
   Use `poetry run` to execute the script within the Poetry-managed environment.
   ```bash
   poetry run python script.py -url <TIKTOK_URL> [-output_dir /path/to/save]
   ```

2. **Arguments**:
   - `-url`: (Required) The TikTok URL to download. Can be a single video or a playlist.
   - `-output_dir`: (Optional) The directory to save the downloaded files. Defaults to `./output`.

### Examples

- **Download a Single Video**:
  ```bash
  poetry run python script.py -url https://www.tiktok.com/@username/video/1234567890
  ```

- **Download a Playlist**:
  ```bash
  poetry run python script.py -url https://www.tiktok.com/@username -output_dir /path/to/save
  ```

## Development

1. **Add Dependencies**:
   To add new dependencies, use:
   ```bash
   poetry add <package-name>
   ```

2. **Run in Virtual Environment**:
   Activate the Poetry-managed virtual environment:
   ```bash
   poetry shell
   ```

3. **Update Dependencies**:
   If you modify `pyproject.toml`, update dependencies:
   ```bash
   poetry update
   ```

## Code Overview

### Main Functions:
1. **`download_tiktok_video(url, output)`**  
   - Downloads a single video to the specified output path.
   - Avoids overwriting by appending a counter to filenames.

2. **`download_tiktok_playlist(url, output_dir)`**  
   - Downloads all videos from a playlist or user profile.
   - Saves videos in an organized folder structure (`output/<playlist_name>/`).

3. **`is_playlist(url)`**  
   - Determines whether the URL points to a single video or a playlist.

4. **`main()`**  
   - Parses command-line arguments using `argparse` and dispatches the download logic.

## Project Structure

```plaintext
.
├── script.py              # Main script file
├── pyproject.toml         # Poetry configuration
├── README.md              # Project documentation
├── output/                # Default output directory (created automatically)
└── poetry.lock            # Poetry lock file for dependencies
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to modify this as needed!

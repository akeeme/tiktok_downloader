import yt_dlp
import os
import argparse
# import shutil



def download_tiktok_video(url: str, output: str = None):
    """
    Download a single TikTok video from the given URL.

    If the 'output' path is not specified, the video is saved
    as 'output/tiktok_vid.mp4'. If a file with that name
    already exists, a counter is appended to create a unique filename.

    Args:
        url (str): The TikTok video URL.
        output (str, optional): The output file path. Defaults to None.
    """
    
    # Default output if none provided
    uniq_id = url.split("/")[-1]
    output = f"output/tiktok_{uniq_id}.mp4" if not output else f'{output}/tiktok_{uniq_id}.mp4'

    base, ext = os.path.splitext(output)
    counter = 1

    # Ensure a unique filename by appending an increasing counter
    while os.path.exists(output):
        output = f"{base}{counter}{ext}"
        counter += 1

    ydl_opts = {
        'outtmpl': output,
        'format': 'mp4/bestaudio/best',
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/108.0.0.0 Safari/537.36'
            )
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_tiktok_playlist(url: str, output_dir: str = None):
    """
    Download all videos from a TikTok playlist or user page URL.

    If 'output_dir' is not specified, the videos are saved
    under the 'output' directory, using the playlist title
    and sequential filenames.

    Args:
        url (str): The TikTok playlist URL.
        output_dir (str, optional): The directory to store downloaded files. 
            Defaults to None.
    """
    
    output_dir = "output" if not output_dir else output_dir

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(playlist_title)s', 'video%(playlist_index)s.%(ext)s'),
        'ignoreerrors': True,
        'format': 'mp4/bestaudio/best',
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/108.0.0.0 Safari/537.36'
            )
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    playlist_title = info.get('title', 'UnintitledPlaylist')
    print(f"\n\n\nDownloading the TikTok playlist: {playlist_title}\n\n\n")

    playlist_folder = os.path.join(output_dir, playlist_title)

    if not os.path.exists(playlist_folder):
        print("No videos were downloaded or playlist folder not found.")
        return

    print(f"Downloaded the TikTok playlist to {playlist_folder}")
    
    return playlist_title

    # (Optional) Code to compress the folder into a zip archive:
    # zip_filename = f"{playlist_title}.zip"
    # shutil.make_archive(playlist_folder, 'zip', playlist_folder)
    # shutil.move(f"{playlist_folder}.zip", os.path.join(output_dir, zip_filename))
    # print(f"Downloaded the TikTok playlist to {zip_filename}")
    # shutil.rmtree(output_dir)


def is_playlist(url: str) -> bool:
    """
    Determine if the given URL points to a playlist (or user page) 
    rather than a single video.

    Simple heuristic: If 'video' is in the URL, it's treated as a single video.

    Args:
        url (str): The TikTok URL.

    Returns:
        bool: True if it's a playlist/user page, False if it's a single video.
    """
    
    return "video" not in url


def download_tiktok(url: str):
    """
    High-level function that detects if the URL is for a single video or a playlist,
    then downloads accordingly.

    Args:
        url (str): The TikTok URL (video or playlist).
    """
    
    if is_playlist(url):
        download_tiktok_playlist(url)
    else:
        download_tiktok_video(url)


def main(*args):
    """
    Entry point when running the script from the command line.
    Parses command-line arguments for URL and output directory, then
    downloads the corresponding TikTok content.
    """
    
    parser = argparse.ArgumentParser(description="Download TikTok videos or playlists.")
    parser.add_argument("-url", required=True, type=str, help="The TikTok URL to download.")
    parser.add_argument("-output_dir", type=str, default=None, help="The output directory to save the downloaded files.")
    args = parser.parse_args()

    url = args.url
    output_dir = args.output_dir

    print(f"Downloading TikTok video/playlist from {url}")

    if is_playlist(url):
        download_tiktok_playlist(url, output_dir)
    else:
        download_tiktok_video(url, output_dir)


if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

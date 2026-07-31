import os
from yt_dlp import YoutubeDL


def download_youtube_video(url):
    """
    Downloads a YouTube video and returns the local file path.
    """

    output_dir = "downloads"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        "format": "mp4/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    return filename
import yt_dlp
import os

DOWNLOAD_DIR = "YT-VideoDownloader/Downloads"

def ensure_download_folder():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)


def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A').strip()
        print(f"\rDownloading: {percent} | Speed: {speed}", end="")
    elif d['status'] == 'finished':
        print("\nDownload complete. Processing...")


def list_formats(url):
    print("\nFetching available qualities...\n")

    ydl_opts = {'quiet': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])

        seen = set()

        for f in formats:
            # filter only useful formats
            if f.get('height') and f.get('ext') == 'mp4':
                key = (f['format_id'], f.get('height'))
                if key not in seen:
                    seen.add(key)
                    print(f"ID: {f['format_id']} | {f.get('height')}p | {f.get('ext')}")


def download(url, mode, format_id=None):
    ensure_download_folder()

    base_opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/%(playlist_title)s/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'ignoreerrors': True,
        'noplaylist': False,
    }

    if mode == "1":  # Full video (manual quality)
        ydl_opts = {
            **base_opts,
            'format': f"{format_id}+bestaudio/best"
        }

    elif mode == "2":  # Best auto
        ydl_opts = {
            **base_opts,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }

    elif mode == "3":  # Audio only
        ydl_opts = {
            **base_opts,
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

    elif mode == "4":  # Thumbnail
        ydl_opts = {
            **base_opts,
            'skip_download': True,
            'writethumbnail': True
        }

    else:
        print("Invalid option.")
        return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    print("=== YouTube Downloader ===\n")

    url = input("Enter YouTube video/playlist URL: ").strip()

    print("\nOptions:")
    print("1. Select Video Quality manually")
    print("2. Best Quality (auto merge)")
    print("3. Audio Only (MP3)")
    print("4. Thumbnail Only")

    mode = input("Choose option (1/2/3/4): ").strip()

    format_id = None

    if mode == "1":
        list_formats(url)
        format_id = input("\nEnter format ID: ").strip()

    download(url, mode, format_id)


if __name__ == "__main__":
    main()
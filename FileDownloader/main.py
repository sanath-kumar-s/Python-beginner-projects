import os
import requests
from urllib.parse import urlparse
from tqdm import tqdm

def get_filename(url, response):
    if "content-disposition" in response.headers:
        content_disp = response.headers["content-disposition"]
        if "filename=" in content_disp:
            return content_disp.split("filename=")[-1].strip('"')

    path = urlparse(url).path
    filename = os.path.basename(path)

    if not filename:
        filename = "downloaded_file"

    return filename

def download_file(url):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        filename = get_filename(url, response)

        os.makedirs("FileDownloader/Downloads", exist_ok=True)
        filepath = os.path.join("FileDownloader/Downloads", filename)

        with open(filepath, "wb") as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:

            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))

        print(f"\n[✔] Downloaded successfully: {filepath}")

    except requests.exceptions.RequestException as e:
        print("[✖] Download failed:", e)


if __name__ == "__main__":
    print("=== File Downloader with Progress ===")
    url = input("Enter file URL: ").strip()

    if not url:
        print("No URL provided.")
    else:
        download_file(url)
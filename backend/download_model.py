"""
Download trained model from Google Drive
Run this once before using the ML pipeline
"""
import os
import requests
import sys
from pathlib import Path


def download_file_from_google_drive(file_id, destination):
    """Download file from Google Drive using file ID"""
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    CHUNK_SIZE = 32768
    total_size = int(response.headers.get('content-length', 0))

    if total_size == 0:
        print("⚠️  Warning: Could not determine file size")

    downloaded = 0
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    bar_length = 40
                    fill = int(bar_length * downloaded / total_size)
                    bar = '█' * fill + '-' * (bar_length - fill)
                    print(
                        f'\r📥 Download: |{bar}| {percent:.1f}%', end='', flush=True)
    print("\n✅ Download selesai!")


def main():
    """Main download function"""
    GOOGLE_DRIVE_FILE_ID = "1XbGwhvyehkmRSVR19ThwJzwRkH7fB-5c"

    # Path untuk simpan model
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_DIR.mkdir(exist_ok=True)

    model_path = DATA_DIR / "sapa_model.pkl"

    # Cek apakah model sudah ada
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024 * 1024)
        print(f"✅ Model sudah ada: {model_path} ({size_mb:.1f} MB)")
        return True

    print(f"📥 Download model dari Google Drive...")
    print(f"📍 Tujuan: {model_path}")

    if GOOGLE_DRIVE_FILE_ID == "YOUR_FILE_ID_HERE":
        print("\n❌ ERROR: Anda belum set Google Drive File ID!")
        print("\nCara mendapatkan File ID:")
        print("1. Buka file di Google Drive")
        print("2. Share → Copy link")
        print("3. Link format: https://drive.google.com/file/d/FILE_ID/view?usp=drive_link")
        print("4. Ganti YOUR_FILE_ID_HERE dengan FILE_ID")
        return False

    try:
        download_file_from_google_drive(GOOGLE_DRIVE_FILE_ID, model_path)
        print(f"\n✅ Model berhasil didownload ke: {model_path}")
        return True
    except Exception as e:
        print(f"\n❌ Error saat download: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

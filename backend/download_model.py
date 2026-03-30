"""
Download trained model & knowledge base from Google Drive
Run this once before using the SAPA ML prediction pipeline

Files downloaded:
  - sapa_model.pkl (trained diagnosis model ~800 MB)
  - knowledge_base.pkl (medical knowledge base)
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
    # Google Drive File IDs
    GOOGLE_DRIVE_MODEL_FILE_ID = "1XbGwhvyehkmRSVR19ThwJzwRkH7fB-5c"  # sapa_model.pkl
    # knowledge_base.pkl
    GOOGLE_DRIVE_KB_FILE_ID = "1BPrrVR4I3CkdWWkMHzPSkDYQ4Gw9hQfu"

    # Path untuk simpan model
    DATA_DIR = Path(__file__).parent.parent / "data"
    DATA_DIR.mkdir(exist_ok=True)

    model_path = DATA_DIR / "sapa_model.pkl"
    kb_path = DATA_DIR / "knowledge_base.pkl"

    # Cek file mana yang sudah ada
    model_exists = model_path.exists()
    kb_exists = kb_path.exists()

    if model_exists and kb_exists:
        model_size = model_path.stat().st_size / (1024 * 1024)
        kb_size = kb_path.stat().st_size / (1024 * 1024)
        print(f"✅ Semua file sudah ada!")
        print(f"   • sapa_model.pkl: {model_size:.1f} MB")
        print(f"   • knowledge_base.pkl: {kb_size:.1f} MB")
        return True

    try:
        # Download sapa_model.pkl
        if not model_exists:
            print(f"📥 Download sapa_model.pkl dari Google Drive...")
            download_file_from_google_drive(
                GOOGLE_DRIVE_MODEL_FILE_ID, model_path)
            print(f"✅ Model berhasil didownload!\n")
        else:
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"✅ sapa_model.pkl sudah ada ({size_mb:.1f} MB)\n")

        # Download knowledge_base.pkl (jika FILE_ID sudah di-set)
        if GOOGLE_DRIVE_KB_FILE_ID != "YOUR_KB_FILE_ID_HERE":
            if not kb_exists:
                print(f"📥 Download knowledge_base.pkl dari Google Drive...")
                download_file_from_google_drive(
                    GOOGLE_DRIVE_KB_FILE_ID, kb_path)
                print(f"✅ Knowledge Base berhasil didownload!\n")
            else:
                size_mb = kb_path.stat().st_size / (1024 * 1024)
                print(f"✅ knowledge_base.pkl sudah ada ({size_mb:.1f} MB)\n")
        else:
            print("⚠️  Catatan: FILE_ID untuk knowledge_base.pkl belum di-set")
            print(
                "   Jika knowledge_base.pkl belum ada, owner perlu upload ke Google Drive\n")

        print("✅ Setup complete! Teman bisa jalankan: python main.py")
        return True
    except Exception as e:
        print(f"\n❌ Error saat download: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

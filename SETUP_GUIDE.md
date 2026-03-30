# 📥 Setup Guide - Download Model dari Google Drive

## **Untuk Anda (Owner Model)**

### Step 1: Upload Model ke Google Drive
1. Buka [Google Drive](https://drive.google.com)
2. Klik tombol `+ New` → **Folder**
3. Beri nama: `SAPA-AI-Models`
4. Upload file `data/sapa_model.pkl` ke folder tersebut (sama seperti yang ada di PC kamu)
5. Klik kanan file → **Share**
6. Ubah permission menjadi **Anyone with the link** → **Viewer** (View only)
7. Copy link yang di-share (format: `https://drive.google.com/file/d/FILE_ID/view?usp=drive_link`)
8. Ambil bagian `FILE_ID` dari URL (string panjang di tengah URL)

### Step 2: Update Script dengan File ID Anda
1. Buka file `backend/download_model.py` di VS Code
2. Cari baris: `GOOGLE_DRIVE_FILE_ID = "YOUR_FILE_ID_HERE"` (kira-kira line 21)
3. Ganti `YOUR_FILE_ID_HERE` dengan FILE_ID dari Google Drive Anda
4. Simpan file (Ctrl+S)

**Contoh perubahan:**
```python
# Sebelum
GOOGLE_DRIVE_FILE_ID = "YOUR_FILE_ID_HERE"

# Sesudah
GOOGLE_DRIVE_FILE_ID = "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7"
```

### Step 3: Push ke GitHub
Sebelum push, pastikan sudah:
1. Update `GOOGLE_DRIVE_FILE_ID` di `backend/download_model.py` dengan FILE_ID Anda

Kemudian jalankan:
```bash
git add backend/download_model.py backend/requirements.txt SETUP_GUIDE.md
git commit -m "Add model download script from Google Drive"
git push
```

✅ **Sekarang teman kamu bisa clone dan setup! Lihat instruksi di bawah.**

---

## **Untuk Teman Anda** (Cara Jalanin Step-by-Step)

### Step 1: Clone Repository
Buka Terminal/PowerShell dan jalankan:
```bash
git clone https://github.com/YOUR_USERNAME/AI-SAPA.git
cd "AI - SAPA"
```
(Ganti `YOUR_USERNAME` dengan username GitHub kamu)

### Step 2: Setup Virtual Environment
**Di Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Di Linux/Mac (Bash):**
```bash
python3 -m venv venv
source venv/bin/activate
```

Kamu akan lihat `(venv)` di awal terminal kalau sudah aktif. ✅

### Step 3: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

Ini akan install semua library yang dibutuhkan (torch, transformers, fastapi, dll)

### Step 4: Download Model ke Folder `data/`
**Opsi A: Otomatis (Recommended)** ⭐
```bash
cd backend
python download_model.py
```
Script ini akan otomatis:
- Membuat folder `data/` jika belum ada
- Download `sapa_model.pkl` dari Google Drive
- Simpan langsung ke `data/sapa_model.pkl` (sama seperti milikmu)

**Opsi B: Manual**
Jika download otomatis tidak bisa:
1. Download file dari link Google Drive yang kamu share
2. Rename menjadi `sapa_model.pkl`
3. Buat folder `data/` di root project (sejajar dengan folder `backend/`)
4. Letakkan file di dalam folder `data/`

**Struktur folder yang benar:**
```
AI - SAPA/
├── data/
│   └── sapa_model.pkl  ← File model disimpan di sini
├── backend/
├── frontend/
└── ...
```

### Step 5: Jalankan ML Pipeline
```bash
cd backend
python main.py
```

Script akan otomatis:
- Detect file `data/sapa_model.pkl` sudah ada
- Load model yang tersimpan
- Jalankan inference / training

---

## **Troubleshooting** 🔧

### ❌ "ERROR: File ID not set"
**Solusi:**
- Owner harus update `GOOGLE_DRIVE_FILE_ID` di `backend/download_model.py`
- Ganti `YOUR_FILE_ID_HERE` dengan file ID dari Google Drive
- Pastikan sudah di-push ke GitHub
- Teman klone ulang atau update branch baru

### ❌ "FileNotFoundError: data/sapa_model.pkl not found"
**Solusi:**
- Jalankan `python download_model.py` di folder `backend/`
- Atau download manual dan letakkan di folder `data/` (bukan di `backend/data/`)
- Struktur harus: `AI-SAPA/data/sapa_model.pkl` (tidak di dalam backend!)

### ❌ "Download error / Permission denied"
**Solusi:**
- Cek apakah link Google Drive sudah di-share dengan "Anyone with link"
- Coba download manual via browser → copy link ke tautan Google Drive
- Pastikan file tersebut adalah file (bukan folder)

### ❌ "ModuleNotFoundError: requests"
**Solusi:**
- Pastikan virtual environment sudah activate (lihat `(venv)` di terminal)
- Jalankan: `pip install -r backend/requirements.txt`
- Jangan lupa update `requirements.txt` sudah ada `requests`

### ❌ "Connection timeout / Download tergantung"
**Solusi:**
- Cek koneksi internet
- Coba manual download dari Google Drive via browser
- Jika file terlalu besar (792MB), tunggu lebih lama

### ✅ "Model sudah ada"
**Artinya:**
- Download sudah berhasil sebelumnya
- Bisa langsung jalankan `main.py`
- Gak perlu download ulang kecuali model di-update

---

## **Tips & Trik** 💡
- 💾 Model hanya perlu didownload **1x saja** (cek di folder `data/`)
- 🔒 Jangan share Google Drive File ID ke publik (privacy/security)
- 📌 Simpan link Google Drive backup di dokumentasi internal
- ⚡ File size: ~792 MB (ambil waktu ~5-15 menit sesuai kecepatan internet)
- 🔄 Setiap update model, owner upload ulang ke Google Drive & update `GOOGLE_DRIVE_FILE_ID`
- 📱 Bisa download di Windows/Linux/Mac dengan script yang sama


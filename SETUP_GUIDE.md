# 📥 Setup Guide - Download Model dari Google Drive

### Step 3: Push ke GitHub
Sebelum push, pastikan sudah:
1. Update **KEDUA FILE_ID** di `backend/download_model.py`
2. Verifikasi: File ID sudah di-ganti dari `YOUR_FILE_ID_HERE`

Kemudian jalankan:
```bash
git add backend/download_model.py backend/requirements.txt SETUP_GUIDE.md
git commit -m "Add Google Drive model download script for inference"
git push
```

✅ **PENTING:** File CSV dan cache files sudah di-exclude via `.gitignore` (tidak perlu di-push)
- Teman bisa straight jalankan tanpa mendownload dataset (hanya model files)


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
- Download `sapa_model.pkl` dari Google Drive (~800 MB, ambil 5-15 menit)
- Download `knowledge_base.pkl` dari Google Drive
- Simpan langsung ke `data/sapa_model.pkl` & `data/knowledge_base.pkl`

**📌 File yang Dibutuhkan Teman:**
```
✅ WAJIB DOWNLOAD:
- sapa_model.pkl (trained model)
- knowledge_base.pkl (medical knowledge base)

❌ TIDAK PERLU (hanya untuk training):
- augmented_dataset.csv
- hybrid_dataset.csv  
- train.csv, val.csv, test.csv
- bert_cache_*.npy
- kaggle_dataset.csv, kaggle_translated.csv
```

**Opsi B: Manual**
Jika download otomatis tidak bisa:
1. Download 2 file dari Google Drive: `sapa_model.pkl` + `knowledge_base.pkl`
2. Buat folder `data/` di root project (sejajar dengan folder `backend/`)
3. Letakkan kedua file di dalam folder `data/`

**Struktur folder yang benar:**
```
AI - SAPA/
├── data/
│   ├── sapa_model.pkl  ← WAJIB ada
│   └── knowledge_base.pkl  ← WAJIB ada
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

### ❌ "FileNotFoundError: knowledge_base.pkl not found"
**Solusi:**
- Pastikan `knowledge_base.pkl` sudah di-download ke folder `data/`
- Jalankan `python download_model.py` lagi
- Atau download manual dan letakkan di folder `data/`

### ❌ "Model loaded tapi ada warning: KB not found"
**Solusi:**
- Cek apakah `knowledge_base.pkl` ada di `data/`
- Jika tidak ada, download dari Google Drive
- Model tetap bisa jalan, tapi rekomendasi diagnosis kurang akurat

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
- 💾 **Hanya 2 file pkl yang dibutuhkan**: `sapa_model.pkl` + `knowledge_base.pkl`
  - CSV & cache files hanya untuk **training/validation** (tidak perlu untuk inference)
- 🚀 **Setup hanya 1x**: File model download sekali saja, tidak perlu diulang
- 🔒 Jangan share Google Drive File ID ke publik (privacy/security)
- 📌 Simpan link Google Drive backup di dokumentasi internal
- ⚡ File size: ~800 MB (ambil waktu ~5-15 menit sesuai kecepatan internet)
- 🔄 Setiap update model, owner upload ulang ke Google Drive & update `FILE_ID`
- 📱 Script bisa jalan di Windows/Linux/Mac (cross-platform)
- 🎯 Teman hanya perlu clone, install venv, install deps, download model, lalu run!


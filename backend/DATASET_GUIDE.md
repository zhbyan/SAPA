# SAPA Dataset Setup Guide

## 📊 Pilihan Dataset

Anda memiliki **3 opsi** untuk dataset:

### 1. **Dataset Kaggle (RECOMMENDED)** ⭐
- **Sumber**: Real medical dataset dari Kaggle
- **Jumlah**: ~4,920 samples
- **Penyakit**: 41 diseases
- **Link**: [Disease Symptom Dataset](https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset)

### 2. **Synthetic Dataset** (Fallback)
- **Sumber**: Generated dari script `generate_data.py`
- **Jumlah**: ~1,200 samples
- **Penyakit**: 6 diseases (DBD, Tifoid, ISPA, Gastritis, Hipertensi, Diabetes)

### 3. **Hybrid Dataset** (BEST) 🏆
- **Sumber**: Kombinasi Kaggle + Synthetic
- **Jumlah**: ~6,000+ samples
- **Penyakit**: 41+ diseases

---

## 🚀 Setup Kaggle Dataset

### Step 1: Install Kaggle API
```bash
pip install kaggle
```

### Step 2: Setup Kaggle API Key
1. Login ke [Kaggle.com](https://www.kaggle.com)
2. Klik foto profil → **Account**
3. Scroll ke **API** section
4. Klik **Create New API Token**
5. Download file `kaggle.json`

**Windows:**
```powershell
mkdir C:\Users\<username>\.kaggle
# Copy kaggle.json ke folder tersebut
```

**Linux/Mac:**
```bash
mkdir ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### Step 3: Download & Preprocess Dataset
```bash
cd backend
python download_kaggle_dataset.py
```

**Menu yang muncul:**
```
1. Download dataset dari Kaggle (Perlu API Key)
2. Preprocess dataset yang sudah didownload
3. Buat Hybrid dataset (Kaggle + Synthetic)
4. Jalankan semua (1+2+3)
```

**Pilih opsi 4** untuk hasil terbaik.

### Step 4: Train Model dengan Dataset Baru
```bash
python model_engine.py
```

Model akan otomatis memilih dataset terbaik yang tersedia (prioritas: hybrid > kaggle > synthetic).

---

## 📂 Struktur File Dataset

Setelah setup, folder `data/` akan berisi:

```
data/
├── kaggle_raw/              # Raw files dari Kaggle
│   ├── dataset.csv
│   ├── symptom_Description.csv
│   └── symptom_precaution.csv
├── kaggle_dataset.csv       # Kaggle yang sudah dipreprocess
├── synthetic_dataset.csv    # Generated synthetic data
├── hybrid_dataset.csv       # Kombinasi keduanya (BEST)
└── sapa_model.pkl          # Trained model
```

---

## 🎯 Expected Results

### Dengan Synthetic Dataset
- Accuracy: **~85-90%**
- Diseases: 6 penyakit umum Indonesia

### Dengan Kaggle Dataset
- Accuracy: **~90-95%**
- Diseases: 41 penyakit internasional

### Dengan Hybrid Dataset
- Accuracy: **~92-97%** 🏆
- Diseases: 41+ penyakit (Indonesia + Internasional)

---

## 🔄 Alternatif: Download Manual

Jika Kaggle API gagal, download manual:

1. Buka: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset
2. Klik **Download** (perlu login)
3. Extract file `archive.zip`
4. Copy semua `.csv` ke folder `backend/../data/kaggle_raw/`
5. Jalankan: `python download_kaggle_dataset.py` → Pilih opsi **2**

---

## 💡 Tips

1. **Rekomendasi**: Gunakan **Hybrid Dataset** untuk hasil terbaik
2. **Fast Start**: Tetap gunakan Synthetic jika tidak bisa setup Kaggle
3. **Custom Dataset**: Bisa tambahkan dataset sendiri dengan format:
   ```csv
   text,label
   "Pasien mengeluh demam tinggi dan sakit kepala","Demam Berdarah"
   ```

---

## ❓ Troubleshooting

**Error: "No module named kaggle"**
```bash
pip install kaggle
```

**Error: "403 Forbidden" saat download**
- Pastikan `kaggle.json` sudah di folder yang benar
- Pastikan sudah accept terms di halaman dataset Kaggle

**Dataset tidak ditemukan saat training**
```bash
# Cek apakah file ada
ls ../data/
# Jika kosong, generate synthetic dulu
python generate_data.py
```

# SAPA - Sistem Asistensi Pra-Asesmen Klinis

Sistem berbasis AI untuk membantu tenaga kesehatan (nakes) dalam melakukan triase dan dokumentasi medis menggunakan **Hybrid AI** (Random Forest + IndoBERT + Gemini LLM).

---

## 📁 Struktur Folder

```
AI - SAPA/
├── backend/              # Python/FastAPI + AI Engine
│   ├── main.py           # FastAPI server (entry point)
│   ├── model_engine.py   # Hybrid AI predictor (RF + BERT + KB)
│   ├── knowledge_base.py # Database 41 penyakit + 130 gejala + ICD-10
│   ├── llm_engine.py     # Integrasi Gemini LLM
│   ├── data_manager.py   # Pipeline data (Kaggle → augmentasi → split)
│   └── requirements.txt  # Dependencies Python
├── frontend/             # Angular 18 + TailwindCSS
│   ├── src/app/
│   │   ├── pages/        # Login, Triage (Nakes), Dashboard & Examination (Dokter)
│   │   ├── layouts/      # Doctor & Nurse sidebar layouts
│   │   ├── services/     # Auth & Patient service
│   │   └── data/         # ICD-10 database & clinical education
│   ├── angular.json
│   ├── tailwind.config.js
│   └── package.json
├── data/                 # Dataset & Model (generated, tidak di-push)
│   ├── kaggle_raw/       # Dataset asli dari Kaggle
│   ├── kaggle_dataset.csv
│   ├── sapa_model.pkl    # Model terlatih (~830MB, di-generate lokal)
│   └── knowledge_base.pkl
└── seed_patient.js       # Script seed data pasien (jalankan di browser console)
```

---

## 🚀 Cara Menjalankan

### **1. Frontend (Angular)**

```bash
cd frontend
npm install
npm start
```

Buka di browser: **http://localhost:4200**

| Halaman             | URL                  |
|---------------------|----------------------|
| Login               | `/`                  |
| Portal Nakes (Triase) | `/nurse/triage`    |
| Dashboard Dokter    | `/doctor`            |
| Pemeriksaan Pasien  | `/doctor/examine/:id`|

> **Login default:**
> - Nakes: `nakes` / `nakes123`
> - Dokter: `dokter` / `dokter123`

---

### **2. Backend (Python/FastAPI)**

> ⚠️ Backend memerlukan Python 3.10+ dengan `pandas`, `scikit-learn`, `torch`, dan `transformers`.

```bash
cd backend
python -m venv venv

# Aktivasi virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

**Generate dataset & train model:**

```bash
python data_manager.py       # Pipeline data (translate + augment + split)
python knowledge_base.py     # Build knowledge base
python model_engine.py       # Train model → ../data/sapa_model.pkl
```

**Jalankan server:**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API Docs: **http://localhost:8000/docs**
- Endpoint utama: `POST /predict`

---

## 🧠 Arsitektur AI

### Hybrid Model (3 komponen)

| Komponen         | Peran                                    | Detail                           |
|------------------|------------------------------------------|----------------------------------|
| **Random Forest**| Prediksi penyakit dari gejala            | TF-IDF + PCA + Calibrated RF    |
| **IndoBERT**     | Embedding teks keluhan Bahasa Indonesia  | `indobenchmark/indobert-base-p2` |
| **Knowledge Base**| Lookup ICD-10, gejala, symptom vector   | 41 penyakit, ~130 gejala         |

### Dataset

| Sumber                | Jumlah    | Keterangan                              |
|-----------------------|-----------|-----------------------------------------|
| Kaggle Disease-Symptom| ~600 baris| Dataset asli (Inggris → Indonesia)      |
| Template Augmentation | ~2400 baris| Variasi kalimat keluhan otomatis       |
| Gemini Augmentation   | ~1200 baris| Natural language dari Gemini AI        |
| **Total**             | **~4200** | Split: 80% train, 10% val, 10% test   |

### ICD-10

Data ICD-10 di-hardcode di `backend/knowledge_base.py` → **41 penyakit** dengan kode ICD-10 lengkap (A90 Dengue, A01.0 Typhoid, E11.9 Diabetes, dll).

---

## 📝 Fitur Utama

### Portal Nakes (Triase)
- ✅ Anamnesis AI melalui chat interaktif (Rasa-style fields)
- ✅ Input data vital & identitas pasien
- ✅ Prediksi diagnosis otomatis (top-3 + ICD-10)
- ✅ Resume medis auto-generated
- ✅ Kirim ke antrian Dokter

### Portal Dokter (Klinis)
- ✅ Dashboard antrian pasien dengan severity color coding
- ✅ Card pasien menampilkan: info vital, kunjungan, gejala, prediksi AI
- ✅ SOAP Editor (Subjektif, Objektif, Assessment, Plan)
  - Subjektif: textarea langsung editable + preview 3 Diagnosis Awal AI
  - Objektif: input vital signs, keadaan umum, hasil lab
  - Assessment: search ICD-10 database, status kasus, prognosis
  - Plan: resep obat, edukasi, tindak lanjut
- ✅ **Simpan per bagian** (S/O/A/P terpisah) dengan validasi selesai
- ✅ Sidebar melayang (floating) dengan rounded corners

---

## 🔧 Tech Stack

| Layer     | Teknologi                         |
|-----------|-----------------------------------|
| Frontend  | Angular 18, TailwindCSS, Lucide Icons |
| Backend   | Python, FastAPI, Uvicorn          |
| AI/ML     | scikit-learn, PyTorch, HuggingFace Transformers |
| LLM       | Google Gemini 2.5 Flash           |
| Data      | Kaggle Disease-Symptom Dataset    |

---

## 🛠️ Troubleshooting

### Frontend blank / error
```bash
cd frontend
npm install
npm start
```

### Backend: module not found
```bash
cd backend
pip install -r requirements.txt
```

### Model belum ada (`sapa_model.pkl`)
```bash
cd backend
python data_manager.py
python model_engine.py
```
> Model ~830MB akan di-generate di `../data/sapa_model.pkl`

---

## 📞 Support

Cek folder `backend/` dan `frontend/` masing-masing untuk detail di `requirements.txt` dan `package.json`.

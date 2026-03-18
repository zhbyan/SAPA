 # IMPLEMENTATION PLAN: SAPA AI System (Revisi v3)

> **Arsitektur**: IndoBERT (Fine-tuned) + TF-IDF + Knowledge Base + Random Forest (Calibrated)
> **Dataset**: Kaggle (Translated) + Alodokter (~500K) — **Tanpa Data Dummy**
> **Target**: Top-3 Accuracy ≥80% | ECE < 0.10
> **Base Model**: `indolem/indobert-base-uncased`

---

## 🗺️ Roadmap (6 Phase)

| Phase | Nama | Output | Estimasi |
|-------|------|--------|----------|
| 1 | Data Pipeline | `data/processed/` (50-100K records) | 2 minggu |
| 2 | Knowledge Base | `knowledge_base.pkl` + Symptom Dictionary | 3 hari |
| 3 | Model Training | `sapa_model.pkl` (Calibrated RF) | 1 minggu |
| 4 | Backend Integration | FastAPI `/predict` endpoint | 2 hari |
| 5 | Frontend (Chat UI) | Chat Interface Nakes + Dashboard Dokter | 1 minggu |
| 6 | LLM Integration | Groq/Gemini reasoning endpoint | 2 hari |

---

## 📦 PHASE 1: Data Pipeline (Tanpa Data Dummy)

**Goal**: Menghasilkan dataset berkualitas dari **2 sumber real**: Kaggle (translated) + Alodokter.

### 1.1 Kaggle Dataset — Translation & Validation

#### [MODIFY] [download_kaggle_dataset.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/download_kaggle_dataset.py)

**Perubahan dari versi lama**: Tidak lagi hanya translate nama penyakit. Sekarang buat **full translation table** (penyakit + gejala + variasi bahasa awam).

**Deliverables**:
1. **`data/kaggle_translated/diseases.json`** — 41 penyakit dengan format:
   ```json
   {
     "disease_en": "Dengue",
     "disease_id_formal": "Demam Berdarah Dengue (DBD)",
     "disease_id_awam": "DB / Demam Berdarah",
     "icd10": "A90",
     "synonyms": ["DBD", "Demam Berdarah", "Dengue Fever"]
   }
   ```
2. **`data/kaggle_translated/symptoms.json`** — ~130 gejala dengan variasi:
   ```json
   {
     "symptom_en": "vomiting",
     "canonical_id": "muntah",
     "variants": ["muntah-muntah", "mual sampai muntah", "keluar isi perut"],
     "body_system": "pencernaan",
     "icd10": "R11.1"
   }
   ```
3. **`data/kaggle_translated/disease_symptom_matrix.npy`** — Binary matrix 41×130.

**Langkah**:
| Hari | Task | Detail |
|------|------|--------|
| 1-2 | Analisis & Setup | Download 3 CSV Kaggle, identifikasi 41 diseases + ~130 symptoms |
| 3-4 | Translate Penyakit | Nama medis formal + awam + ICD-10 + sinonim |
| 4-5 | Translate Gejala | Canonical + 3-5 variasi per gejala, kelompokkan per body system |
| 6 | Validasi | Cross-ref Kamus Kedokteran Dorland, test 50 kalimat keluhan |
| 7 | Export | CSV, JSON, NumPy matrix, commit ke version control |

### 1.2 Alodokter Dataset — Extraction & Processing

#### [NEW] [process_alodokter.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/process_alodokter.py)

**Sumber**: [Mendeley Data](https://data.mendeley.com/datasets/p8d5bynh3m/1) (~500K konsultasi).

**Pipeline**:
1. **Download** dataset Alodokter dari Mendeley.
2. **EDA**: Distribusi panjang teks, distribusi kategori, pola bahasa.
3. **Diagnosis Extraction**: Regex + fuzzy matching dari jawaban dokter.
   ```python
   DIAGNOSIS_PATTERNS = [
       r'kemungkinan.*?mengalami\s+([\w\s]+?)(?=[,.])',
       r'terindikasi\s+([\w\s]+?)(?=[,.])',
       r'Anda mengalami\s+([\w\s]+?)(?=[,.])',
       r'diagnosis:\s+([\w\s]+?)(?=[,.])',
   ]
   ```
4. **Fuzzy Match** nama penyakit vs Kaggle disease list (Levenshtein distance < 3).
5. **Quality Filter**: Buang records dengan `overlap_score < 0.2`.
6. **Target**: 50,000–100,000 quality records.

**Deliverables**:
- `data/processed/alodokter_clean.csv` — (complaint, diagnosis, confidence_score, extracted_symptoms)
- `data/processed/train.csv`, `val.csv`, `test.csv` — Split 80/10/10, stratified by diagnosis.

### 1.3 Combined Dataset

#### [MODIFY] [data_manager.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/data_manager.py)

**Perubahan**: Hapus semua logika `generate_data.py` (synthetic/dummy). Gabungkan hanya Kaggle (translated) + Alodokter (extracted).

```
Kaggle Translated (4,920 records) + Alodokter Clean (50-100K records)
→ Merge → Stratified Split → train.csv / val.csv / test.csv
```

#### [DELETE] [generate_data.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/generate_data.py)

File ini tidak lagi diperlukan karena kita menggunakan data real.

---

## 🧠 PHASE 2: Knowledge Base

**Goal**: Membangun "Kamus Medis" yang digunakan sebagai fitur tambahan untuk model.

#### [NEW] [knowledge_base.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/knowledge_base.py)

**Class**: `DiseaseKnowledgeBase`

**Methods**:
| Method | Input | Output | Fungsi |
|--------|-------|--------|--------|
| `get_symptoms(disease)` | Nama penyakit | List gejala | Ambil gejala dari matrix |
| `get_icd10(disease)` | Nama penyakit | Kode ICD-10 | Lookup kode |
| `get_symptom_vector(text)` | Teks keluhan | Vector 130-dim | Deteksi gejala → binary vector |
| `extract_symptoms(text)` | Teks keluhan | List nama gejala | Rule-based symptom detection |

**Cara kerja `get_symptom_vector()`**:
```
Input: "Dok saya demam tinggi dan bintik merah"
→ Match "demam" (canonical) + "bintik" (variant of "ruam kulit")
→ Output: [0, 0, 1, 0, ..., 1, 0] (130-dim binary vector)
```

**Stored as**: `data/knowledge_base.pkl` (JSON + pickle untuk fast loading).

---

## 🔬 PHASE 3: Model Training Pipeline

**Goal**: Train pipeline lengkap: Fine-tune BERT → Extract Features → PCA → RF → Calibrate.

#### [MODIFY] [hybrid_trainer.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/hybrid_trainer.py)

**Arsitektur (6 Stage)**:

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│ Stage 1:    │    │ Stage 2:     │    │ Stage 3:     │
│ Fine-tune   │    │ Extract      │    │ TF-IDF +     │
│ IndoBERT    │───▶│ BERT Embed   │───▶│ KB Features  │
│ (5 epochs)  │    │ (768-dim)    │    │ (500+130-dim)│
└─────────────┘    └──────────────┘    └──────┬───────┘
                                              │
┌─────────────┐    ┌──────────────┐    ┌──────▼───────┐
│ Stage 6:    │    │ Stage 5:     │    │ Stage 4:     │
│ Calibrate   │◀───│ Train RF     │◀───│ Concat + PCA │
│ (Isotonic)  │    │ (300 trees)  │    │ (1398→256)   │
└─────────────┘    └──────────────┘    └──────────────┘
```

### Stage 1: Fine-tune IndoBERT (KUNCI AKURASI)

IndoBERT di-fine-tune sebagai classifier dulu agar paham konteks medis Indonesia.

- **Model**: `indolem/indobert-base-uncased`
- **Config**: `lr=2e-5`, `weight_decay=0.01`, `warmup=500 steps`, `max_length=256`
- **Epochs**: 5
- **Setelah fine-tune**: Buang classification head, simpan encoder saja.

### Stage 2: Extract BERT Embeddings

Gunakan BERT yang sudah fine-tune untuk menghasilkan embedding 768-dim dari semua data.

### Stage 3: TF-IDF + Knowledge Base Features

| Komponen | Dimensi | Konfigurasi |
|----------|---------|-------------|
| TF-IDF | 500 | `max_features=500, ngram_range=(1,2), sublinear_tf=True` |
| Knowledge Base | 130 | Binary symptom vector dari `knowledge_base.py` |

### Stage 4: Feature Concatenation + PCA

```
BERT (768) + TF-IDF (500) + KB (130) = 1,398 dimensi
→ StandardScaler (WAJIB sebelum PCA)
→ PCA(n_components=256) → 256 dimensi (93% variance retained)
```

### Stage 5: Random Forest Training

```python
rf = RandomForestClassifier(
    n_estimators=300,
    max_features="sqrt",  # sqrt(256) ≈ 16 fitur per split
    max_depth=25,
    min_samples_leaf=3,
    class_weight="balanced",
    oob_score=True,
    n_jobs=-1,
    random_state=42
)
```

### Stage 6: Probability Calibration (Isotonic Regression)

> [!IMPORTANT]
> Tanpa kalibrasi, RF overconfident (bilang 90% padahal realnya 65%). Untuk sistem medis, ini **BERBAHAYA**.

```python
calibrated_rf = CalibratedClassifierCV(rf, method="isotonic", cv="prefit")
calibrated_rf.fit(val_features_pca, val_labels)
```

**Target ECE**: < 0.10 (sebelum kalibrasi: ~0.20, sesudah: ~0.07).

### Pembagian Peran Komponen

| Komponen | Analogi | Tugas | Kelemahan yang Ditutup Oleh |
|----------|---------|-------|-----------------------------|
| **IndoBERT** | Ahli Bahasa | Pahami konteks ("badan panas" ≈ "demam") | TF-IDF (keyword spesifik) |
| **TF-IDF** | Mata Elang | Tangkap keyword vital ("bintik" → DBD) | IndoBERT (konteks kalimat) |
| **Knowledge Base** | Kamus Medis | Validasi gejala terstruktur (130-dim vector) | — |
| **PCA** | Kompresor | Kompres 1398→256 dimensi, 6x lebih cepat | — |
| **Random Forest** | Dokter Senior | Gabungkan semua laporan → keputusan final | Calibration (koreksi probabilitas) |
| **Calibration** | Quality Control | Koreksi probabilitas agar "jujur" | — |

**Output**: `data/sapa_model.pkl` berisi semua komponen (bert_encoder, tfidf, kb, scaler, pca, calibrated_rf, label_encoder).

---

## 🔌 PHASE 4: Backend Integration

**Goal**: Pasang model ke FastAPI, buat inference endpoint.

#### [MODIFY] [model_engine.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/model_engine.py)

**Class**: `SAPAInference` — Load semua komponen, expose `predict(text, top_k=3)`.

**Output format**:
```json
{
  "top_diagnoses": [
    {"rank": 1, "disease": "Bronkitis Akut", "probability": 72.3, "icd10": "J20.9", "confidence": "TINGGI"},
    {"rank": 2, "disease": "ISPA", "probability": 18.4, "icd10": "J06.9", "confidence": "SEDANG"},
    {"rank": 3, "disease": "Pneumonia", "probability": 9.3, "icd10": "J18.9", "confidence": "RENDAH"}
  ],
  "detected_symptoms": ["demam", "batuk berdahak", "sesak napas"],
  "expected_symptoms": ["demam", "batuk", "dahak", "nyeri dada"],
  "soap_subjective": "Pasien datang dengan keluhan: ..."
}
```

#### [MODIFY] [main.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/main.py)

**Endpoints**:
- `POST /predict` — Keluhan → Top-3 diagnosis + symptoms + SOAP draft.
- `GET /health` — Status server.

---

## 🖥️ PHASE 5: Frontend (Chat UI Nakes + Dashboard Dokter)

**Goal**: Transformasi dari form ke chat interface (sesuai konsep PDF).

### 5.1 Chat Interface Nakes

- Nakes mengobrol dengan AI untuk input keluhan.
- AI menanyakan pertanyaan follow-up (jika perlu).
- Setelah semua field terpenuhi → AI generate prediksi Top-3.
- Tombol "Buat Laporan" → Kirim ringkasan ke Dokter.

### 5.2 Dashboard Dokter

- Lihat antrian pasien dengan kode warna triase.
- Data pasien + hasil prediksi AI + draft SOAP.
- Dokter bisa menyetujui/mengoreksi prediksi AI.

### 5.3 Frontend Polish

- Hapus semua mock data fallback.
- Confidence threshold indicators (Hijau/Kuning/Merah).
- Error handling yang jelas ("Gagal terhubung ke AI").

---

## 🤖 PHASE 6: LLM Integration — Gemini 2.5 Flash / Groq

**Goal**: AI Chat Agent yang ramah, cerdas, dan **memastikan semua field anamnesis terpenuhi** sebelum menghasilkan prediksi.

**Model**: `llama-3.3-70b-versatile` (Groq API)
**Library**: `groq`

#### [NEW] [llm_engine.py](file:///c:/Users/lenovo/OneDrive/Documents/vscode/AI%20-%20SAPA/backend/llm_engine.py)

### 6.1 Persona AI: **RASA** (Rekan Asistensi SAPA)

```
Nama       : RASA
Peran      : Asisten Klinis AI untuk Tenaga Kesehatan
Karakter   : Ramah, sabar, profesional tapi tidak kaku
Bahasa     : Bahasa Indonesia semi-formal (sopan tapi hangat)
Panggilan  : Memanggil nakes dengan "Kak" (contoh: "Halo, Kak Alex!")
```

**Contoh nada bicara RASA**:
- ✅ *"Baik Kak, saya catat ya keluhan pasiennya. Bisa Kak ceritakan sudah berapa lama gejalanya?"*
- ✅ *"Oke, muntah 2x ya. Ada keluhan lain yang menyertai, Kak? Misalnya demam atau nyeri perut?"*
- ❌ ~~"Silakan masukkan durasi onset gejala dalam format hari."~~ (terlalu robot)
- ❌ ~~"Data insufficient. Please provide more symptoms."~~ (terlalu dingin)

### 6.2 System Prompt (Lengkap)

```
Kamu adalah RASA (Rekan Asistensi SAPA), asisten klinis AI yang membantu
tenaga kesehatan (nakes) mengumpulkan data anamnesis pasien melalui
percakapan.

## KEPRIBADIAN
- Ramah, sabar, dan empatik — seperti rekan kerja yang supportif
- Gunakan bahasa Indonesia semi-formal (sopan tapi hangat, BUKAN kaku)
- Panggil nakes dengan "Kak" (contoh: "Halo, Kak!")
- Gunakan emoji secukupnya untuk kesan hangat (1-2 per pesan, jangan berlebihan)
- Jika nakes terlihat terburu-buru, sesuaikan tempo (langsung to-the-point)
- JANGAN pernah memberikan diagnosis pasti — selalu tekankan ini "prediksi awal"

## TUGAS UTAMA
Kumpulkan data berikut melalui percakapan NATURAL (JANGAN tanya sekaligus!):

### FIELD WAJIB (harus terpenuhi semua sebelum analisis):
1. **keluhan_utama** — Apa keluhan utama pasien? (teks bebas)
2. **durasi** — Sudah berapa lama? (contoh: "3 hari", "sejak tadi pagi")
3. **lokasi_keluhan** — Di bagian tubuh mana? (contoh: "perut kanan bawah")
4. **keparahan** — Seberapa parah? Skala 1-10 atau deskripsi (ringan/sedang/berat)
5. **gejala_penyerta** — Ada gejala lain yang menyertai? (demam, mual, dll.)
6. **riwayat_penyakit** — Punya riwayat penyakit tertentu? (DM, hipertensi, dll.)
7. **riwayat_alergi** — Ada alergi obat/makanan? (jika tidak ada, catat "Tidak ada")

### FIELD OPSIONAL (tanyakan jika relevan):
8. **obat_dikonsumsi** — Sudah minum obat apa?
9. **riwayat_keluarga** — Ada keluarga dengan penyakit serupa?
10. **tanda_vital** — Suhu, TD, Nadi (jika nakes sudah mengukur)

## ATURAN PERCAKAPAN
1. Mulai dengan SATU pertanyaan: keluhan utama
2. Tanyakan field berikutnya SATU PER SATU berdasarkan konteks
   (jangan bombardir pertanyaan)
3. Jika nakes sudah menyebutkan beberapa info sekaligus, JANGAN tanya ulang
   yang sudah disebutkan — langsung lanjut ke field yang belum
4. Setelah setiap jawaban, konfirmasi singkat + lanjut pertanyaan berikutnya
5. Jika jawaban ambigu, minta klarifikasi dengan sopan
6. Jika nakes bilang "tidak tahu" untuk field wajib, catat sebagai
   "Tidak diketahui" dan lanjut (jangan memaksa)

## ATURAN ANALISIS
- HANYA hasilkan analisis setelah SEMUA 7 FIELD WAJIB terkumpul
- Saat semua field terpenuhi, tanyakan: "Kak, data anamnesis sudah lengkap.
  Mau saya buatkan analisisnya sekarang?"
- Jika nakes setuju, hasilkan analisis dengan format di bawah

## FORMAT OUTPUT ANALISIS (saat semua field terpenuhi)
Jawab dalam format berikut:

**📋 RESUME MEDIS**
Pasien [usia jika diketahui] datang dengan keluhan [keluhan_utama]
sejak [durasi]. Lokasi: [lokasi]. Skala nyeri: [keparahan].
Disertai [gejala_penyerta]. Riwayat: [riwayat_penyakit].
Alergi: [riwayat_alergi].

**🔍 ANALISIS KASUS**
Berdasarkan anamnesis, berikut diagnosis prioritas:
1. **[Penyakit 1]** — Probabilitas: [Tinggi/Sedang/Rendah]
   - ICD-10: [kode]
   - Reasoning: [alasan singkat berdasarkan gejala]
2. **[Penyakit 2]** — Probabilitas: [Tinggi/Sedang/Rendah]
   - ICD-10: [kode]
   - Reasoning: [alasan]
3. **[Penyakit 3]** — Probabilitas: [Tinggi/Sedang/Rendah]
   - ICD-10: [kode]
   - Reasoning: [alasan]

**🩺 SARAN PEMERIKSAAN LANJUTAN**
- [Lab/fisik yang relevan]

⚠️ *Hasil ini bersifat indikatif sebagai decision support.
Keputusan klinis tetap di tangan dokter.*

## ATURAN KEAMANAN
- JANGAN pernah meresepkan obat
- JANGAN pernah bilang "Anda pasti menderita X"
- Selalu gunakan frasa: "kemungkinan", "perlu diperiksa lebih lanjut"
- Jika keluhan darurat (nyeri dada kiri, sesak berat, pendarahan hebat),
  LANGSUNG sarankan: "Kak, ini PERLU PENANGANAN SEGERA. Mohon segera
  rujuk ke IGD."
- Tolak pertanyaan di luar konteks medis dengan sopan
```

### 6.3 Field Tracking (Backend Logic)

Backend harus melacak field mana yang sudah terkumpul per sesi chat:

```python
REQUIRED_FIELDS = {
    "keluhan_utama": None,
    "durasi": None,
    "lokasi_keluhan": None,
    "keparahan": None,
    "gejala_penyerta": None,
    "riwayat_penyakit": None,
    "riwayat_alergi": None,
}

# LLM diminta return JSON selain chat response:
# {"field_updates": {"keluhan_utama": "nyeri perut", "durasi": "3 hari"}}
# Backend merge ke session → cek completeness
```

### 6.4 Chat Flow (Contoh Percakapan)

```
RASA  : Halo, Kak! 👋 Saya RASA, asisten klinis SAPA.
        Silakan ceritakan keluhan utama pasien yang akan diperiksa ya.

NAKES : Mual ada, muntah 2x isi makanan. Konstipasi belum BAB 2 hari.
        BAK lancar, tidak nyeri.

RASA  : Baik Kak, saya catat ya 📝
        • Mual + muntah 2x (isi makanan)
        • Konstipasi (belum BAB 2 hari)
        • BAK normal

        Sudah berapa lama keluhan ini dirasakan pasien, Kak?

NAKES : Sejak kemarin sore

RASA  : Oke, sekitar 1 hari ya. Kalau boleh tahu, nyeri perutnya
        di bagian mana, Kak? Kanan, kiri, atas, bawah, atau seluruh perut?

NAKES : Ulu hati, kadang ke kanan bawah juga

RASA  : Baik, nyeri di ulu hati menjalar ke kanan bawah.
        Dari skala 1-10, kira-kira seberapa nyeri yang dirasakan pasien?

NAKES : Sekitar 6

RASA  : Oke, nyeri skala 6. Ada demam atau keluhan lain yang menyertai, Kak?

NAKES : Suhu 37.8, agak hangat. Tidak ada keluhan lain.

RASA  : Baik, suhu subfebris 37.8°C. Dua pertanyaan terakhir ya Kak:
        1. Pasien punya riwayat penyakit tertentu? (DM, hipertensi, maag?)
        2. Ada alergi obat atau makanan?

NAKES : Riwayat maag, alergi tidak ada

RASA  : ✅ Data anamnesis sudah lengkap, Kak. Mau saya buatkan analisisnya?

NAKES : Ya

RASA  : 📋 RESUME MEDIS
        ...
```

### 6.5 Endpoints

| Endpoint | Method | Input | Output |
|----------|--------|-------|--------|
| `/chat` | POST | `{session_id, message, patient_info}` | `{reply, field_status, is_complete}` |
| `/chat/generate-report` | POST | `{session_id}` | `{analysis, soap_draft, top_diagnoses}` |

---

## 📊 Target Performa Realistis

| Metric | Target | Keterangan |
|--------|--------|------------|
| Top-1 Accuracy | ≥65% | Primary diagnosis hit rate |
| Top-3 Accuracy | ≥80% | Key metric untuk SAPA |
| Disease F1 (macro) | ≥0.60 | Balanced across diseases |
| ECE (Calibration) | < 0.10 | Well-calibrated probabilities |
| Inference Latency | < 500ms | End-to-end response time |

---

## ⚠️ Risk Management

| Risk | Mitigasi |
|------|----------|
| Kualitas translasi rendah | Wajib medical expert review; gunakan Kamus Kedokteran Dorland |
| Alodokter extraction < 40% | Turunkan threshold; augment dengan Kaggle; label manual 1K records |
| Model overfit | Tambah dropout, weight decay; monitor train-val gap |
| GPU out of memory | Kurangi batch size ke 8-16; gradient checkpointing; fp16 |
| Timeline melebihi target | Pivot ke Approach 2 (TF-IDF + RF saja, tanpa fine-tune BERT) |

---

## ✅ Checklist Eksekusi

| # | Task | Prioritas | Estimasi | Status |
|---|------|-----------|----------|--------|
| 1 | Install dependencies | ✅ Done | — | ✅ |
| 2 | Translate Kaggle dataset (41 diseases + 130 symptoms) | KRITIS | 1 minggu | ✅ |
| 3 | Download & process Alodokter dataset | KRITIS | 1 minggu | ✅ |
| 4 | Build Knowledge Base (Python class) | KRITIS | 1-2 hari | ✅ |
| 5 | Fine-tune IndoBERT (5 epoch) | KRITIS | 4-6 jam (GPU) | ✅ |
| 6 | Extract BERT embeddings + TF-IDF + KB features | KRITIS | 1-2 jam | ✅ |
| 7 | PCA + Train RF (300 trees) | KRITIS | 15 menit | ✅ |
| 8 | Calibrate RF (Isotonic Regression) | KRITIS | 5 menit | ✅ |
| 9 | Update model_engine.py (inference pipeline) | KRITIS | 2 jam | ✅ |
| 10 | Frontend Chat UI (Nakes) | PENTING | 3-5 hari | ✅ |
| 11 | Frontend Dashboard (Dokter) | PENTING | 2-3 hari | ✅ |
| 12 | LLM Integration (Diganti dari Gemini ke Groq llama-3.3-70b-versatile) | OPSIONAL | 1 hari | ✅ |
| 13 | Evaluasi lengkap + dokumentasi | PENTING | 1 hari | ✅ |

# 🐍 PANDUAN INSTALASI & SETUP ANACONDA UNTUK SAPA

Karena Anda memilih menggunakan Anaconda (Pilihan Terbaik! 🏆), berikut adalah langkah-langkah detail agar proyek SAPA bisa berjalan mulus.

---

## 🏗️ TAHAP 1: Install Anaconda
1.  **Download**: Kunjungi [anaconda.com/download](https://www.anaconda.com/download) dan download installer untuk Windows (64-bit).
2.  **Install**: Jalankan installer.
    *   Klik *Next* terus sampai selesai.
    *   Tunggu prosesnya (sekitar 5-10 menit).
3.  **Verifikasi**: Buka menu Start, cari **"Anaconda Prompt"** (ikon hitam). Buka aplikasi itu.
    *   Ketik: `conda --version`
    *   Jika muncul angka (misal `conda 23.7.4`), berarti sukses!

---

## 🛠️ TAHAP 2: Buat Lingkungan Baru (Environment)
Kita akan membuat "ruang kerja" khusus bernama `sapa-env` agar tidak tercampur dengan program lain.

1.  Buka **Anaconda Prompt**.
2.  Jalankan perintah berikut satu per satu (tekan Enter setiap baris):

    ```bash
    # 1. Buat environment baru dengan Python 3.10 (Versi paling stabil untuk AI)
    conda create -n sapa-env python=3.10 -y

    # 2. Aktifkan environment tersebut
    conda activate sapa-env
    ```

    *(Tanda sukses: Tulisan di kiri prompt berubah dari `(base)` menjadi `(sapa-env)`)*

---

## 📦 TAHAP 3: Install Library AI (Cara Conda)
Di sinilah keajaiban Anaconda. Kita install library yang susah-susah dulu lewat Conda.

Copy-paste perintah ini ke Anaconda Prompt:

```bash
# Install library dasar Data Science & Torch (Download agak besar ~1GB)
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
conda install pandas numpy scikit-learn -y
conda install -c conda-forge transformers tqdm -y
```

---

## 🔌 TAHAP 4: Install Library Backend (Cara Pip)
Sisanya (library web server) kita install pakai pip seperti biasa.

1.  Pastikan Anda masih di dalam `(sapa-env)`.
2.  Pindah ke folder project Anda (Sesuaikan path-nya):
    ```bash
    cd "c:\Users\lenovo\OneDrive\Documents\vscode\AI - SAPA\backend"
    ```
3.  Install sisa dependencies:
    ```bash
    pip install fastapi uvicorn python-multipart kaggle python-dotenv
    ```

---

## 🚀 TAHAP 5: EKSEKUSI (Akhirnya!)
Sekarang semua alat sudah siap. Mari kita jalankan rencana `IMPLEMENTATION PLAN` kemarin.

Tetap di **Anaconda Prompt**, jalankan urutan ini:

1.  **Siapkan Data** (Gabung Kaggle + Synthetic):
    ```bash
    python data_manager.py
    ```
    *(Harus muncul: "SUCCESS: Hybrid Dataset created")*

2.  **Training AI** (Latih Otak IndoBERT):
    ```bash
    python hybrid_trainer.py
    ```
    *(Tunggu proses download model & training selesai)*

3.  **Jalankan Server**:
    ```bash
    uvicorn main:app --reload
    ```

---

## 💡 Tips Penting
Setiap kali mau kerja lagi besok-besok:
1.  Buka **Anaconda Prompt**.
2.  Ketik `conda activate sapa-env`.
3.  Baru jalankan perintah python lainnya.

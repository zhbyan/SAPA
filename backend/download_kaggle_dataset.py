"""
Download dan preprocessing dataset medis dari Kaggle
Dataset: Disease Symptom Prediction
Source: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset
"""

import pandas as pd
import os
import sys

def download_from_kaggle():
    """
    Download dataset dari Kaggle menggunakan Kaggle API
    Perlu setup Kaggle API Key terlebih dahulu
    """
    print("=" * 60)
    print("SETUP KAGGLE API (Langkah pertama kali)")
    print("=" * 60)
    print("1. Login ke Kaggle.com")
    print("2. Go to: Account > API > Create New API Token")
    print("3. Download file 'kaggle.json'")
    print("4. Windows: Taruh di C:\\Users\\<username>\\.kaggle\\kaggle.json")
    print("5. Linux/Mac: Taruh di ~/.kaggle/kaggle.json")
    print("=" * 60)
    print()
    
    try:
        import kaggle
        print("✓ Kaggle API sudah terinstall")
    except ImportError:
        print("✗ Installing Kaggle API...")
        os.system("pip install kaggle")
        import kaggle
    
    # Download dataset
    print("\nDownloading dataset dari Kaggle...")
    dataset_name = "itachi9604/disease-symptom-description-dataset"
    download_path = "../data/kaggle_raw"
    
    try:
        kaggle.api.dataset_download_files(
            dataset_name,
            path=download_path,
            unzip=True
        )
        print(f"✓ Dataset berhasil didownload ke: {download_path}")
        return True
    except Exception as e:
        print(f"✗ Error downloading: {e}")
        print("\nAlternatif: Download manual dari:")
        print(f"https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset")
        print(f"Lalu extract ke folder: {download_path}")
        return False

# Translation Dictionaries
SYMPTOM_TRANSLATION = {
    "abdominal pain": "sakit perut",
    "abnormal menstruation": "haid tidak normal",
    "acidity": "asam lambung naik",
    "acute liver failure": "gagal hati akut",
    "altered sensorium": "kesadaran berubah",
    "anxiety": "cemas",
    "back pain": "sakit punggung",
    "belly pain": "sakit perut",
    "blackheads": "komedo",
    "bladder discomfort": "tidak nyaman di kandung kemih",
    "blister": "melepuh",
    "blood in sputum": "batuk berdarah",
    "bloody stool": "buang air besar berdarah",
    "blurred and distorted vision": "penglihatan kabur",
    "breathlessness": "sesak napas",
    "brittle nails": "kuku rapuh",
    "bruising": "memar",
    "burning micturition": "rasa terbakar saat buang air kecil",
    "chest pain": "sakit dada",
    "chills": "menggigil",
    "cold hands and feets": "tangan dan kaki dingin",
    "coma": "koma",
    "congestion": "hidung tersumbat",
    "constipation": "sembelit",
    "continuous feel of urine": "rasa ingin pipis terus",
    "continuous sneezing": "bersin terus menerus",
    "cough": "batuk",
    "cramps": "kram",
    "dark urine": "urine berwarna gelap",
    "dehydration": "dehidrasi",
    "depression": "depresi",
    "diarrhoea": "diare",
    "dischromic patches": "bercak perubahan warna kulit",
    "distention of abdomen": "perut kembung",
    "dizziness": "pusing",
    "drying and tingling lips": "bibir kering dan kesemutan",
    "enlarged thyroid": "pembesaran tiroid",
    "excessive hunger": "rasa lapar berlebihan",
    "extra marital contacts": "kontak seksual berisiko",
    "family history": "riwayat keluarga",
    "fast heart rate": "detak jantung cepat",
    "fatigue": "lemas",
    "fluid overload": "kelebihan cairan",
    "foul smell of urine": "bau urine menyengat",
    "headache": "sakit kepala",
    "high fever": "demam tinggi",
    "hip joint pain": "nyeri sendi panggul",
    "history of alcohol consumption": "riwayat konsumsi alkohol",
    "increased appetite": "nafsu makan meningkat",
    "indigestion": "gangguan pencernaan",
    "inflammatory nails": "kuku meradang",
    "internal itching": "gatal di dalam",
    "irregular sugar level": "kadar gula tidak teratur",
    "irritability": "mudah marah",
    "irritation in anus": "iritasi di anus",
    "joint pain": "nyeri sendi",
    "knee pain": "sakit lutut",
    "lack of concentration": "sulit berkonsentrasi",
    "lethargy": "lesu",
    "loss of appetite": "hilang nafsu makan",
    "loss of balance": "hilang keseimbangan",
    "loss of smell": "hilang penciuman",
    "malaise": "tidak enak badan",
    "mild fever": "demam ringan",
    "mood swings": "perubahan suasana hati",
    "movement stiffness": "kaku saat bergerak",
    "mucoid sputum": "dahak berlendir",
    "muscle pain": "nyeri otot",
    "muscle wasting": "pengecilan otot",
    "muscle weakness": "lemah otot",
    "nausea": "mual",
    "neck pain": "sakit leher",
    "nodal skin eruptions": "benjolan merah di kulit",
    "obesity": "obesitas",
    "pain behind the eyes": "sakit di belakang mata",
    "pain during bowel movements": "sakit saat buang air besar",
    "pain in anal region": "sakit di daerah anus",
    "painful walking": "sakit saat berjalan",
    "palpitations": "jantung berdebar",
    "passage of gases": "sering buang gas",
    "patches in throat": "bercak di tenggorokan",
    "phlegm": "dahak",
    "polyuria": "sering buang air kecil",
    "prominent veins on calf": "urat menonjol di betis",
    "puffy face and eyes": "wajah dan mata bengkak",
    "pus filled pimples": "jerawat bernanah",
    "receiving blood transfusion": "menerima transfusi darah",
    "receiving unsterile injections": "menerima suntikan tidak steril",
    "red sore around nose": "luka merah di sekitar hidung",
    "red spots over body": "bintik merah di seluruh tubuh",
    "redness of eyes": "mata merah",
    "restlessness": "gelisah",
    "runny nose": "hidung meler",
    "rusty sputum": "dahak berwarna karat",
    "scurring": "luka gores",
    "shivering": "menggigil",
    "silver like dusting": "sisik perak",
    "sinus pressure": "tekanan sinus",
    "skin peeling": "kulit mengelupas",
    "skin rash": "ruam kulit",
    "slurred speech": "bicara pelat",
    "small dents in nails": "lekukan kecil di kuku",
    "spinning movements": "berputar-putar",
    "spotting urination": "bercak urin",
    "stiff neck": "leher kaku",
    "stomach bleeding": "pendarahan lambung",
    "stomach pain": "sakit perut",
    "sunken eyes": "mata cekung",
    "sweating": "berkeringat",
    "swelled lymph nodes": "kelenjar getah bening bengkak",
    "swelling joints": "sendi bengkak",
    "swelling of stomach": "perut membengkak",
    "swollen blood vessels": "pembuluh darah bengkak",
    "swollen legs": "kaki bengkak",
    "throat irritation": "iritasi tenggorokan",
    "toxic look (typhos)": "wajah pucat sakit",
    "ulcers on tongue": "sariawan di lidah",
    "unsteadiness": "tidak stabil",
    "visual disturbances": "gangguan pengelihatan",
    "vomiting": "muntah",
    "watering from eyes": "mata berair",
    "weakness in limbs": "lemah anggota gerak",
    "weakness of one body side": "lemah satu sisi tubuh",
    "weight gain": "berat badan naik",
    "weight loss": "berat badan turun",
    "yellow crust ooze": "cairan kuning mengeras",
    "yellow urine": "urine kuning pekat",
    "yellowing of eyes": "mata menguning",
    "yellowish skin": "kulit menguning"
}

DISEASE_TRANSLATION = {
    "Dengue": "Demam Berdarah Dengue (DBD)",
    "Typhoid": "Tifush (Demam Tifoid)",
    "Tuberculosis": "TBC (Tuberkulosis)",
    "Common Cold": "ISPA/Influenza",
    "Pneumonia": "Pneumonia (Radang Paru)",
    "Diabetes ": "Diabetes Melitus",
    "Hypertension ": "Hipertensi",
    "Migraine": "Migrain",
    "Malaria": "Malaria",
    "Chicken pox": "Cacar Air",
    "Bronchial Asthma": "Asma Bronkial",
    "Gastroenteritis": "Gastroenteritis (Muntaber)",
    "Drug Reaction": "Reaksi Obat/Alergi",
    "Peptic ulcer diseae": "Gastritis (Maag)",
    "Jaundice": "Penyakit Kuning",
    "Fungal infection": "Infeksi Jamur",
    "Allergy": "Alergi",
    "GERD": "GERD (Asam Lambung)",
    "Chronic cholestasis": "Kolestasis Kronis",
    "Hepatitis A": "Hepatitis A", 
    "Hepatitis B": "Hepatitis B",
    "Hepatitis C": "Hepatitis C",
    "Hepatitis D": "Hepatitis D",
    "Hepatitis E": "Hepatitis E",
    "Alcoholic hepatitis": "Hepatitis Alkoholik",
    "AIDS": "HIV/AIDS",
    "Urinary tract infection": "Infeksi Saluran Kemih",
    "Psoriasis": "Psoriasis",
    "Impetigo": "Impetigo",
    "Acne": "Jerawat",
    "Dimorphic hemmorhoids(piles)": "Wasir/Ambeien",
    "Cervical spondylosis": "Saraf Leher Terjepit",
    "Hyperthyroidism": "Hipertiroid",
    "Hypothyroidism": "Hipotiroid",
    "Hypoglycemia": "Hipoglikemia (Gula Darah Rendah)",
    "Osteoarthristis": "Osteoartritis",
    "Arthritis": "Radang Sendi",
    "(vertigo) Paroymsal  Positional Vertigo": "Vertigo",
    "Varicose veins": "Varises",
    "Paralysis (brain hemorrhage)": "Kelumpuhan (Pendarahan Otak)",
    "Heart attack": "Serangan Jantung"
}

def preprocess_kaggle_dataset():
    """
    Mengubah format dataset Kaggle menjadi format yang compatible dengan model SAPA
    """
    print("\n" + "=" * 60)
    print("PREPROCESSING DATASET (WITH TRANSLATION)")
    print("=" * 60)
    
    raw_path = "../data/kaggle_raw"
    output_path = "../data/kaggle_dataset.csv"
    
    # Cek apakah file sudah ada
    if not os.path.exists(os.path.join(raw_path, "dataset.csv")):
        print(f"✗ File dataset.csv tidak ditemukan di {raw_path}")
        print("Silakan download dataset terlebih dahulu")
        return False
    
    # Load dataset
    print("Loading dataset...")
    df_symptoms = pd.read_csv(os.path.join(raw_path, "dataset.csv"))
    
    # Dataset Kaggle format: Disease, Symptom_1, Symptom_2, ..., Symptom_17
    # SAPA format: text (keluhan), label (diagnosis)
    
    print(f"Original dataset: {len(df_symptoms)} rows, {df_symptoms.columns.tolist()}")
    
    # Transform ke format SAPA
    data = []
    print("Translating symptoms & diseases to Indonesian...")
    
    for idx, row in df_symptoms.iterrows():
        # Translate Disease
        original_disease = row['Disease'].strip()
        disease = DISEASE_TRANSLATION.get(original_disease, original_disease)
        
        # Ambil semua symptom yang tidak null
        symptoms = []
        for col in df_symptoms.columns:
            if col.startswith('Symptom') and pd.notna(row[col]):
                # Clean symptom text (remove underscore, lowercase)
                raw_symptom = str(row[col]).replace('_', ' ').strip()
                
                # TRANSLATE SYMPTOM
                symptom = SYMPTOM_TRANSLATION.get(raw_symptom, raw_symptom)
                
                if symptom:
                    symptoms.append(symptom)
        
        if symptoms:
            # Buat kalimat keluhan natural dari symptoms
            # Template bahasa Indonesia
            templates = [
                f"Pasien mengeluh {', '.join(symptoms[:-1])} dan {symptoms[-1]}",
                f"Saya mengalami {symptoms[0]}, {', '.join(symptoms[1:])}",
                f"Keluhan utama: {', '.join(symptoms)}",
                f"Gejala yang dialami: {' serta '.join(symptoms[:2])}",
                f"Dok, saya merasa {symptoms[0]} dan {symptoms[-1]}",
                f"Badan terasa {symptoms[0]} disertai {', '.join(symptoms[1:])}"
            ]
            
            # Pilih template berdasarkan index
            template_idx = idx % len(templates)
            complaint = templates[template_idx] if len(symptoms) > 1 else f"Pasien mengeluh {symptoms[0]}"
            
            data.append({
                'text': complaint,
                'label': disease
            })
    
    # Convert to DataFrame
    df_sapa = pd.DataFrame(data)
    
    # Shuffle data
    df_sapa = df_sapa.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_sapa.to_csv(output_path, index=False)
    
    print(f"\n✓ Dataset SAPA (Translated) berhasil dibuat!")
    print(f"  - Total samples: {len(df_sapa)}")
    print(f"  - Unique diseases: {df_sapa['label'].nunique()}")
    print(f"  - Saved to: {output_path}")
    print(f"\nContoh data (Indonesian):")
    print(df_sapa.head())
    
    return True

def hybrid_dataset():
    """
    Gabungkan dataset Kaggle dengan synthetic data untuk hasil optimal
    """
    print("\n" + "=" * 60)
    print("CREATING HYBRID DATASET (Kaggle + Synthetic)")
    print("=" * 60)
    
    kaggle_path = "../data/kaggle_dataset.csv"
    synthetic_path = "../data/synthetic_dataset.csv"
    hybrid_path = "../data/hybrid_dataset.csv"
    
    datasets = []
    
    # Load Kaggle dataset
    if os.path.exists(kaggle_path):
        df_kaggle = pd.read_csv(kaggle_path)
        print(f"✓ Kaggle dataset: {len(df_kaggle)} samples")
        datasets.append(df_kaggle)
    else:
        print("✗ Kaggle dataset tidak ditemukan")
    
    # Load Synthetic dataset
    if os.path.exists(synthetic_path):
        df_synthetic = pd.read_csv(synthetic_path)
        print(f"✓ Synthetic dataset: {len(df_synthetic)} samples")
        datasets.append(df_synthetic)
    else:
        print("✗ Synthetic dataset tidak ditemukan")
    
    if not datasets:
        print("✗ Tidak ada dataset yang ditemukan!")
        return False
    
    # Gabungkan
    df_hybrid = pd.concat(datasets, ignore_index=True)
    df_hybrid = df_hybrid.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Save
    df_hybrid.to_csv(hybrid_path, index=False)
    
    print(f"\n✓ Hybrid dataset berhasil dibuat!")
    print(f"  - Total samples: {len(df_hybrid)}")
    print(f"  - Unique diseases: {df_hybrid['label'].nunique()}")
    print(f"  - Saved to: {hybrid_path}")
    
    return True

def main():
    print("╔" + "=" * 58 + "╗")
    print("║  SAPA - KAGGLE DATASET DOWNLOADER & PREPROCESSOR      ║")
    print("╚" + "=" * 58 + "╝")
    
    print("\nPilih opsi:")
    print("1. Download dataset dari Kaggle (Perlu API Key)")
    print("2. Preprocess dataset yang sudah didownload")
    print("3. Buat Hybrid dataset (Kaggle + Synthetic)")
    print("4. Jalankan semua (1+2+3)")
    
    choice = input("\nPilihan (1/2/3/4): ").strip()
    
    if choice == "1":
        download_from_kaggle()
    elif choice == "2":
        preprocess_kaggle_dataset()
    elif choice == "3":
        hybrid_dataset()
    elif choice == "4":
        if download_from_kaggle():
            if preprocess_kaggle_dataset():
                hybrid_dataset()
    else:
        print("Pilihan tidak valid")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("SELESAI!")
    print("=" * 60)
    print("Next step: Jalankan `python model_engine.py` untuk training")

if __name__ == "__main__":
    main()

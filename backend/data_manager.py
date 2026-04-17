"""
SAPA Data Pipeline — Phase 1: Real Data Only (No Synthetic/Dummy)
Combines Kaggle (translated + Gemini-augmented) with stratified splits.
Uses Gemini 2.5 Flash Lite for natural language augmentation.
"""

import pandas as pd
import numpy as np
import os
import sys
import json
import time
import random
from pathlib import Path

# Paths
DATA_DIR = "../data"
KAGGLE_RAW = os.path.join(DATA_DIR, "kaggle_raw", "dataset.csv")
KAGGLE_TRANSLATED = os.path.join(DATA_DIR, "kaggle_translated.csv")
AUGMENTED_PATH = os.path.join(DATA_DIR, "augmented_dataset.csv")
TRAIN_PATH = os.path.join(DATA_DIR, "train.csv")
VAL_PATH = os.path.join(DATA_DIR, "val.csv")
TEST_PATH = os.path.join(DATA_DIR, "test.csv")
FINAL_DATASET = os.path.join(DATA_DIR, "hybrid_dataset.csv")

# Gemini API Key
GEMINI_API_KEY = "AIzaSyA1xeDvYANK-g5UvKnhg3TmIKtGxJWm9lQ"

# Import translations from existing file
from download_kaggle_dataset import SYMPTOM_TRANSLATION, DISEASE_TRANSLATION


def step1_translate_kaggle():
    """Step 1: Translate Kaggle dataset to Indonesian with structured format."""
    print("\n" + "=" * 60)
    print("STEP 1: Translate Kaggle Dataset")
    print("=" * 60)

    if not os.path.exists(KAGGLE_RAW):
        print(f"❌ Kaggle dataset not found at {KAGGLE_RAW}")
        print("   Please download from: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset")
        return False

    df = pd.read_csv(KAGGLE_RAW)
    print(f"📂 Loaded {len(df)} rows, {df['Disease'].str.strip().nunique()} diseases")

    records = []
    for _, row in df.iterrows():
        # Translate disease
        disease_en = row['Disease'].strip()
        disease_id = DISEASE_TRANSLATION.get(disease_en, disease_en)

        # Collect symptoms (English + Indonesian)
        symptoms_en = []
        symptoms_id = []
        for col in df.columns:
            if col.startswith('Symptom') and pd.notna(row[col]):
                raw = str(row[col]).replace('_', ' ').strip()
                symptoms_en.append(raw)
                symptoms_id.append(SYMPTOM_TRANSLATION.get(raw, raw))

        if symptoms_id:
            records.append({
                'disease_en': disease_en,
                'disease_id': disease_id,
                'symptoms_en': '|'.join(symptoms_en),
                'symptoms_id': '|'.join(symptoms_id),
                'num_symptoms': len(symptoms_id),
            })

    df_out = pd.DataFrame(records)
    df_out.to_csv(KAGGLE_TRANSLATED, index=False)
    print(f"✅ Saved {len(df_out)} translated records to {KAGGLE_TRANSLATED}")
    print(f"   Diseases: {df_out['disease_id'].nunique()}")
    return True


def step2_augment_with_templates():
    """
    Step 2: Generate natural-language complaints using TEMPLATES + variations.
    This creates diverse training data from structured Kaggle symptom lists.
    Falls back from Gemini API if rate limited.
    """
    print("\n" + "=" * 60)
    print("STEP 2: Augment with Natural Language Templates")
    print("=" * 60)

    if not os.path.exists(KAGGLE_TRANSLATED):
        print("❌ Run step 1 first")
        return False

    df = pd.read_csv(KAGGLE_TRANSLATED)

    # Template patterns for various complaint styles
    TEMPLATES = [
        # Patient self-report style
        "Dok, saya mengalami {s1}. Sudah {dur} ini {s2} juga. {extra}",
        "Saya merasa {s1} sejak {dur} lalu. Selain itu ada {s2}. {extra}",
        "Keluhan utama saya {s1}. Disertai {s2} sejak {dur}. {extra}",
        "Badan terasa {s1}, {s2} sudah {dur}. {extra}",
        "Dok, pasien mengeluh {s1} dan {s2}. Keluhan dirasakan sejak {dur}. {extra}",
        # Nurse report style
        "Pasien datang dengan keluhan {s1}, {s2}. Onset {dur}. {extra}",
        "Keluhan: {s1}, disertai {s2}. Sudah berlangsung {dur}. {extra}",
        "Pasien mengeluh {s1} sejak {dur}. Gejala penyerta: {s2}. {extra}",
        # Short style
        "{s1}, {s2}. Sudah {dur}.",
        "Keluhan {s1} dan {s2}, {dur} terakhir.",
        # Detailed style
        "Dok, saya mau konsultasi. Saya {s1} sudah {dur}. Selain itu {s2}. Ada juga {s3}. {extra}",
        "Pasien laki-laki datang dengan keluhan utama {s1} sejak {dur}. Disertai {s2} dan {s3}. {extra}",
        "Pasien perempuan mengeluh {s1}. Keluhan muncul {dur} yang lalu. Gejala tambahan: {s2}, {s3}. {extra}",
    ]

    DURATIONS = [
        "2 hari", "3 hari", "sejak kemarin", "1 minggu", "5 hari",
        "sejak tadi pagi", "2 minggu", "4 hari", "sejak semalam",
        "3 hari ini", "beberapa hari", "1 hari", "sekitar seminggu",
    ]

    EXTRAS = [
        "", "Belum minum obat apapun.", "Sudah minum paracetamol tapi tidak membaik.",
        "Tidak punya riwayat penyakit.", "Ada riwayat maag.",
        "Belum periksa ke dokter sebelumnya.", "Sempat membaik tapi kambuh lagi.",
        "", "", "",  # More empty for variety
    ]

    augmented = []
    for _, row in df.iterrows():
        symptoms = row['symptoms_id'].split('|')
        disease = row['disease_id']

        # Generate 3-5 variations per record
        n_variations = random.randint(3, 5)
        for _ in range(n_variations):
            random.shuffle(symptoms)
            template = random.choice(TEMPLATES)
            dur = random.choice(DURATIONS)
            extra = random.choice(EXTRAS)

            s1 = symptoms[0] if len(symptoms) > 0 else ""
            s2 = symptoms[1] if len(symptoms) > 1 else ""
            s3 = symptoms[2] if len(symptoms) > 2 else symptoms[0]

            text = template.format(s1=s1, s2=s2, s3=s3, dur=dur, extra=extra)
            text = text.replace("  ", " ").strip()

            augmented.append({
                'text': text,
                'label': disease,
                'source': 'kaggle_augmented',
            })

    df_aug = pd.DataFrame(augmented)
    df_aug = df_aug.sample(frac=1, random_state=42).reset_index(drop=True)
    df_aug.to_csv(AUGMENTED_PATH, index=False)

    print(f"✅ Generated {len(df_aug)} augmented records")
    print(f"   Diseases: {df_aug['label'].nunique()}")
    print(f"   Saved to {AUGMENTED_PATH}")
    print(f"\n📋 Sample records:")
    for _, row in df_aug.head(5).iterrows():
        print(f"   [{row['label']}] {row['text'][:80]}...")
    return True


def step3_gemini_augment(n_per_disease=30):
    """
    Step 3: Use Gemini 2.5 Flash Lite to generate highly natural complaints.
    This creates the most diverse and realistic training data.
    """
    print("\n" + "=" * 60)
    print("STEP 3: Gemini 2.5 Flash Lite Augmentation")
    print("=" * 60)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        print("   Skipping Gemini augmentation (template data will be used)")
        return True  # Not fatal

    # Load knowledge base for symptom info
    from knowledge_base import DiseaseKnowledgeBase, DISEASE_DATABASE
    kb = DiseaseKnowledgeBase()
    kb.build_matrix_from_kaggle(KAGGLE_RAW)

    gemini_records = []
    diseases = list(DISEASE_DATABASE.items())

    print(f"🤖 Generating {n_per_disease} complaints per disease ({len(diseases)} diseases)...")

    for i, (disease_id, info) in enumerate(diseases):
        symptoms = kb.get_disease_symptoms(disease_id)
        if not symptoms:
            continue

        symptom_list = ", ".join(symptoms[:6])

        prompt = f"""Buatkan {n_per_disease} contoh kalimat keluhan pasien Indonesia yang mengarah ke penyakit "{disease_id}".

Gejala utama penyakit ini: {symptom_list}

ATURAN:
1. Gunakan bahasa Indonesia sehari-hari (bukan bahasa medis formal)
2. Variasikan gaya: ada yang singkat, ada yang cerita detail
3. Campurkan: kadang pasien sendiri, kadang perawat yang lapor
4. Jangan sebutkan nama penyakitnya di keluhan
5. Setiap keluhan HARUS mengandung minimal 2-3 gejala dari daftar
6. Variasikan durasi keluhan (2 hari, seminggu, dll)

FORMAT: Satu keluhan per baris, tanpa penomoran. Langsung teks keluhan saja."""

        try:
            response = model.generate_content(prompt)
            lines = [l.strip() for l in response.text.strip().split('\n') if l.strip() and len(l.strip()) > 15]

            for line in lines[:n_per_disease]:
                # Remove any numbering
                clean = line.lstrip('0123456789.-) ').strip()
                if clean and len(clean) > 15:
                    gemini_records.append({
                        'text': clean,
                        'label': disease_id,
                        'source': 'gemini_augmented',
                    })

            print(f"   [{i+1}/{len(diseases)}] {disease_id}: {len(lines)} complaints generated")
            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"   ⚠️ Error for {disease_id}: {e}")
            time.sleep(2)

    if gemini_records:
        df_gemini = pd.DataFrame(gemini_records)
        gemini_path = os.path.join(DATA_DIR, "gemini_augmented.csv")
        df_gemini.to_csv(gemini_path, index=False)
        print(f"\n✅ Gemini generated {len(df_gemini)} records → {gemini_path}")
    else:
        print("⚠️ No Gemini records generated")

    return True


def step4_merge_and_split():
    """Step 4: Merge all data sources and create stratified train/val/test splits."""
    print("\n" + "=" * 60)
    print("STEP 4: Merge & Stratified Split")
    print("=" * 60)

    datasets = []

    # 1. Template-augmented Kaggle
    if os.path.exists(AUGMENTED_PATH):
        df = pd.read_csv(AUGMENTED_PATH)
        datasets.append(df)
        print(f"   ✅ Template augmented: {len(df)} records")

    # 2. Gemini-augmented
    gemini_path = os.path.join(DATA_DIR, "gemini_augmented.csv")
    if os.path.exists(gemini_path):
        df = pd.read_csv(gemini_path)
        datasets.append(df)
        print(f"   ✅ Gemini augmented: {len(df)} records")

    # 3. Original Kaggle translated (fallback)
    kaggle_processed = os.path.join(DATA_DIR, "kaggle_dataset.csv")
    if os.path.exists(kaggle_processed):
        df = pd.read_csv(kaggle_processed)
        if 'source' not in df.columns:
            df['source'] = 'kaggle_original'
        datasets.append(df)
        print(f"   ✅ Kaggle original: {len(df)} records")

    if not datasets:
        print("❌ No datasets found to merge!")
        return False

    # Merge
    df_all = pd.concat(datasets, ignore_index=True)
    df_all = df_all.sample(frac=1, random_state=42).reset_index(drop=True)

    # Remove duplicates by text
    df_all = df_all.drop_duplicates(subset=['text'], keep='first')

    print(f"\n📊 Combined dataset: {len(df_all)} records, {df_all['label'].nunique()} diseases")
    print(f"   Sources: {df_all['source'].value_counts().to_dict()}")

    # Stratified Split: 80% train, 10% val, 10% test
    from sklearn.model_selection import train_test_split

    # First split: 80% train, 20% temp
    df_train, df_temp = train_test_split(
        df_all, test_size=0.2, random_state=42, stratify=df_all['label']
    )
    # Second split: 50/50 of temp → 10% val, 10% test
    df_val, df_test = train_test_split(
        df_temp, test_size=0.5, random_state=42, stratify=df_temp['label']
    )

    # Save all
    df_train.to_csv(TRAIN_PATH, index=False)
    df_val.to_csv(VAL_PATH, index=False)
    df_test.to_csv(TEST_PATH, index=False)
    df_all.to_csv(FINAL_DATASET, index=False)

    print(f"\n✅ Splits saved:")
    print(f"   Train: {len(df_train)} → {TRAIN_PATH}")
    print(f"   Val:   {len(df_val)} → {VAL_PATH}")
    print(f"   Test:  {len(df_test)} → {TEST_PATH}")
    print(f"   Full:  {len(df_all)} → {FINAL_DATASET}")

    return True


def main():
    print("╔" + "═" * 58 + "╗")
    print("║  SAPA DATA PIPELINE — Phase 1 (Real Data Only)         ║")
    print("╚" + "═" * 58 + "╝")

    # Step 1: Translate Kaggle
    if not step1_translate_kaggle():
        sys.exit(1)

    # Step 2: Template augmentation (fast, local)
    if not step2_augment_with_templates():
        sys.exit(1)

    # Step 3: Gemini augmentation (API, slower but higher quality)
    step3_gemini_augment(n_per_disease=30)

    # Step 4: Merge everything & split
    if not step4_merge_and_split():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("🎉 PHASE 1 COMPLETE!")
    print("=" * 60)
    print("Next: python knowledge_base.py  (if not already run)")
    print("Then: python hybrid_trainer.py  (Phase 3: Model Training)")


if __name__ == "__main__":
    main()

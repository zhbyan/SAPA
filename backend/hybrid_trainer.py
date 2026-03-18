"""
SAPA Hybrid Trainer — Phase 3: Full Pipeline
Architecture: IndoBERT (Fine-tuned) + TF-IDF + Knowledge Base + PCA + Random Forest (Calibrated)
Target: Top-3 Accuracy ≥80% | ECE < 0.10
"""

import pandas as pd
import numpy as np
import pickle
import os
import sys
import time
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report, accuracy_score, f1_score,
    top_k_accuracy_score
)
from sklearn.model_selection import train_test_split

# ═══ Configuration ═══════════════════════════════════
DATA_DIR = "../data"
TRAIN_PATH = os.path.join(DATA_DIR, "train.csv")
VAL_PATH = os.path.join(DATA_DIR, "val.csv")
TEST_PATH = os.path.join(DATA_DIR, "test.csv")
FALLBACK_PATH = os.path.join(DATA_DIR, "hybrid_dataset.csv")
KB_PATH = os.path.join(DATA_DIR, "knowledge_base.pkl")
MODEL_OUTPUT = os.path.join(DATA_DIR, "sapa_model.pkl")

# Model hyperparameters
TFIDF_MAX_FEATURES = 500
TFIDF_NGRAM = (1, 2)
PCA_COMPONENTS = 256
RF_ESTIMATORS = 300
RF_MAX_DEPTH = 25
RF_MIN_SAMPLES_LEAF = 3

# Try to use IndoBERT (if torch available)
USE_BERT = False
BERT_MODEL = "indolem/indobert-base-uncased"
BERT_DIM = 768

try:
    import torch
    from transformers import AutoTokenizer, AutoModel
    USE_BERT = True
    print("✅ PyTorch + Transformers available → Using IndoBERT embeddings")
except ImportError:
    print("⚠️ PyTorch not available → Using TF-IDF only (no BERT embeddings)")
    print("   To enable BERT: conda install pytorch cpuonly -c pytorch")
    print("   Then: pip install transformers")


class HybridTrainer:
    """
    6-Stage Training Pipeline:
    1. [Optional] Extract IndoBERT embeddings (768-dim)
    2. Extract TF-IDF features (500-dim)
    3. Extract Knowledge Base features (130-dim)
    4. Concatenate + StandardScaler + PCA (→ 256-dim)
    5. Train Random Forest (300 trees, balanced)
    6. Calibrate probabilities (Isotonic Regression)
    """

    def __init__(self):
        print("=" * 60)
        print("SAPA HYBRID TRAINER")
        print("=" * 60)

        # Components
        self.tfidf = TfidfVectorizer(
            max_features=TFIDF_MAX_FEATURES,
            ngram_range=TFIDF_NGRAM,
            sublinear_tf=True,
            min_df=2,
            max_df=0.95,
        )
        self.scaler = StandardScaler()
        self.pca = None  # Will be set based on actual n_features
        self.rf = RandomForestClassifier(
            n_estimators=RF_ESTIMATORS,
            max_features="sqrt",
            max_depth=RF_MAX_DEPTH,
            min_samples_leaf=RF_MIN_SAMPLES_LEAF,
            class_weight="balanced",
            oob_score=True,
            n_jobs=-1,
            random_state=42,
        )
        self.calibrated_rf = None
        self.label_encoder = LabelEncoder()
        self.kb = None

        # BERT components (optional)
        self.bert_tokenizer = None
        self.bert_model = None

    def _load_data(self):
        """Load stratified splits or fallback to single file."""
        if os.path.exists(TRAIN_PATH) and os.path.exists(VAL_PATH) and os.path.exists(TEST_PATH):
            df_train = pd.read_csv(TRAIN_PATH)
            df_val = pd.read_csv(VAL_PATH)
            df_test = pd.read_csv(TEST_PATH)
            print(f"📂 Loaded splits: train={len(df_train)}, val={len(df_val)}, test={len(df_test)}")
        elif os.path.exists(FALLBACK_PATH):
            print(f"⚠️ Using fallback single file: {FALLBACK_PATH}")
            df = pd.read_csv(FALLBACK_PATH)
            df_train, df_temp = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
            df_val, df_test = train_test_split(df_temp, test_size=0.5, random_state=42, stratify=df_temp['label'])
        else:
            raise FileNotFoundError("No dataset found! Run data_manager.py first.")

        # Clean text
        for df in [df_train, df_val, df_test]:
            df['text'] = df['text'].astype(str).str.strip()

        return df_train, df_val, df_test

    def _load_kb(self):
        """Load Knowledge Base."""
        if os.path.exists(KB_PATH):
            from knowledge_base import DiseaseKnowledgeBase
            self.kb = DiseaseKnowledgeBase()
            self.kb.load(KB_PATH)
            print(f"✅ Knowledge Base loaded: {len(self.kb.symptom_names)} symptoms")
            return True
        else:
            print("⚠️ Knowledge Base not found → Skipping KB features")
            return False

    def _extract_bert_embeddings(self, texts, batch_size=32, cache_name=None):
        """Extract IndoBERT CLS embeddings with .npy caching."""
        if not USE_BERT:
            return None

        # Check cache first
        if cache_name:
            cache_path = os.path.join(DATA_DIR, f"bert_cache_{cache_name}.npy")
            if os.path.exists(cache_path):
                cached = np.load(cache_path)
                if cached.shape[0] == len(texts):
                    print(f"   ✅ Loaded BERT cache: {cache_path} ({cached.shape})")
                    return cached
                else:
                    print(f"   ⚠️ Cache size mismatch ({cached.shape[0]} vs {len(texts)}), recomputing...")

        print(f"   Processing {len(texts)} texts with IndoBERT...")

        if self.bert_tokenizer is None:
            print(f"   Loading {BERT_MODEL}...")
            self.bert_tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL)
            self.bert_model = AutoModel.from_pretrained(BERT_MODEL)
            self.bert_model.eval()

        all_embeddings = []
        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                encoded = self.bert_tokenizer(
                    batch, padding=True, truncation=True,
                    max_length=256, return_tensors="pt"
                )
                outputs = self.bert_model(**encoded)
                cls_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
                all_embeddings.append(cls_embeddings)

                if (i // batch_size) % 10 == 0:
                    print(f"   Batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")

        result = np.vstack(all_embeddings)

        # Save cache
        if cache_name:
            cache_path = os.path.join(DATA_DIR, f"bert_cache_{cache_name}.npy")
            np.save(cache_path, result)
            print(f"   💾 Cached BERT embeddings: {cache_path}")

        return result

    def _extract_tfidf(self, texts_train, texts_val, texts_test):
        """Extract TF-IDF features."""
        X_train = self.tfidf.fit_transform(texts_train).toarray()
        X_val = self.tfidf.transform(texts_val).toarray()
        X_test = self.tfidf.transform(texts_test).toarray()
        print(f"   TF-IDF shape: {X_train.shape[1]} features")
        return X_train, X_val, X_test

    def _extract_kb_features(self, texts):
        """Extract Knowledge Base symptom vectors."""
        if self.kb is None:
            return None
        vectors = np.array([self.kb.get_symptom_vector(t) for t in texts])
        print(f"   KB shape: {vectors.shape[1]} features, avg symptoms detected: {vectors.sum(axis=1).mean():.1f}")
        return vectors

    def _concatenate_features(self, *feature_arrays):
        """Concatenate feature arrays, skipping None."""
        valid = [f for f in feature_arrays if f is not None]
        return np.hstack(valid) if valid else None

    def train(self):
        """Run the full 6-stage training pipeline."""
        start_time = time.time()

        # ── Load Data ──
        df_train, df_val, df_test = self._load_data()
        has_kb = self._load_kb()

        texts_train = df_train['text'].tolist()
        texts_val = df_val['text'].tolist()
        texts_test = df_test['text'].tolist()

        # Encode labels
        y_train = self.label_encoder.fit_transform(df_train['label'])
        y_val = self.label_encoder.transform(df_val['label'])
        y_test = self.label_encoder.transform(df_test['label'])
        n_classes = len(self.label_encoder.classes_)
        print(f"\n🏷️ Classes: {n_classes} diseases")

        # ══ STAGE 1: IndoBERT Embeddings (Optional) ══════════
        print(f"\n{'═'*50}")
        print("STAGE 1: IndoBERT Embeddings")
        print(f"{'═'*50}")
        bert_train = self._extract_bert_embeddings(texts_train, cache_name="train")
        bert_val = self._extract_bert_embeddings(texts_val, cache_name="val")
        bert_test = self._extract_bert_embeddings(texts_test, cache_name="test")

        if bert_train is not None:
            print(f"   ✅ BERT embeddings: {bert_train.shape}")
        else:
            print("   ⏭️ Skipped (PyTorch not available)")

        # ══ STAGE 2: TF-IDF Features ═════════════════════════
        print(f"\n{'═'*50}")
        print("STAGE 2: TF-IDF Features")
        print(f"{'═'*50}")
        tfidf_train, tfidf_val, tfidf_test = self._extract_tfidf(texts_train, texts_val, texts_test)

        # ══ STAGE 3: Knowledge Base Features ══════════════════
        print(f"\n{'═'*50}")
        print("STAGE 3: Knowledge Base Features")
        print(f"{'═'*50}")
        if has_kb:
            kb_train = self._extract_kb_features(texts_train)
            kb_val = self._extract_kb_features(texts_val)
            kb_test = self._extract_kb_features(texts_test)
        else:
            kb_train = kb_val = kb_test = None

        # ══ STAGE 4: Concatenate + Scale + PCA ════════════════
        print(f"\n{'═'*50}")
        print("STAGE 4: Feature Concatenation + PCA")
        print(f"{'═'*50}")

        X_train = self._concatenate_features(bert_train, tfidf_train, kb_train)
        X_val = self._concatenate_features(bert_val, tfidf_val, kb_val)
        X_test = self._concatenate_features(bert_test, tfidf_test, kb_test)

        total_features = X_train.shape[1]
        print(f"   Combined features: {total_features}")

        # StandardScaler (WAJIB sebelum PCA)
        X_train = self.scaler.fit_transform(X_train)
        X_val = self.scaler.transform(X_val)
        X_test = self.scaler.transform(X_test)

        # PCA — only if features > target
        pca_target = min(PCA_COMPONENTS, total_features, X_train.shape[0])
        if total_features > pca_target:
            self.pca = PCA(n_components=pca_target, random_state=42)
            X_train = self.pca.fit_transform(X_train)
            X_val = self.pca.transform(X_val)
            X_test = self.pca.transform(X_test)
            variance = self.pca.explained_variance_ratio_.sum()
            print(f"   PCA: {total_features} → {pca_target} ({variance*100:.1f}% variance retained)")
        else:
            print(f"   PCA: Skipped (features={total_features} ≤ target={pca_target})")

        # ══ STAGE 5: Random Forest Training ═══════════════════
        print(f"\n{'═'*50}")
        print(f"STAGE 5: Random Forest ({RF_ESTIMATORS} trees)")
        print(f"{'═'*50}")

        self.rf.fit(X_train, y_train)
        train_acc = accuracy_score(y_train, self.rf.predict(X_train))
        val_acc = accuracy_score(y_val, self.rf.predict(X_val))
        oob = self.rf.oob_score_ if hasattr(self.rf, 'oob_score_') and self.rf.oob_score_ else 0
        print(f"   Train accuracy: {train_acc*100:.1f}%")
        print(f"   Val accuracy:   {val_acc*100:.1f}%")
        print(f"   OOB score:      {oob*100:.1f}%")

        # ══ STAGE 6: Probability Calibration ══════════════════
        print(f"\n{'═'*50}")
        print("STAGE 6: Isotonic Regression Calibration")
        print(f"{'═'*50}")

        try:
            # Try prefit approach (sklearn <1.8)
            self.calibrated_rf = CalibratedClassifierCV(self.rf, method="isotonic", cv="prefit")
            self.calibrated_rf.fit(X_val, y_val)
            print("   ✅ Calibrated with Isotonic Regression (prefit) on validation set")
        except (TypeError, ValueError):
            # sklearn 1.8+ — train calibrated classifier using cross-validation on combined set
            print("   ⚠️ cv='prefit' not supported, using cv=3 with combined train+val data")
            X_cal = np.vstack([X_train, X_val])
            y_cal = np.concatenate([y_train, y_val])
            self.calibrated_rf = CalibratedClassifierCV(
                RandomForestClassifier(
                    n_estimators=RF_ESTIMATORS, max_features="sqrt",
                    max_depth=RF_MAX_DEPTH, min_samples_leaf=RF_MIN_SAMPLES_LEAF,
                    class_weight="balanced", n_jobs=-1, random_state=42,
                ),
                method="isotonic", cv=3
            )
            self.calibrated_rf.fit(X_cal, y_cal)
            print("   ✅ Calibrated with Isotonic Regression (cv=3)")

        # ══ EVALUATION ════════════════════════════════════════
        print(f"\n{'═'*50}")
        print("EVALUATION (on Test Set)")
        print(f"{'═'*50}")

        # Predictions
        y_pred = self.calibrated_rf.predict(X_test)
        y_proba = self.calibrated_rf.predict_proba(X_test)

        # Metrics
        test_acc = accuracy_score(y_test, y_pred)
        f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
        f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)

        # Top-3 accuracy
        if n_classes >= 3:
            top3_acc = top_k_accuracy_score(y_test, y_proba, k=3)
        else:
            top3_acc = test_acc

        # ECE (Expected Calibration Error)
        ece = self._compute_ece(y_test, y_proba, n_bins=10)

        print(f"\n   📊 Results:")
        print(f"   ┌──────────────────────────────┐")
        print(f"   │ Top-1 Accuracy: {test_acc*100:6.2f}%     │")
        print(f"   │ Top-3 Accuracy: {top3_acc*100:6.2f}%     │")
        print(f"   │ F1 (macro):     {f1_macro*100:6.2f}%     │")
        print(f"   │ F1 (weighted):  {f1_weighted*100:6.2f}%     │")
        print(f"   │ ECE:            {ece:.4f}        │")
        print(f"   └──────────────────────────────┘")

        # Detailed classification report
        print(f"\n   Classification Report (Top 10 classes):")
        report = classification_report(y_test, y_pred,
                                       target_names=self.label_encoder.classes_,
                                       zero_division=0, output_dict=True)
        sorted_classes = sorted(
            [(k, v) for k, v in report.items() if isinstance(v, dict) and k not in ['macro avg', 'weighted avg']],
            key=lambda x: x[1]['support'], reverse=True
        )[:10]
        for name, metrics in sorted_classes:
            print(f"   {name[:30]:30s}  P={metrics['precision']:.2f}  R={metrics['recall']:.2f}  F1={metrics['f1-score']:.2f}  N={metrics['support']}")

        # ══ SAVE MODEL ════════════════════════════════════════
        elapsed = time.time() - start_time
        print(f"\n{'═'*50}")
        print(f"SAVING MODEL → {MODEL_OUTPUT}")
        print(f"{'═'*50}")

        model_pack = {
            # Core pipeline
            "tfidf": self.tfidf,
            "scaler": self.scaler,
            "pca": self.pca,
            "rf": self.rf,
            "calibrated_rf": self.calibrated_rf,
            "label_encoder": self.label_encoder,
            # Config
            "use_bert": USE_BERT and bert_train is not None,
            "bert_model_name": BERT_MODEL if USE_BERT else None,
            "feature_dims": {
                "bert": BERT_DIM if USE_BERT and bert_train is not None else 0,
                "tfidf": TFIDF_MAX_FEATURES,
                "kb": len(self.kb.symptom_names) if self.kb else 0,
                "pca_output": pca_target if self.pca else total_features,
            },
            # Metrics
            "metrics": {
                "top1_accuracy": test_acc,
                "top3_accuracy": top3_acc,
                "f1_macro": f1_macro,
                "f1_weighted": f1_weighted,
                "ece": ece,
            },
            "type": "hybrid_tfidf_kb_rf_calibrated",
        }

        os.makedirs(os.path.dirname(MODEL_OUTPUT), exist_ok=True)
        with open(MODEL_OUTPUT, 'wb') as f:
            pickle.dump(model_pack, f)

        size_mb = os.path.getsize(MODEL_OUTPUT) / (1024 * 1024)
        print(f"   ✅ Model saved: {size_mb:.1f} MB")
        print(f"   ⏱️ Total time: {elapsed:.1f}s")
        print(f"\n🎉 TRAINING COMPLETE!")

        return model_pack

    @staticmethod
    def _compute_ece(y_true, y_proba, n_bins=10):
        """Compute Expected Calibration Error."""
        confidences = np.max(y_proba, axis=1)
        predictions = np.argmax(y_proba, axis=1)
        accuracies = (predictions == y_true).astype(float)

        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        for i in range(n_bins):
            mask = (confidences > bin_boundaries[i]) & (confidences <= bin_boundaries[i + 1])
            if mask.sum() > 0:
                bin_acc = accuracies[mask].mean()
                bin_conf = confidences[mask].mean()
                ece += mask.sum() / len(y_true) * abs(bin_acc - bin_conf)

        return ece


if __name__ == "__main__":
    trainer = HybridTrainer()
    trainer.train()

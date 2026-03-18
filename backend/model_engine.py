"""
SAPA Model Engine — Phase 4: Backend Inference
Loads trained pipeline (TF-IDF + KB + PCA + RF Calibrated) and provides predictions.
"""

import pickle
import os
import numpy as np

# Path to the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sapa_model.pkl")
KB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.pkl")

# Fallback to old model
LEGACY_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sapa_hybrid_model.pkl")

# Try to import BERT (optional)
USE_BERT = False
try:
    import torch
    
    # Suppress HuggingFace auto-conversion and advisory warnings
    os.environ["HF_HUB_DISABLE_EXPERIMENTAL_WARNING"] = "1"
    os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
    
    import transformers
    transformers.logging.set_verbosity_error()
    from transformers import AutoTokenizer, AutoModel
    
    USE_BERT = True
except ImportError:
    pass


class SAPAInference:
    """
    SAPA Inference Engine — loads all trained components and provides predictions.
    Supports both new pipeline (TF-IDF + KB + PCA + RF Calibrated) and legacy (TF-IDF + RF).
    """

    def __init__(self):
        self.model_loaded = False
        self.model_pack = None
        self.kb = None
        self.bert_tokenizer = None
        self.bert_model = None

    def load_model(self):
        """Load the trained pipeline."""
        print("🔄 Loading SAPA AI Model...")

        # Try new calibrated model first
        model_path = MODEL_PATH
        if not os.path.exists(model_path):
            model_path = LEGACY_MODEL_PATH

        if not os.path.exists(model_path):
            print(f"⚠️ No model found at {MODEL_PATH} or {LEGACY_MODEL_PATH}")
            return False

        try:
            with open(model_path, 'rb') as f:
                self.model_pack = pickle.load(f)

            model_type = self.model_pack.get("type", "unknown")
            print(f"✅ Model loaded: {model_type}")

            # Load Knowledge Base
            if os.path.exists(KB_PATH):
                from knowledge_base import DiseaseKnowledgeBase
                self.kb = DiseaseKnowledgeBase()
                self.kb.load(KB_PATH)
                print(f"✅ Knowledge Base loaded ({len(self.kb.symptom_names)} symptoms)")

            # Load BERT if model was trained with it
            if self.model_pack.get("use_bert") and USE_BERT:
                bert_name = self.model_pack.get("bert_model_name")
                if bert_name:
                    print(f"🔄 Loading BERT: {bert_name}...")
                    self.bert_tokenizer = AutoTokenizer.from_pretrained(bert_name)
                    self.bert_model = AutoModel.from_pretrained(bert_name)
                    self.bert_model.eval()
                    print(f"✅ BERT loaded")

            if self.model_pack.get("metrics"):
                m = self.model_pack["metrics"]
                print(f"📊 Model metrics: Top-1={m.get('top1_accuracy', 0)*100:.1f}%, "
                      f"Top-3={m.get('top3_accuracy', 0)*100:.1f}%, "
                      f"ECE={m.get('ece', 0):.4f}")

            self.model_loaded = True
            return True

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False

    def predict(self, text: str, top_k: int = 3) -> dict:
        """
        Predict diagnosis from patient complaint text.
        Returns top-k diagnoses with probabilities, ICD-10, symptoms, and confidence level.
        """
        if not self.model_loaded:
            if not self.load_model():
                return {"predictions": [{"diagnosis": "Model Error", "confidence": 0.0}]}

        try:
            model_type = self.model_pack.get("type", "tfidf_rf")

            if model_type == "hybrid_tfidf_kb_rf_calibrated":
                return self._predict_hybrid(text, top_k)
            else:
                return self._predict_legacy(text, top_k)

        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return {"predictions": [], "error": str(e)}

    def _predict_hybrid(self, text: str, top_k: int) -> dict:
        """Prediction using the new calibrated hybrid pipeline."""
        tfidf = self.model_pack["tfidf"]
        scaler = self.model_pack["scaler"]
        pca = self.model_pack.get("pca")
        calibrated_rf = self.model_pack["calibrated_rf"]
        label_encoder = self.model_pack["label_encoder"]
        feature_dims = self.model_pack.get("feature_dims", {})

        # 1. Extract features
        features_list = []

        # BERT embeddings (if available)
        if self.model_pack.get("use_bert") and self.bert_model is not None:
            with torch.no_grad():
                encoded = self.bert_tokenizer(
                    text, return_tensors="pt", padding=True,
                    truncation=True, max_length=256
                )
                outputs = self.bert_model(**encoded)
                bert_embed = outputs.last_hidden_state[:, 0, :].numpy()
                features_list.append(bert_embed)

        # TF-IDF
        tfidf_features = tfidf.transform([text]).toarray()
        features_list.append(tfidf_features)

        # KB features
        if self.kb and feature_dims.get("kb", 0) > 0:
            kb_vec = self.kb.get_symptom_vector(text).reshape(1, -1)
            features_list.append(kb_vec)

        # Concatenate
        features = np.hstack(features_list)

        # Scale
        features = scaler.transform(features)

        # PCA
        if pca is not None:
            features = pca.transform(features)

        # Predict
        probs = calibrated_rf.predict_proba(features)[0]
        top_indices = np.argsort(probs)[::-1][:top_k]

        # Build results
        predictions = []
        for rank, idx in enumerate(top_indices, 1):
            score = float(probs[idx])
            disease_name = label_encoder.inverse_transform([idx])[0]

            # Get ICD-10 and symptoms from KB
            icd10 = "—"
            symptoms = []
            if self.kb:
                icd10 = self.kb.get_icd10(disease_name)
                symptoms = self.kb.get_disease_symptoms(disease_name)[:5]

            # Confidence level
            if score >= 0.6:
                confidence_level = "TINGGI"
            elif score >= 0.3:
                confidence_level = "SEDANG"
            else:
                confidence_level = "RENDAH"

            predictions.append({
                "rank": rank,
                "disease": disease_name,
                "probability": round(score * 100, 1),
                "icd10": icd10,
                "confidence": confidence_level,
                "related_symptoms": symptoms,
            })

        # Extract detected symptoms
        detected_symptoms = self.kb.extract_symptoms(text) if self.kb else []

        return {
            "predictions": predictions,
            "detected_symptoms": detected_symptoms,
            "soap_subjective": text,
            "model_type": "hybrid_calibrated",
        }

    def _predict_legacy(self, text: str, top_k: int) -> dict:
        """Fallback prediction using old TF-IDF + RF model."""
        classifier = self.model_pack["classifier"]
        vectorizer = self.model_pack["vectorizer"]
        labels = self.model_pack["labels"]

        features = vectorizer.transform([text])
        probs = classifier.predict_proba(features)[0]
        top_indices = np.argsort(probs)[::-1][:top_k]

        predictions = []
        for rank, idx in enumerate(top_indices, 1):
            score = float(probs[idx])
            disease_name = labels[idx]
            icd10 = self.kb.get_icd10(disease_name) if self.kb else "—"
            predictions.append({
                "rank": rank,
                "disease": disease_name,
                "probability": round(score * 100, 1),
                "icd10": icd10,
                "confidence": "TINGGI" if score >= 0.6 else ("SEDANG" if score >= 0.3 else "RENDAH"),
            })

        return {
            "predictions": predictions,
            "soap_subjective": text,
            "model_type": "legacy_tfidf_rf",
        }


# Backward compatibility alias
SapaModel = SAPAInference


if __name__ == "__main__":
    engine = SAPAInference()
    engine.load_model()
    result = engine.predict("Saya demam tinggi sejak 3 hari lalu, disertai mual dan bintik merah di badan")
    print("\n🔍 Prediction Result:")
    for pred in result.get("predictions", []):
        print(f"  {pred['rank']}. {pred['disease']} ({pred['probability']}%) — ICD-10: {pred['icd10']} [{pred['confidence']}]")
    print(f"  Detected symptoms: {result.get('detected_symptoms', [])}")

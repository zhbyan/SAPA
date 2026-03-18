"""Quick test: verify model metrics and test predictions."""
import pickle, os

model_path = "../data/sapa_model.pkl"
with open(model_path, 'rb') as f:
    m = pickle.load(f)

print("Model Type:", m.get("type"))
print("Use BERT:", m.get("use_bert"))
print("BERT Model:", m.get("bert_model_name"))
print()
print("Feature Dims:", m.get("feature_dims"))
print()
if m.get("metrics"):
    metrics = m["metrics"]
    print("=== EVALUATION METRICS ===")
    print(f"  Top-1 Accuracy: {metrics['top1_accuracy']*100:.2f}%")
    print(f"  Top-3 Accuracy: {metrics['top3_accuracy']*100:.2f}%")
    print(f"  F1 (macro):     {metrics['f1_macro']*100:.2f}%")
    print(f"  F1 (weighted):  {metrics['f1_weighted']*100:.2f}%")
    print(f"  ECE:            {metrics['ece']:.4f}")
print()
sz = os.path.getsize(model_path) / 1024 / 1024
print(f"Model size: {sz:.1f} MB")
n = len(m["label_encoder"].classes_)
print(f"Labels: {n} diseases")

# Test full inference via model_engine
print("\n=== INFERENCE TEST ===")
from model_engine import SAPAInference
engine = SAPAInference()
engine.load_model()

tests = [
    "Saya demam tinggi sejak 3 hari lalu, disertai mual dan bintik merah di badan",
    "Dok, sudah 2 hari ini perut saya sakit, mual, dan diare terus",
    "Pasien mengeluh sakit kepala sebelah, mual, dan sensitif terhadap cahaya",
]
for text in tests:
    result = engine.predict(text)
    print(f"\nInput: {text[:60]}...")
    for pred in result.get("predictions", []):
        print(f"  {pred['rank']}. {pred['disease']} ({pred['probability']}%) — ICD-10: {pred['icd10']} [{pred['confidence']}]")
    sym = result.get("detected_symptoms", [])
    if sym:
        print(f"  Symptoms: {sym}")

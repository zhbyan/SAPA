"""
SAPA API — FastAPI Backend
Endpoints:
  - /predict  — ML-based diagnosis prediction
  - /chat     — RASA AI chat (Gemini 2.5 Flash Lite)
  - /chat/generate-report — Generate medical report from chat session
  - /health   — Server health check
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
import os

# Suppress HuggingFace auto-conversion and advisory warnings globally
os.environ["HF_HUB_DISABLE_EXPERIMENTAL_WARNING"] = "1"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"  # Forces transformers to only use local cache, stopping the auto-conversion thread
# ═══ App Setup ═══════════════════════════════════════
app = FastAPI(
    title="SAPA API",
    description="Sistem Asistensi Pra-Asesmen Klinis — AI-Powered Clinical Decision Support",
    version="2.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══ Load Engines ════════════════════════════════════
from model_engine import SAPAInference

model_engine = SAPAInference()
rasa_engine = None  # Lazy-loaded

try:
    model_engine.load_model()
except Exception as e:
    print(f"⚠️ Model not loaded: {e}")

def get_rasa():
    """Lazy-load RASA engine."""
    global rasa_engine
    if rasa_engine is None:
        try:
            from llm_engine import RASAEngine
            rasa_engine = RASAEngine()
        except Exception as e:
            print(f"⚠️ RASA engine error: {e}")
            raise HTTPException(status_code=503, detail=f"RASA engine not available: {e}")
    return rasa_engine


# ═══ Request/Response Models ═════════════════════════

class PredictRequest(BaseModel):
    text: str = Field(..., description="Patient complaint text")
    top_k: int = Field(3, description="Number of top predictions")

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Chat session ID")
    message: str = Field(..., description="Message from nakes")
    nakes_name: Optional[str] = Field("Kak", description="Name of the nurse")

class ReportRequest(BaseModel):
    session_id: str = Field(..., description="Chat session ID")


# ═══ Endpoints ═══════════════════════════════════════

@app.get("/")
def root():
    return {
        "service": "SAPA API",
        "version": "2.0.0",
        "status": "running",
        "model_loaded": model_engine.model_loaded,
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model_engine.model_loaded,
        "rasa_available": rasa_engine is not None,
    }


# ─── Prediction Endpoint ────────────────────────────

@app.post("/predict")
def predict(request: PredictRequest):
    """Predict diagnosis from patient complaint text using ML pipeline."""
    if not model_engine.model_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded. Run hybrid_trainer.py first.")

    result = model_engine.predict(request.text, top_k=request.top_k)
    return result


# ─── Chat Endpoints (RASA) ──────────────────────────

@app.post("/chat")
def chat(request: ChatRequest):
    """Send a message to RASA AI chat assistant."""
    engine = get_rasa()

    # Check if session exists, create if not
    session = engine.get_session(request.session_id)
    if session is None:
        engine.create_session(request.session_id, request.nakes_name)

    result = engine.send_message(request.session_id, request.message)
    return result


@app.post("/chat/create")
def create_chat(request: ChatRequest):
    """Create a new RASA chat session."""
    engine = get_rasa()
    result = engine.create_session(request.session_id, request.nakes_name)
    return result


@app.post("/chat/generate-report")
def generate_report(request: ReportRequest):
    """Generate medical report from chat session data."""
    engine = get_rasa()
    result = engine.generate_report(request.session_id)
    return result


@app.get("/chat/{session_id}")
def get_chat_session(session_id: str):
    """Get chat session data including field status and history."""
    engine = get_rasa()
    session = engine.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


# ═══ Run ═════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

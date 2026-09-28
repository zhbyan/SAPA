"""
SAPA LLM Engine — Gemini 2.0 Flash with RASA Persona
Menggunakan Gemini REST API via `requests` (tanpa google-generativeai SDK).
"""

import json
import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ═══ Configuration ═══════════════════════════════════
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-1.5-flash"

def _gemini_url() -> str:
    return (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )

# Required anamnesis fields
REQUIRED_FIELDS = [
    "keluhan_utama",
    "durasi",
    "lokasi_keluhan",
    "keparahan",
    "gejala_penyerta",
    "riwayat_penyakit",
    "riwayat_alergi",
]

OPTIONAL_FIELDS = [
    "obat_dikonsumsi",
    "riwayat_keluarga",
    "tanda_vital",
]

# ═══ RASA System Prompt ══════════════════════════════
RASA_SYSTEM_PROMPT = """Kamu adalah RASA (Rekan Asistensi SAPA), asisten klinis AI yang membantu
tenaga kesehatan (nakes) mengumpulkan data anamnesis pasien melalui percakapan.

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
3. Jika nakes sudah menyebutkan beberapa info sekaligus, JANGAN tanya ulang — langsung lanjut ke field yang belum
4. Setelah setiap jawaban, konfirmasi singkat + lanjut pertanyaan berikutnya
5. Jika jawaban ambigu, minta klarifikasi dengan sopan
6. Jika nakes bilang "tidak tahu" untuk field wajib, catat "Tidak diketahui" dan lanjut

## ATURAN ANALISIS
- HANYA hasilkan analisis setelah SEMUA 7 FIELD WAJIB terkumpul
- Saat semua field terpenuhi, tanyakan: "Kak, data anamnesis sudah lengkap. Mau saya buatkan analisisnya sekarang?"
- Jika nakes setuju, hasilkan analisis dengan format di bawah

## ATURAN KEAMANAN
- JANGAN pernah meresepkan obat
- JANGAN pernah bilang "Anda pasti menderita X"
- Selalu gunakan frasa: "kemungkinan", "perlu diperiksa lebih lanjut"
- Jika keluhan darurat (nyeri dada kiri, sesak berat, pendarahan hebat), LANGSUNG sarankan rujuk IGD
- Tolak pertanyaan di luar konteks medis dengan sopan

## FORMAT RESPONS (SANGAT PENTING!)
Kamu HARUS SELALU merespons HANYA dengan JSON valid.
JANGAN tambahkan markdown ```json. Hasilkan JSON murni:

{
    "reply": "Baik Kak, sudah saya catat. Sejak kapan pasien merasakannya?",
    "field_updates": {
        "keluhan_utama": "Sakit perut"
    },
    "is_complete": false,
    "analysis": null
}

Jika semua field sudah lengkap DAN nakes meminta analisis:
{
    "reply": "📋 RESUME MEDIS...",
    "field_updates": {},
    "is_complete": true,
    "analysis": {
        "resume_medis": "...",
        "diagnoses": [
            {"name": "...", "icd10": "...", "probability": "Tinggi/Sedang/Rendah", "reasoning": "..."}
        ],
        "saran_pemeriksaan": ["...", "..."],
        "disclaimer": "Hasil bersifat indikatif. Keputusan klinis tetap di tangan dokter."
    }
}
"""


def _call_gemini(history: list[dict], temperature: float = 0.2) -> str:
    """
    Call Gemini REST API. Retries up to 3x on 503 (overloaded) with backoff.
    """
    payload = {
        "system_instruction": {
            "parts": [{"text": RASA_SYSTEM_PROMPT}]
        },
        "contents": history,
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
        },
    }

    max_retries = 3
    for attempt in range(max_retries):
        resp = requests.post(
            _gemini_url(),
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )

        if resp.status_code == 200:
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        if resp.status_code == 503 and attempt < max_retries - 1:
            wait = 2 ** attempt  # 1s, 2s
            print(f"⚠️  Gemini 503 overloaded, retry {attempt + 1}/{max_retries - 1} in {wait}s...")
            time.sleep(wait)
            continue

        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text[:300]}")

    raise RuntimeError("Gemini API failed after max retries")


class RASAEngine:
    """
    RASA (Rekan Asistensi SAPA) - Gemini REST-powered clinical assistant.
    Manages chat sessions and field collection for patient anamnesis.
    """

    def __init__(self):
        if not GEMINI_API_KEY:
            print("⚠️  GEMINI_API_KEY not set in .env!")
        print(f"✅ RASA Engine initialized (model: {GEMINI_MODEL})")
        self.sessions: dict = {}

    def create_session(self, session_id: str, nakes_name: str = "Kak") -> dict:
        """Create a new chat session."""
        welcome = (
            f"Halo, {nakes_name}! 👋 Saya RASA, asisten klinis SAPA.\n\n"
            "Silakan ceritakan keluhan utama pasien yang akan diperiksa ya."
        )

        self.sessions[session_id] = {
            "nakes_name": nakes_name,
            "fields": {f: None for f in REQUIRED_FIELDS},
            "optional_fields": {f: None for f in OPTIONAL_FIELDS},
            # Gemini REST history format
            "gemini_history": [
                {"role": "model", "parts": [{"text": welcome}]},
            ],
            "history": [
                {"role": "ai", "text": welcome, "timestamp": time.time()}
            ],
            "is_complete": False,
        }

        return {
            "reply": welcome,
            "field_status": self._get_field_status(session_id),
            "is_complete": False,
        }

    def send_message(self, session_id: str, message: str) -> dict:
        """Send a message to RASA and get response."""
        if session_id not in self.sessions:
            return self.create_session(session_id)

        session = self.sessions[session_id]

        # Add user message to UI history
        session["history"].append({
            "role": "user",
            "text": message,
            "timestamp": time.time(),
        })

        try:
            # Build field context
            filled_fields = []
            missing_fields = []
            for field, value in session["fields"].items():
                if value:
                    filled_fields.append(f"- {field}: ✅ {value}")
                else:
                    missing_fields.append(field)

            field_context = "\n\n[SISTEM] STATUS FIELD SAAT INI:\n"
            field_context += "\n".join(filled_fields) if filled_fields else "(belum ada)"
            field_context += "\n"

            if missing_fields:
                field_context += (
                    f"\n⚠️ FIELD BELUM TERISI ({len(missing_fields)} tersisa): "
                    f"{', '.join(missing_fields)}\n"
                    f"INSTRUKSI KERAS: Tanyakan '{missing_fields[0]}' di respons berikutnya. "
                    f"Jika nakes sudah menjawabnya di pesan ini, update field_updates "
                    f"lalu tanyakan: "
                    f"{missing_fields[1] if len(missing_fields) > 1 else 'SELESAI'}."
                )
            else:
                field_context += (
                    "\n✅ SEMUA 7 FIELD WAJIB TERISI! "
                    "Informasikan ke nakes bahwa data lengkap dan bisa klik 'Buat Laporan'."
                )
            field_context += "\nRespond HANYA dengan JSON murni."

            full_message = message + field_context

            # Append user turn to Gemini history
            session["gemini_history"].append({
                "role": "user",
                "parts": [{"text": full_message}],
            })

            # Call Gemini REST API
            response_text = _call_gemini(session["gemini_history"])

            # Append model reply to history
            session["gemini_history"].append({
                "role": "model",
                "parts": [{"text": response_text}],
            })

            # Parse JSON
            parsed = self._parse_response(response_text)

            # Update fields
            if parsed.get("field_updates"):
                for field, value in parsed["field_updates"].items():
                    if field in session["fields"]:
                        session["fields"][field] = value
                    elif field in session["optional_fields"]:
                        session["optional_fields"][field] = value

            # Check completeness
            is_complete = all(v is not None for v in session["fields"].values())
            session["is_complete"] = is_complete

            reply = parsed.get("reply", "Maaf, format respons salah. Silakan ulangi.")

            session["history"].append({
                "role": "ai",
                "text": reply,
                "timestamp": time.time(),
            })

            return {
                "reply": reply,
                "field_status": self._get_field_status(session_id),
                "is_complete": is_complete,
                "analysis": parsed.get("analysis"),
            }

        except Exception as e:
            # Roll back the user message from gemini_history on error
            if session["gemini_history"] and session["gemini_history"][-1]["role"] == "user":
                session["gemini_history"].pop()

            error_msg = f"Maaf Kak, ada gangguan sementara 🙏 Bisa diulang ya.\n(Error: {str(e)[:150]})"
            return {
                "reply": error_msg,
                "field_status": self._get_field_status(session_id),
                "is_complete": False,
                "error": str(e),
            }

    def generate_report(self, session_id: str) -> dict:
        """Generate a full medical report from collected data."""
        if session_id not in self.sessions:
            return {"error": "Session not found"}

        session = self.sessions[session_id]

        # Auto-fill empty required fields
        for field, value in session["fields"].items():
            if value is None:
                session["fields"][field] = "Tidak diketahui"
        session["is_complete"] = True

        prompt = (
            "Kak, tolong buatkan analisis lengkap berdasarkan semua data yang sudah terkumpul. "
            "Berikan resume medis, diagnosis awal (top-3 dengan ICD-10 dan reasoning), "
            "dan saran pemeriksaan lanjutan."
        )
        return self.send_message(session_id, prompt)

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data."""
        if session_id not in self.sessions:
            return None
        session = self.sessions[session_id]
        return {
            "fields": session["fields"],
            "optional_fields": session["optional_fields"],
            "history": session["history"],
            "is_complete": session["is_complete"],
        }

    def _get_field_status(self, session_id: str) -> dict:
        session = self.sessions[session_id]
        total  = len(REQUIRED_FIELDS)
        filled = sum(1 for v in session["fields"].values() if v is not None)
        return {
            "required":   session["fields"],
            "optional":   session["optional_fields"],
            "progress":   f"{filled}/{total}",
            "percentage": int(filled / total * 100),
        }

    @staticmethod
    def _parse_response(text: str) -> dict:
        """Parse JSON response. Falls back gracefully."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        import re
        match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        return {"reply": text, "field_updates": {}, "is_complete": False}


# ═══ Standalone test ═════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("RASA Engine Test — Gemini 2.0 Flash (REST API)")
    print("=" * 60)

    engine = RASAEngine()
    result = engine.create_session("test-001", "Alex")
    print(f"\n🤖 RASA: {result['reply']}")

    messages = [
        "Mual ada, muntah 2x isi makanan. Konstipasi belum BAB 2 hari.",
        "Sejak kemarin sore",
        "Ulu hati, kadang ke kanan bawah juga",
        "Sekitar 6",
        "Suhu 37.8, agak hangat. Tidak ada keluhan lain",
        "Riwayat maag, alergi tidak ada",
    ]

    for msg in messages:
        print(f"\n👤 Nakes: {msg}")
        result = engine.send_message("test-001", msg)
        print(f"🤖 RASA: {result['reply'][:200]}...")
        print(f"   Fields: {result['field_status']['progress']}")
        if result.get("is_complete"):
            print("\n✅ Semua field terkumpul!")
            break
        time.sleep(0.3)

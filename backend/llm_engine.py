"""
SAPA LLM Engine — Phase 6: Gemini 2.5 Flash Lite with RASA Persona
AI Chat Agent untuk pengumpulan data anamnesis pasien via percakapan.
"""

import json
import os
import time
from typing import Optional
from groq import Groq

# ═══ Configuration ═══════════════════════════════════
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

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
2. Tanyakan field berikutnya SATU PER SATU berdasarkan konteks (jangan bombardir pertanyaan)
3. Jika nakes sudah menyebutkan beberapa info sekaligus, JANGAN tanya ulang yang sudah disebutkan — langsung lanjut ke field yang belum
4. Setelah setiap jawaban, konfirmasi singkat + lanjut pertanyaan berikutnya
5. Jika jawaban ambigu, minta klarifikasi dengan sopan
6. Jika nakes bilang "tidak tahu" untuk field wajib, catat sebagai "Tidak diketahui" dan lanjut (jangan memaksa)

## ATURAN ANALISIS
- HANYA hasilkan analisis setelah SEMUA 7 FIELD WAJIB terkumpul
- Saat semua field terpenuhi, tanyakan: "Kak, data anamnesis sudah lengkap. Mau saya buatkan analisisnya sekarang?"
- Jika nakes setuju, hasilkan analisis dengan format di bawah

## ATURAN KEAMANAN
- JANGAN pernah meresepkan obat
- JANGAN pernah bilang "Anda pasti menderita X"
- Selalu gunakan frasa: "kemungkinan", "perlu diperiksa lebih lanjut"
- Jika keluhan darurat (nyeri dada kiri, sesak berat, pendarahan hebat), LANGSUNG sarankan: "Kak, ini PERLU PENANGANAN SEGERA. Mohon segera rujuk ke IGD."
- Tolak pertanyaan di luar konteks medis dengan sopan

## FORMAT RESPONS (SANGAT PENTING!)
Kamu HARUS SELALU merespons HANYA dengan JSON valid. 
Jangan tambahkan format markdown ````json` pada awal atau akhir, JANGAN MENAMBAH TEKS APAPUN SEBELUM/SESUDAH JSON.
Hasilkan JSON murni seperti contoh berikut:

{
    "reply": "Baik Kak, sudah saya catat keluhannya. Sejak kapan pasien merasakannya?",
    "field_updates": {
        "keluhan_utama": "Sakit perut"
    },
    "is_complete": false,
    "analysis": null
}

Jika semua field sudah lengkap DAN nakes meminta analisis:
{
    "reply": "📋 RESUME MEDIS\\nPasien mengeluh sakit perut sejak 3 hari lalu...",
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


class RASAEngine:
    """
    RASA (Rekan Asistensi SAPA) - Groq-powered clinical assistant.
    Manages chat sessions and field collection for patient anamnesis.
    """

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.sessions = {}  # session_id -> {llm_history, fields, history}
        print(f"✅ RASA Engine initialized (model: {GROQ_MODEL})")

    def create_session(self, session_id: str, nakes_name: str = "Kak") -> dict:
        """Create a new chat session."""
        welcome = f"Halo, {nakes_name}! 👋 Saya RASA, asisten klinis SAPA.\n\nSilakan ceritakan keluhan utama pasien yang akan diperiksa ya."
        
        self.sessions[session_id] = {
            "nakes_name": nakes_name,
            "fields": {f: None for f in REQUIRED_FIELDS},
            "optional_fields": {f: None for f in OPTIONAL_FIELDS},
            "llm_history": [
                {"role": "system", "content": RASA_SYSTEM_PROMPT},
                {"role": "assistant", "content": welcome}
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
            # Build context about collected fields — aggressive enforcement
            filled_fields = []
            missing_fields = []
            for field, value in session["fields"].items():
                if value:
                    filled_fields.append(f"- {field}: ✅ {value}")
                else:
                    missing_fields.append(field)
            
            field_context = f"\n\n[SISTEM] STATUS FIELD SAAT INI:\n"
            field_context += "\n".join(filled_fields) if filled_fields else ""
            field_context += "\n"
            
            if missing_fields:
                field_context += f"\n⚠️ FIELD YANG BELUM TERISI ({len(missing_fields)} tersisa): {', '.join(missing_fields)}\n"
                field_context += f"INSTRUKSI KERAS: Kamu HARUS bertanya tentang '{missing_fields[0]}' di respons berikutnya. "
                field_context += f"JANGAN membahas topik lain sampai field ini terisi. "
                field_context += f"Jika nakes sudah menjawab field ini di pesan sekarang, update field_updates lalu tanyakan field berikutnya: {missing_fields[1] if len(missing_fields) > 1 else 'SELESAI'}."
            else:
                field_context += "\n✅ SEMUA 7 FIELD WAJIB SUDAH TERISI! Sampaikan ke nakes bahwa data sudah lengkap dan mereka bisa klik tombol 'Buat Laporan'."
            
            field_context += "\nPastikan respond Anda HANYA berupa JSON tanpa penjelasan tambahan."

            # Send to Groq
            full_message = message + field_context
            session["llm_history"].append({"role": "user", "content": full_message})

            completion = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=session["llm_history"],
                temperature=0.2, # Lower temperature for stricter JSON format
                response_format={"type": "json_object"} # Force JSON mode on Groq
            )
            
            response_text = completion.choices[0].message.content.strip()

            # Add raw response to LLM history so it remembers what it said
            session["llm_history"].append({"role": "assistant", "content": response_text})

            # Parse JSON response
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

            # Add AI response to UI history
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
            error_msg = f"Maaf Kak, ada gangguan sementara 🙏 Bisa diulang ya.\n(Error: {str(e)[:100]})"
            
            # Remove the last user message from llm_history if it caused an error
            if session["llm_history"][-1]["role"] == "user":
                session["llm_history"].pop()
                
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

        # Auto-fill empty required fields with fallback value
        for field, value in session["fields"].items():
            if value is None:
                session["fields"][field] = "Tidak diketahui"

        session["is_complete"] = True

        # Ask RASA to generate analysis
        prompt = "Kak, tolong buatkan analisis lengkap berdasarkan semua data yang sudah terkumpul. Berikan resume medis, diagnosis awal (top-3 dengan ICD-10 dan reasoning), dan saran pemeriksaan lanjutan."

        result = self.send_message(session_id, prompt)
        return result

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
        """Get current status of all fields."""
        session = self.sessions[session_id]
        total = len(REQUIRED_FIELDS)
        filled = sum(1 for v in session["fields"].values() if v is not None)
        return {
            "required": session["fields"],
            "optional": session["optional_fields"],
            "progress": f"{filled}/{total}",
            "percentage": int(filled / total * 100),
        }

    @staticmethod
    def _parse_response(text: str) -> dict:
        """Parse JSON response from LLM. Falls back to generating a blank one."""
        # Try direct JSON parse
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code block
        import re
        json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass

        # Parse failed, fallback
        return {"reply": text, "field_updates": {}, "is_complete": False}


# ═══ Standalone test ═════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("RASA Engine Test")
    print("=" * 60)

    engine = RASAEngine()

    # Create session
    result = engine.create_session("test-001", "Alex")
    print(f"\n🤖 RASA: {result['reply']}")
    print(f"   Fields: {result['field_status']['progress']}")

    # Simulate conversation
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

        if result.get('is_complete'):
            print("\n✅ All fields collected! Generating report...")
            report = engine.generate_report("test-001")
            print(f"📋 Report: {report.get('reply', '')[:300]}...")
            break

        time.sleep(1)  # Rate limiting

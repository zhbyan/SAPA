"""
SAPA Knowledge Base — Disease/Symptom Database + ICD-10 Codes
Sumber data: Kaggle Disease-Symptom Dataset (translated to Indonesian)
"""

import json
import os
import pickle
import re
import numpy as np

# ══════════════════════════════════════════════════════
# DISEASE DATABASE: 41 penyakit + ICD-10 + sinonim
# ══════════════════════════════════════════════════════

DISEASE_DATABASE = {
    "Demam Berdarah Dengue (DBD)": {
        "en": "Dengue", "icd10": "A90",
        "synonyms": ["DBD", "Demam Berdarah", "Dengue"],
    },
    "Tifus (Demam Tifoid)": {
        "en": "Typhoid", "icd10": "A01.0",
        "synonyms": ["Tifus", "Tipes", "Demam Tifoid", "Typhoid"],
    },
    "TBC (Tuberkulosis)": {
        "en": "Tuberculosis", "icd10": "A15.0",
        "synonyms": ["TBC", "TB", "Tuberkulosis", "Flek Paru"],
    },
    "ISPA/Influenza": {
        "en": "Common Cold", "icd10": "J06.9",
        "synonyms": ["ISPA", "Influenza", "Flu", "Pilek", "Masuk Angin"],
    },
    "Pneumonia (Radang Paru)": {
        "en": "Pneumonia", "icd10": "J18.9",
        "synonyms": ["Pneumonia", "Radang Paru", "Infeksi Paru"],
    },
    "Diabetes Melitus": {
        "en": "Diabetes", "icd10": "E11.9",
        "synonyms": ["Diabetes", "DM", "Kencing Manis", "Gula Darah Tinggi"],
    },
    "Hipertensi": {
        "en": "Hypertension", "icd10": "I10",
        "synonyms": ["Hipertensi", "Darah Tinggi", "Tensi Tinggi"],
    },
    "Migrain": {
        "en": "Migraine", "icd10": "G43.9",
        "synonyms": ["Migrain", "Migraine", "Sakit Kepala Sebelah"],
    },
    "Malaria": {
        "en": "Malaria", "icd10": "B54",
        "synonyms": ["Malaria"],
    },
    "Cacar Air": {
        "en": "Chicken pox", "icd10": "B01.9",
        "synonyms": ["Cacar Air", "Varicella", "Cacar"],
    },
    "Asma Bronkial": {
        "en": "Bronchial Asthma", "icd10": "J45.9",
        "synonyms": ["Asma", "Asthma", "Sesak Napas Kambuhan"],
    },
    "Gastroenteritis (Muntaber)": {
        "en": "Gastroenteritis", "icd10": "A09",
        "synonyms": ["Gastroenteritis", "Muntaber", "GE"],
    },
    "Reaksi Obat/Alergi": {
        "en": "Drug Reaction", "icd10": "T88.7",
        "synonyms": ["Alergi Obat", "Reaksi Obat", "Drug Allergy"],
    },
    "Gastritis (Maag)": {
        "en": "Peptic ulcer diseae", "icd10": "K29.7",
        "synonyms": ["Maag", "Gastritis", "Sakit Lambung", "Asam Lambung"],
    },
    "Penyakit Kuning": {
        "en": "Jaundice", "icd10": "R17",
        "synonyms": ["Penyakit Kuning", "Jaundice", "Ikterus"],
    },
    "Infeksi Jamur": {
        "en": "Fungal infection", "icd10": "B35.9",
        "synonyms": ["Infeksi Jamur", "Jamur Kulit", "Panu", "Kurap"],
    },
    "Alergi": {
        "en": "Allergy", "icd10": "T78.4",
        "synonyms": ["Alergi", "Reaksi Alergi"],
    },
    "GERD (Asam Lambung)": {
        "en": "GERD", "icd10": "K21.0",
        "synonyms": ["GERD", "Asam Lambung", "Refluks"],
    },
    "Kolestasis Kronis": {
        "en": "Chronic cholestasis", "icd10": "K83.1",
        "synonyms": ["Kolestasis"],
    },
    "Hepatitis A": {
        "en": "Hepatitis A", "icd10": "B15.9",
        "synonyms": ["Hepatitis A", "Hep A"],
    },
    "Hepatitis B": {
        "en": "Hepatitis B", "icd10": "B16.9",
        "synonyms": ["Hepatitis B", "Hep B"],
    },
    "Hepatitis C": {
        "en": "Hepatitis C", "icd10": "B17.1",
        "synonyms": ["Hepatitis C", "Hep C"],
    },
    "Hepatitis D": {
        "en": "Hepatitis D", "icd10": "B17.0",
        "synonyms": ["Hepatitis D"],
    },
    "Hepatitis E": {
        "en": "Hepatitis E", "icd10": "B17.2",
        "synonyms": ["Hepatitis E"],
    },
    "Hepatitis Alkoholik": {
        "en": "Alcoholic hepatitis", "icd10": "K70.1",
        "synonyms": ["Hepatitis Alkohol"],
    },
    "HIV/AIDS": {
        "en": "AIDS", "icd10": "B20",
        "synonyms": ["HIV", "AIDS", "HIV/AIDS"],
    },
    "Infeksi Saluran Kemih": {
        "en": "Urinary tract infection", "icd10": "N39.0",
        "synonyms": ["ISK", "Infeksi Saluran Kemih", "Anyang-anyangan"],
    },
    "Psoriasis": {
        "en": "Psoriasis", "icd10": "L40.9",
        "synonyms": ["Psoriasis"],
    },
    "Impetigo": {
        "en": "Impetigo", "icd10": "L01.0",
        "synonyms": ["Impetigo"],
    },
    "Jerawat": {
        "en": "Acne", "icd10": "L70.0",
        "synonyms": ["Jerawat", "Acne", "Berjerawat"],
    },
    "Wasir/Ambeien": {
        "en": "Dimorphic hemmorhoids(piles)", "icd10": "K64.9",
        "synonyms": ["Wasir", "Ambeien", "Hemorrhoid"],
    },
    "Saraf Leher Terjepit": {
        "en": "Cervical spondylosis", "icd10": "M47.8",
        "synonyms": ["Saraf Terjepit", "Cervical Spondylosis"],
    },
    "Hipertiroid": {
        "en": "Hyperthyroidism", "icd10": "E05.9",
        "synonyms": ["Hipertiroid", "Tiroid Overaktif"],
    },
    "Hipotiroid": {
        "en": "Hypothyroidism", "icd10": "E03.9",
        "synonyms": ["Hipotiroid", "Tiroid Kurang Aktif"],
    },
    "Hipoglikemia (Gula Darah Rendah)": {
        "en": "Hypoglycemia", "icd10": "E16.2",
        "synonyms": ["Hipoglikemia", "Gula Darah Rendah"],
    },
    "Osteoartritis": {
        "en": "Osteoarthristis", "icd10": "M19.9",
        "synonyms": ["Osteoartritis", "OA", "Pengapuran Sendi"],
    },
    "Radang Sendi": {
        "en": "Arthritis", "icd10": "M13.9",
        "synonyms": ["Radang Sendi", "Artritis", "Arthritis"],
    },
    "Vertigo": {
        "en": "(vertigo) Paroymsal  Positional Vertigo", "icd10": "H81.1",
        "synonyms": ["Vertigo", "BPPV", "Pusing Berputar"],
    },
    "Varises": {
        "en": "Varicose veins", "icd10": "I83.9",
        "synonyms": ["Varises", "Pembuluh Darah Menonjol"],
    },
    "Kelumpuhan (Pendarahan Otak)": {
        "en": "Paralysis (brain hemorrhage)", "icd10": "I61.9",
        "synonyms": ["Stroke", "Kelumpuhan", "Pendarahan Otak"],
    },
    "Serangan Jantung": {
        "en": "Heart attack", "icd10": "I21.9",
        "synonyms": ["Serangan Jantung", "Infark Miokard", "Heart Attack"],
    },
}

# ══════════════════════════════════════════════════════
# SYMPTOM DATABASE: ~130 gejala + variasi bahasa awam
# ══════════════════════════════════════════════════════

SYMPTOM_DATABASE = {
    "sakit perut": {"en": "abdominal pain", "variants": ["sakit perut", "nyeri perut", "perut sakit", "mules", "melilit"], "body_system": "pencernaan"},
    "haid tidak normal": {"en": "abnormal menstruation", "variants": ["haid tidak normal", "menstruasi tidak teratur", "telat haid"], "body_system": "reproduksi"},
    "asam lambung naik": {"en": "acidity", "variants": ["asam lambung naik", "perut perih", "lambung perih", "ulu hati panas"], "body_system": "pencernaan"},
    "gagal hati akut": {"en": "acute liver failure", "variants": ["gagal hati", "liver failure"], "body_system": "hepatik"},
    "kesadaran berubah": {"en": "altered sensorium", "variants": ["kesadaran berubah", "linglung", "bingung", "tidak sadar"], "body_system": "neurologis"},
    "cemas": {"en": "anxiety", "variants": ["cemas", "gelisah", "khawatir", "takut", "panik"], "body_system": "psikiatri"},
    "sakit punggung": {"en": "back pain", "variants": ["sakit punggung", "nyeri punggung", "punggung pegal", "pegal-pegal"], "body_system": "muskuloskeletal"},
    "komedo": {"en": "blackheads", "variants": ["komedo", "komedo hitam", "pori-pori tersumbat"], "body_system": "dermatologi"},
    "tidak nyaman di kandung kemih": {"en": "bladder discomfort", "variants": ["tidak nyaman kandung kemih", "nyeri kandung kemih"], "body_system": "urologi"},
    "melepuh": {"en": "blister", "variants": ["melepuh", "kulit melepuh", "lecet", "gelembung kulit"], "body_system": "dermatologi"},
    "batuk berdarah": {"en": "blood in sputum", "variants": ["batuk berdarah", "dahak berdarah", "ludah darah"], "body_system": "respirasi"},
    "buang air besar berdarah": {"en": "bloody stool", "variants": ["BAB berdarah", "buang air besar berdarah", "tinja berdarah"], "body_system": "pencernaan"},
    "penglihatan kabur": {"en": "blurred and distorted vision", "variants": ["penglihatan kabur", "mata kabur", "buram", "tidak jelas melihat"], "body_system": "oftalmologi"},
    "sesak napas": {"en": "breathlessness", "variants": ["sesak napas", "susah napas", "napas pendek", "napas berat", "ngos-ngosan"], "body_system": "respirasi"},
    "kuku rapuh": {"en": "brittle nails", "variants": ["kuku rapuh", "kuku mudah patah", "kuku tipis"], "body_system": "dermatologi"},
    "memar": {"en": "bruising", "variants": ["memar", "lebam", "biru-biru", "bengkak biru"], "body_system": "hematologi"},
    "rasa terbakar saat buang air kecil": {"en": "burning micturition", "variants": ["sakit BAK", "perih BAK", "panas saat pipis", "anyang-anyangan"], "body_system": "urologi"},
    "sakit dada": {"en": "chest pain", "variants": ["sakit dada", "nyeri dada", "dada sesak", "dada terasa berat"], "body_system": "kardiovaskular"},
    "menggigil": {"en": "chills", "variants": ["menggigil", "kedinginan", "meriang", "badan dingin"], "body_system": "umum"},
    "tangan dan kaki dingin": {"en": "cold hands and feets", "variants": ["tangan dingin", "kaki dingin", "ujung jari dingin"], "body_system": "kardiovaskular"},
    "koma": {"en": "coma", "variants": ["koma", "tidak sadarkan diri", "pingsan lama"], "body_system": "neurologis"},
    "hidung tersumbat": {"en": "congestion", "variants": ["hidung tersumbat", "hidung mampet", "pilek", "buntu"], "body_system": "respirasi"},
    "sembelit": {"en": "constipation", "variants": ["sembelit", "susah BAB", "konstipasi", "tidak bisa BAB"], "body_system": "pencernaan"},
    "rasa ingin pipis terus": {"en": "continuous feel of urine", "variants": ["sering pipis", "BAK terus", "rasa ingin pipis", "beser"], "body_system": "urologi"},
    "bersin terus menerus": {"en": "continuous sneezing", "variants": ["bersin-bersin", "bersin terus", "sering bersin"], "body_system": "respirasi"},
    "batuk": {"en": "cough", "variants": ["batuk", "batuk-batuk", "batuk kering", "batuk berdahak"], "body_system": "respirasi"},
    "kram": {"en": "cramps", "variants": ["kram", "keram", "kejang otot", "otot tegang"], "body_system": "muskuloskeletal"},
    "urine berwarna gelap": {"en": "dark urine", "variants": ["urine gelap", "air kencing gelap", "pipis berwarna teh"], "body_system": "urologi"},
    "dehidrasi": {"en": "dehydration", "variants": ["dehidrasi", "kurang cairan", "haus terus", "bibir kering"], "body_system": "umum"},
    "depresi": {"en": "depression", "variants": ["depresi", "sedih terus", "murung", "tidak bergairah"], "body_system": "psikiatri"},
    "diare": {"en": "diarrhoea", "variants": ["diare", "mencret", "buang air besar cair", "BAB cair"], "body_system": "pencernaan"},
    "bercak perubahan warna kulit": {"en": "dischromic patches", "variants": ["bercak kulit", "perubahan warna kulit", "flek kulit"], "body_system": "dermatologi"},
    "perut kembung": {"en": "distention of abdomen", "variants": ["kembung", "perut kembung", "perut begah", "perut keras"], "body_system": "pencernaan"},
    "pusing": {"en": "dizziness", "variants": ["pusing", "kepala pusing", "vertigo", "puyeng", "kliyengan"], "body_system": "neurologis"},
    "bibir kering dan kesemutan": {"en": "drying and tingling lips", "variants": ["bibir kering", "bibir pecah-pecah", "kesemutan bibir"], "body_system": "dermatologi"},
    "pembesaran tiroid": {"en": "enlarged thyroid", "variants": ["tiroid membesar", "gondok", "benjolan leher"], "body_system": "endokrin"},
    "rasa lapar berlebihan": {"en": "excessive hunger", "variants": ["lapar terus", "selalu lapar", "nafsu makan berlebihan"], "body_system": "endokrin"},
    "kontak seksual berisiko": {"en": "extra marital contacts", "variants": ["kontak seksual berisiko", "hubungan tidak aman"], "body_system": "infeksi"},
    "riwayat keluarga": {"en": "family history", "variants": ["riwayat keluarga", "ada keturunan", "bawaan keluarga"], "body_system": "umum"},
    "detak jantung cepat": {"en": "fast heart rate", "variants": ["jantung cepat", "berdebar-debar", "jantung berdebar", "deg-degan"], "body_system": "kardiovaskular"},
    "lemas": {"en": "fatigue", "variants": ["lemas", "capek", "lelah", "tidak bertenaga", "loyo"], "body_system": "umum"},
    "kelebihan cairan": {"en": "fluid overload", "variants": ["kelebihan cairan", "bengkak", "edema"], "body_system": "kardiovaskular"},
    "bau urine menyengat": {"en": "foul smell of urine", "variants": ["pipis bau", "urine bau", "air kencing berbau"], "body_system": "urologi"},
    "sakit kepala": {"en": "headache", "variants": ["sakit kepala", "kepala pusing", "nyeri kepala", "pening", "cekot-cekot"], "body_system": "neurologis"},
    "demam tinggi": {"en": "high fever", "variants": ["demam tinggi", "panas tinggi", "demam", "badan panas", "suhu tinggi"], "body_system": "umum"},
    "nyeri sendi panggul": {"en": "hip joint pain", "variants": ["nyeri panggul", "sakit pinggul", "nyeri sendi panggul"], "body_system": "muskuloskeletal"},
    "riwayat konsumsi alkohol": {"en": "history of alcohol consumption", "variants": ["sering minum alkohol", "riwayat alkohol", "peminum"], "body_system": "hepatik"},
    "nafsu makan meningkat": {"en": "increased appetite", "variants": ["nafsu makan naik", "selalu lapar", "doyan makan"], "body_system": "endokrin"},
    "gangguan pencernaan": {"en": "indigestion", "variants": ["gangguan pencernaan", "susah cerna", "perut tidak enak"], "body_system": "pencernaan"},
    "kuku meradang": {"en": "inflammatory nails", "variants": ["kuku meradang", "kuku bengkak", "infeksi kuku"], "body_system": "dermatologi"},
    "gatal di dalam": {"en": "internal itching", "variants": ["gatal dalam", "gatal di dalam tubuh"], "body_system": "imunologi"},
    "kadar gula tidak teratur": {"en": "irregular sugar level", "variants": ["gula tidak stabil", "gula naik turun", "gula darah tidak teratur"], "body_system": "endokrin"},
    "mudah marah": {"en": "irritability", "variants": ["mudah marah", "sensitif", "emosional", "mudah tersinggung"], "body_system": "psikiatri"},
    "iritasi di anus": {"en": "irritation in anus", "variants": ["gatal anus", "iritasi anus", "sakit dubur"], "body_system": "pencernaan"},
    "nyeri sendi": {"en": "joint pain", "variants": ["nyeri sendi", "sendi sakit", "sakit sendi", "pegal sendi"], "body_system": "muskuloskeletal"},
    "sakit lutut": {"en": "knee pain", "variants": ["sakit lutut", "nyeri lutut", "lutut ngilu"], "body_system": "muskuloskeletal"},
    "sulit berkonsentrasi": {"en": "lack of concentration", "variants": ["sulit konsentrasi", "tidak fokus", "susah fokus"], "body_system": "neurologis"},
    "lesu": {"en": "lethargy", "variants": ["lesu", "malas", "loyo", "tidak bersemangat"], "body_system": "umum"},
    "hilang nafsu makan": {"en": "loss of appetite", "variants": ["tidak nafsu makan", "hilang nafsu makan", "malas makan"], "body_system": "pencernaan"},
    "hilang keseimbangan": {"en": "loss of balance", "variants": ["hilang keseimbangan", "sempoyongan", "oleng"], "body_system": "neurologis"},
    "hilang penciuman": {"en": "loss of smell", "variants": ["hilang penciuman", "tidak bisa cium bau", "anosmia"], "body_system": "respirasi"},
    "tidak enak badan": {"en": "malaise", "variants": ["tidak enak badan", "badan tidak fit", "merasa sakit"], "body_system": "umum"},
    "demam ringan": {"en": "mild fever", "variants": ["demam ringan", "agak panas", "sumeng", "hangat"], "body_system": "umum"},
    "perubahan suasana hati": {"en": "mood swings", "variants": ["mood swing", "suasana hati berubah", "kadang senang kadang sedih"], "body_system": "psikiatri"},
    "kaku saat bergerak": {"en": "movement stiffness", "variants": ["kaku", "badan kaku", "susah gerak", "otot kaku"], "body_system": "muskuloskeletal"},
    "dahak berlendir": {"en": "mucoid sputum", "variants": ["dahak", "dahak berlendir", "lendir di tenggorokan"], "body_system": "respirasi"},
    "nyeri otot": {"en": "muscle pain", "variants": ["nyeri otot", "otot pegal", "badan pegal", "pegal-pegal"], "body_system": "muskuloskeletal"},
    "pengecilan otot": {"en": "muscle wasting", "variants": ["otot mengecil", "otot atropi", "kurus otot"], "body_system": "muskuloskeletal"},
    "lemah otot": {"en": "muscle weakness", "variants": ["lemah otot", "otot lemas", "tidak kuat angkat"], "body_system": "muskuloskeletal"},
    "mual": {"en": "nausea", "variants": ["mual", "enek", "mau muntah", "eneg"], "body_system": "pencernaan"},
    "sakit leher": {"en": "neck pain", "variants": ["sakit leher", "nyeri leher", "leher kaku"], "body_system": "muskuloskeletal"},
    "benjolan merah di kulit": {"en": "nodal skin eruptions", "variants": ["benjolan kulit", "bentol merah", "ruam"], "body_system": "dermatologi"},
    "obesitas": {"en": "obesity", "variants": ["obesitas", "kegemukan", "berat badan berlebih"], "body_system": "endokrin"},
    "sakit di belakang mata": {"en": "pain behind the eyes", "variants": ["sakit belakang mata", "nyeri di balik mata", "mata nyeri"], "body_system": "oftalmologi"},
    "sakit saat buang air besar": {"en": "pain during bowel movements", "variants": ["sakit saat BAB", "nyeri BAB", "BAB sakit"], "body_system": "pencernaan"},
    "sakit di daerah anus": {"en": "pain in anal region", "variants": ["sakit anus", "nyeri dubur", "sakit di pantat"], "body_system": "pencernaan"},
    "sakit saat berjalan": {"en": "painful walking", "variants": ["sakit jalan", "nyeri saat berjalan", "pincang"], "body_system": "muskuloskeletal"},
    "jantung berdebar": {"en": "palpitations", "variants": ["jantung berdebar", "deg-degan", "berdebar-debar", "palpitasi"], "body_system": "kardiovaskular"},
    "sering buang gas": {"en": "passage of gases", "variants": ["sering kentut", "buang gas", "perut bunyi"], "body_system": "pencernaan"},
    "bercak di tenggorokan": {"en": "patches in throat", "variants": ["bercak tenggorokan", "putih di tenggorokan", "radang tenggorokan"], "body_system": "respirasi"},
    "dahak": {"en": "phlegm", "variants": ["dahak", "lendir", "berdahak"], "body_system": "respirasi"},
    "sering buang air kecil": {"en": "polyuria", "variants": ["sering pipis", "sering BAK", "pipis terus", "beser"], "body_system": "urologi"},
    "urat menonjol di betis": {"en": "prominent veins on calf", "variants": ["urat menonjol", "pembuluh menonjol", "varises kaki"], "body_system": "kardiovaskular"},
    "wajah dan mata bengkak": {"en": "puffy face and eyes", "variants": ["wajah bengkak", "mata bengkak", "muka sembab"], "body_system": "nefrologi"},
    "jerawat bernanah": {"en": "pus filled pimples", "variants": ["jerawat nanah", "jerawat besar", "bisul"], "body_system": "dermatologi"},
    "menerima transfusi darah": {"en": "receiving blood transfusion", "variants": ["transfusi darah", "pernah transfusi"], "body_system": "infeksi"},
    "menerima suntikan tidak steril": {"en": "receiving unsterile injections", "variants": ["suntikan tidak steril", "jarum suntik bekas"], "body_system": "infeksi"},
    "luka merah di sekitar hidung": {"en": "red sore around nose", "variants": ["luka di hidung", "merah di hidung", "lecet hidung"], "body_system": "dermatologi"},
    "bintik merah di seluruh tubuh": {"en": "red spots over body", "variants": ["bintik merah", "bercak merah", "ruam merah", "bentol-bentol"], "body_system": "dermatologi"},
    "mata merah": {"en": "redness of eyes", "variants": ["mata merah", "mata iritasi", "conjunctivitis"], "body_system": "oftalmologi"},
    "gelisah": {"en": "restlessness", "variants": ["gelisah", "tidak tenang", "resah", "was-was"], "body_system": "psikiatri"},
    "hidung meler": {"en": "runny nose", "variants": ["hidung meler", "ingus", "pilek encer"], "body_system": "respirasi"},
    "dahak berwarna karat": {"en": "rusty sputum", "variants": ["dahak karat", "dahak coklat kemerahan"], "body_system": "respirasi"},
    "luka gores": {"en": "scurring", "variants": ["luka gores", "lecet", "luka cakar"], "body_system": "dermatologi"},
    "sisik perak": {"en": "silver like dusting", "variants": ["sisik perak", "kulit bersisik", "serpihan kulit"], "body_system": "dermatologi"},
    "tekanan sinus": {"en": "sinus pressure", "variants": ["tekanan sinus", "sinus", "nyeri sinus", "wajah terasa berat"], "body_system": "respirasi"},
    "kulit mengelupas": {"en": "skin peeling", "variants": ["kulit mengelupas", "kulit ngelotok", "kulit kering mengelupas"], "body_system": "dermatologi"},
    "ruam kulit": {"en": "skin rash", "variants": ["ruam", "ruam kulit", "gatal-gatal", "biduran"], "body_system": "dermatologi"},
    "bicara pelat": {"en": "slurred speech", "variants": ["bicara pelat", "cadel mendadak", "sulit bicara", "pelo"], "body_system": "neurologis"},
    "lekukan kecil di kuku": {"en": "small dents in nails", "variants": ["kuku berlekuk", "kuku tidak rata"], "body_system": "dermatologi"},
    "berputar-putar": {"en": "spinning movements", "variants": ["berputar-putar", "dunia berputar", "vertigo"], "body_system": "neurologis"},
    "bercak urin": {"en": "spotting urination", "variants": ["bercak urin", "pipis sedikit-sedikit"], "body_system": "urologi"},
    "leher kaku": {"en": "stiff neck", "variants": ["leher kaku", "leher tegang", "tortikolis"], "body_system": "muskuloskeletal"},
    "pendarahan lambung": {"en": "stomach bleeding", "variants": ["lambung berdarah", "muntah darah", "BAB hitam"], "body_system": "pencernaan"},
    "mata cekung": {"en": "sunken eyes", "variants": ["mata cekung", "mata cowong", "mata dalam"], "body_system": "umum"},
    "berkeringat": {"en": "sweating", "variants": ["berkeringat", "keringat banyak", "keringatan", "keringat dingin"], "body_system": "umum"},
    "kelenjar getah bening bengkak": {"en": "swelled lymph nodes", "variants": ["kelenjar bengkak", "benjolan di leher", "KGB bengkak"], "body_system": "imunologi"},
    "sendi bengkak": {"en": "swelling joints", "variants": ["sendi bengkak", "bengkak sendi", "sendi membengkak"], "body_system": "muskuloskeletal"},
    "perut membengkak": {"en": "swelling of stomach", "variants": ["perut membengkak", "perut buncit", "asites"], "body_system": "pencernaan"},
    "pembuluh darah bengkak": {"en": "swollen blood vessels", "variants": ["pembuluh darah bengkak", "varises", "vena menonjol"], "body_system": "kardiovaskular"},
    "kaki bengkak": {"en": "swollen legs", "variants": ["kaki bengkak", "kaki sembab", "edema kaki"], "body_system": "kardiovaskular"},
    "iritasi tenggorokan": {"en": "throat irritation", "variants": ["tenggorokan gatal", "radang tenggorokan", "sakit tenggorokan"], "body_system": "respirasi"},
    "wajah pucat sakit": {"en": "toxic look (typhos)", "variants": ["wajah pucat", "muka pucat", "tampak sakit"], "body_system": "umum"},
    "sariawan di lidah": {"en": "ulcers on tongue", "variants": ["sariawan", "sariawan lidah", "luka di mulut"], "body_system": "pencernaan"},
    "tidak stabil": {"en": "unsteadiness", "variants": ["tidak stabil", "goyang", "limbung", "oleng"], "body_system": "neurologis"},
    "gangguan pengelihatan": {"en": "visual disturbances", "variants": ["gangguan penglihatan", "penglihatan terganggu", "mata bermasalah"], "body_system": "oftalmologi"},
    "muntah": {"en": "vomiting", "variants": ["muntah", "muntah-muntah", "mual muntah"], "body_system": "pencernaan"},
    "mata berair": {"en": "watering from eyes", "variants": ["mata berair", "mata keluar air", "nrocos"], "body_system": "oftalmologi"},
    "lemah anggota gerak": {"en": "weakness in limbs", "variants": ["lemah tangan kaki", "anggota gerak lemas", "tidak bertenaga"], "body_system": "neurologis"},
    "lemah satu sisi tubuh": {"en": "weakness of one body side", "variants": ["lemah sebelah", "lumpuh sebelah", "hemiparesis"], "body_system": "neurologis"},
    "berat badan naik": {"en": "weight gain", "variants": ["berat badan naik", "gendut", "badan melar"], "body_system": "endokrin"},
    "berat badan turun": {"en": "weight loss", "variants": ["berat badan turun", "kurus", "badan menyusut"], "body_system": "endokrin"},
    "cairan kuning mengeras": {"en": "yellow crust ooze", "variants": ["cairan kuning", "koreng berair", "luka basah kuning"], "body_system": "dermatologi"},
    "urine kuning pekat": {"en": "yellow urine", "variants": ["pipis kuning pekat", "urine kuning", "air kencing kuning"], "body_system": "urologi"},
    "mata menguning": {"en": "yellowing of eyes", "variants": ["mata kuning", "sklera kuning", "mata ikterik"], "body_system": "hepatik"},
    "kulit menguning": {"en": "yellowish skin", "variants": ["kulit kuning", "kulit menguning", "ikterus"], "body_system": "hepatik"},
}


class DiseaseKnowledgeBase:
    """
    Knowledge Base untuk SAPA: lookup penyakit, gejala, ICD-10, dan symptom vector.
    """

    def __init__(self):
        self.diseases = DISEASE_DATABASE
        self.symptoms = SYMPTOM_DATABASE
        self.symptom_names = list(SYMPTOM_DATABASE.keys())
        self.disease_names = list(DISEASE_DATABASE.keys())

        # Build reverse lookup: english symptom name -> canonical indonesian
        self._en_to_id = {}
        for canonical, info in self.symptoms.items():
            self._en_to_id[info["en"].lower().strip()] = canonical

        # Build variant -> canonical lookup (for fast text matching)
        self._variant_lookup = {}
        for canonical, info in self.symptoms.items():
            for variant in info["variants"]:
                self._variant_lookup[variant.lower()] = canonical

        # Disease-symptom matrix will be built from Kaggle data
        self._disease_symptom_matrix = None

    def build_matrix_from_kaggle(self, kaggle_csv_path):
        """Build disease-symptom binary matrix from Kaggle dataset.csv"""
        import pandas as pd

        df = pd.read_csv(kaggle_csv_path)
        n_diseases = len(self.disease_names)
        n_symptoms = len(self.symptom_names)

        matrix = np.zeros((n_diseases, n_symptoms), dtype=np.float32)

        # Create disease name mapping (English -> index)
        disease_en_to_id = {}
        for i, (name_id, info) in enumerate(self.diseases.items()):
            en_name = info["en"].strip()
            disease_en_to_id[en_name] = i

        for _, row in df.iterrows():
            disease_en = row['Disease'].strip()
            d_idx = disease_en_to_id.get(disease_en)
            if d_idx is None:
                continue

            for col in df.columns:
                if col.startswith('Symptom') and pd.notna(row[col]):
                    symp_en = str(row[col]).replace('_', ' ').strip().lower()
                    canonical = self._en_to_id.get(symp_en)
                    if canonical:
                        s_idx = self.symptom_names.index(canonical)
                        matrix[d_idx, s_idx] = 1.0

        self._disease_symptom_matrix = matrix
        print(f"✅ Disease-Symptom Matrix built: {matrix.shape}")
        print(f"   Non-zero entries: {int(matrix.sum())} / {n_diseases * n_symptoms}")
        return matrix

    def get_icd10(self, disease_name):
        """Get ICD-10 code for a disease."""
        info = self.diseases.get(disease_name)
        return info["icd10"] if info else "—"

    def get_disease_symptoms(self, disease_name):
        """Get list of symptom names for a disease."""
        if self._disease_symptom_matrix is None:
            return []
        d_idx_list = [i for i, name in enumerate(self.disease_names) if name == disease_name]
        if not d_idx_list:
            return []
        d_idx = d_idx_list[0]
        active = np.where(self._disease_symptom_matrix[d_idx] > 0)[0]
        return [self.symptom_names[i] for i in active]

    def get_symptom_vector(self, text):
        """
        Convert free-text complaint into a binary symptom vector (130-dim).
        Uses variant matching to detect symptoms from text.
        """
        text_lower = text.lower()
        vector = np.zeros(len(self.symptom_names), dtype=np.float32)

        for variant, canonical in self._variant_lookup.items():
            if variant in text_lower:
                idx = self.symptom_names.index(canonical)
                vector[idx] = 1.0

        return vector

    def extract_symptoms(self, text):
        """
        Extract detected symptom names from free-text complaint.
        Returns list of canonical Indonesian symptom names.
        """
        text_lower = text.lower()
        detected = set()

        for variant, canonical in self._variant_lookup.items():
            if len(variant) > 2 and variant in text_lower:
                detected.add(canonical)

        return list(detected)

    def save(self, path):
        """Save the knowledge base to pickle."""
        data = {
            "diseases": self.diseases,
            "symptoms": self.symptoms,
            "matrix": self._disease_symptom_matrix,
            "symptom_names": self.symptom_names,
            "disease_names": self.disease_names,
        }
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        print(f"💾 Knowledge Base saved to {path}")

    def load(self, path):
        """Load the knowledge base from pickle."""
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.diseases = data["diseases"]
        self.symptoms = data["symptoms"]
        self._disease_symptom_matrix = data["matrix"]
        self.symptom_names = data["symptom_names"]
        self.disease_names = data["disease_names"]
        print(f"✅ Knowledge Base loaded from {path}")


# ══════════════════════════════════════════════════════
# CLI: Build and save KB
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("SAPA Knowledge Base Builder")
    print("=" * 60)

    kb = DiseaseKnowledgeBase()
    print(f"\n📊 Database Stats:")
    print(f"   Diseases: {len(kb.disease_names)}")
    print(f"   Symptoms: {len(kb.symptom_names)}")
    print(f"   Variants: {len(kb._variant_lookup)}")

    kaggle_csv = "../data/kaggle_raw/dataset.csv"
    if os.path.exists(kaggle_csv):
        print(f"\n🔨 Building disease-symptom matrix from {kaggle_csv}...")
        kb.build_matrix_from_kaggle(kaggle_csv)

        # Save
        out_path = "../data/knowledge_base.pkl"
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        kb.save(out_path)

        # Test
        print("\n🧪 Test: 'Saya demam tinggi dan bintik merah di badan'")
        test_text = "Saya demam tinggi dan bintik merah di badan"
        vec = kb.get_symptom_vector(test_text)
        detected = kb.extract_symptoms(test_text)
        print(f"   Detected symptoms: {detected}")
        print(f"   Symptom vector sum: {vec.sum()}")
        print(f"   ICD-10 DBD: {kb.get_icd10('Demam Berdarah Dengue (DBD)')}")
        print(f"   DBD symptoms: {kb.get_disease_symptoms('Demam Berdarah Dengue (DBD)')[:5]}")
    else:
        print(f"\n⚠️ Kaggle dataset not found at {kaggle_csv}")
        print("   Please run download_kaggle_dataset.py first")

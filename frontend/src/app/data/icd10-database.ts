/**
 * SAPA ICD-10 Database
 * Source: WHO ICD-10 Version 2019 (https://icd.who.int/browse10/2019/en)
 * Cross-validated with Kemenkes RI 144 penyakit BPJS Puskesmas
 * 
 * Format: { code, name (English), nameId (Indonesian) }
 * Grouped by ICD-10 Chapter
 */

const ICD10_DATABASE = [
    // ═══ Chapter I: Certain infectious and parasitic diseases (A00-B99) ═══
    { code: "A01.0", name: "Typhoid fever", nameId: "Demam Tifoid (Tifus)" },
    { code: "A09", name: "Infectious gastroenteritis and colitis", nameId: "Gastroenteritis (Muntaber)" },
    { code: "A15.0", name: "Tuberculosis of lung", nameId: "TBC Paru (Tuberkulosis)" },
    { code: "A16.9", name: "Respiratory tuberculosis unspecified", nameId: "TBC Paru (tidak terkonfirmasi)" },
    { code: "A90", name: "Dengue fever", nameId: "Demam Berdarah Dengue (DBD)" },
    { code: "A91", name: "Dengue haemorrhagic fever", nameId: "Demam Berdarah Dengue Berat" },
    { code: "B01.9", name: "Varicella without complication", nameId: "Cacar Air (Varicella)" },
    { code: "B02.9", name: "Zoster without complication", nameId: "Herpes Zoster (Cacar Ular)" },
    { code: "B15.9", name: "Hepatitis A without hepatic coma", nameId: "Hepatitis A" },
    { code: "B16.9", name: "Acute hepatitis B without delta-agent", nameId: "Hepatitis B Akut" },
    { code: "B17.0", name: "Acute delta-(super)infection of hepatitis B carrier", nameId: "Hepatitis D" },
    { code: "B17.1", name: "Acute hepatitis C", nameId: "Hepatitis C Akut" },
    { code: "B17.2", name: "Acute hepatitis E", nameId: "Hepatitis E Akut" },
    { code: "B20", name: "HIV disease resulting in infectious and parasitic diseases", nameId: "HIV/AIDS" },
    { code: "B24", name: "Unspecified HIV disease", nameId: "Penyakit HIV (tidak spesifik)" },
    { code: "B35.0", name: "Tinea barbae and tinea capitis", nameId: "Kurap Kepala" },
    { code: "B35.1", name: "Tinea unguium", nameId: "Jamur Kuku" },
    { code: "B35.4", name: "Tinea corporis", nameId: "Kurap Badan" },
    { code: "B35.6", name: "Tinea cruris", nameId: "Kurap Selangkangan" },
    { code: "B35.9", name: "Dermatophytosis, unspecified", nameId: "Infeksi Jamur Kulit" },
    { code: "B36.0", name: "Pityriasis versicolor", nameId: "Panu" },
    { code: "B37.0", name: "Candidal stomatitis", nameId: "Infeksi Jamur Mulut (Sariawan)" },
    { code: "B54", name: "Unspecified malaria", nameId: "Malaria" },
    { code: "B77.9", name: "Ascariasis, unspecified", nameId: "Cacingan (Askariasis)" },
    { code: "B82.9", name: "Intestinal parasitism, unspecified", nameId: "Cacingan" },
    { code: "B86", name: "Scabies", nameId: "Kudis (Skabies)" },

    // ═══ Chapter II: Neoplasms (C00-D48) ═══
    { code: "C50.9", name: "Breast, unspecified", nameId: "Kanker Payudara" },
    { code: "C53.9", name: "Cervix uteri, unspecified", nameId: "Kanker Serviks" },
    { code: "D25.9", name: "Leiomyoma of uterus, unspecified", nameId: "Mioma Uteri" },

    // ═══ Chapter III: Diseases of blood (D50-D89) ═══
    { code: "D50.9", name: "Iron deficiency anaemia, unspecified", nameId: "Anemia Defisiensi Besi" },
    { code: "D64.9", name: "Anaemia, unspecified", nameId: "Anemia" },

    // ═══ Chapter IV: Endocrine, nutritional and metabolic diseases (E00-E90) ═══
    { code: "E03.9", name: "Hypothyroidism, unspecified", nameId: "Hipotiroid" },
    { code: "E05.9", name: "Thyrotoxicosis, unspecified", nameId: "Hipertiroid" },
    { code: "E10.9", name: "Type 1 diabetes mellitus", nameId: "Diabetes Melitus Tipe 1" },
    { code: "E11.9", name: "Type 2 diabetes mellitus", nameId: "Diabetes Melitus Tipe 2" },
    { code: "E14.9", name: "Unspecified diabetes mellitus", nameId: "Diabetes Melitus" },
    { code: "E16.2", name: "Hypoglycaemia, unspecified", nameId: "Hipoglikemia" },
    { code: "E44.0", name: "Moderate protein-energy malnutrition", nameId: "Gizi Kurang (Sedang)" },
    { code: "E46", name: "Unspecified protein-energy malnutrition", nameId: "Gizi Kurang" },
    { code: "E66.9", name: "Obesity, unspecified", nameId: "Obesitas" },
    { code: "E78.0", name: "Pure hypercholesterolaemia", nameId: "Kolesterol Tinggi" },
    { code: "E78.5", name: "Hyperlipidaemia, unspecified", nameId: "Hiperlipidemia" },
    { code: "E79.0", name: "Hyperuricaemia", nameId: "Asam Urat Tinggi (Hiperurisemia)" },
    { code: "E87.6", name: "Hypokalaemia", nameId: "Hipokalemia" },

    // ═══ Chapter V: Mental and behavioural disorders (F00-F99) ═══
    { code: "F10.2", name: "Alcohol dependence syndrome", nameId: "Ketergantungan Alkohol" },
    { code: "F20.9", name: "Schizophrenia, unspecified", nameId: "Skizofrenia" },
    { code: "F32.9", name: "Depressive episode, unspecified", nameId: "Depresi" },
    { code: "F41.0", name: "Panic disorder", nameId: "Gangguan Panik" },
    { code: "F41.1", name: "Generalized anxiety disorder", nameId: "Gangguan Cemas Menyeluruh" },
    { code: "F41.9", name: "Anxiety disorder, unspecified", nameId: "Gangguan Kecemasan" },
    { code: "F51.0", name: "Nonorganic insomnia", nameId: "Insomnia" },

    // ═══ Chapter VI: Diseases of the nervous system (G00-G99) ═══
    { code: "G40.9", name: "Epilepsy, unspecified", nameId: "Epilepsi" },
    { code: "G43.9", name: "Migraine, unspecified", nameId: "Migrain" },
    { code: "G44.2", name: "Tension-type headache", nameId: "Sakit Kepala Tegang (Tension)" },
    { code: "G47.0", name: "Disorders of initiating and maintaining sleep", nameId: "Gangguan Tidur" },

    // ═══ Chapter VII: Diseases of the eye (H00-H59) ═══
    { code: "H10.9", name: "Conjunctivitis, unspecified", nameId: "Konjungtivitis (Mata Merah)" },
    { code: "H25.9", name: "Senile cataract, unspecified", nameId: "Katarak Senilis" },
    { code: "H65.9", name: "Nonsuppurative otitis media, unspecified", nameId: "Otitis Media Non-Supuratif" },
    { code: "H66.9", name: "Otitis media, unspecified", nameId: "Otitis Media (Infeksi Telinga Tengah)" },

    // ═══ Chapter VIII: Diseases of the ear (H60-H95) ═══
    { code: "H81.1", name: "Benign paroxysmal vertigo", nameId: "Vertigo (BPPV)" },
    { code: "H81.3", name: "Other peripheral vertigo", nameId: "Vertigo Perifer" },
    { code: "H81.9", name: "Disorder of vestibular function, unspecified", nameId: "Gangguan Vestibular" },

    // ═══ Chapter IX: Diseases of the circulatory system (I00-I99) ═══
    { code: "I10", name: "Essential (primary) hypertension", nameId: "Hipertensi Primer (Darah Tinggi)" },
    { code: "I11.9", name: "Hypertensive heart disease without heart failure", nameId: "Penyakit Jantung Hipertensi" },
    { code: "I20.9", name: "Angina pectoris, unspecified", nameId: "Angina Pektoris" },
    { code: "I21.9", name: "Acute myocardial infarction, unspecified", nameId: "Serangan Jantung (Infark Miokard)" },
    { code: "I25.9", name: "Chronic ischaemic heart disease, unspecified", nameId: "Penyakit Jantung Koroner" },
    { code: "I48.9", name: "Atrial fibrillation and flutter, unspecified", nameId: "Fibrilasi Atrium" },
    { code: "I50.9", name: "Heart failure, unspecified", nameId: "Gagal Jantung" },
    { code: "I61.9", name: "Intracerebral haemorrhage, unspecified", nameId: "Stroke Hemoragik (Pendarahan Otak)" },
    { code: "I63.9", name: "Cerebral infarction, unspecified", nameId: "Stroke Iskemik" },
    { code: "I64", name: "Stroke, not specified as haemorrhage or infarction", nameId: "Stroke" },
    { code: "I83.9", name: "Varicose veins of lower extremities", nameId: "Varises Tungkai Bawah" },
    { code: "I84.9", name: "Haemorrhoids, unspecified", nameId: "Wasir (Hemoroid)" },
    { code: "I95.1", name: "Orthostatic hypotension", nameId: "Hipotensi Ortostatik" },

    // ═══ Chapter X: Diseases of the respiratory system (J00-J99) ═══
    { code: "J00", name: "Acute nasopharyngitis (common cold)", nameId: "Pilek (Common Cold)" },
    { code: "J01.9", name: "Acute sinusitis, unspecified", nameId: "Sinusitis Akut" },
    { code: "J02.9", name: "Acute pharyngitis, unspecified", nameId: "Faringitis Akut (Radang Tenggorokan)" },
    { code: "J03.9", name: "Acute tonsillitis, unspecified", nameId: "Tonsilitis Akut (Amandel)" },
    { code: "J04.0", name: "Acute laryngitis", nameId: "Laringitis Akut" },
    { code: "J06.9", name: "Acute upper respiratory infection, unspecified", nameId: "ISPA (Infeksi Saluran Napas Atas)" },
    { code: "J10.1", name: "Influenza with other respiratory manifestations", nameId: "Influenza (Flu)" },
    { code: "J11.1", name: "Influenza with other respiratory manifestations, virus not identified", nameId: "Influenza (virus belum teridentifikasi)" },
    { code: "J18.9", name: "Pneumonia, unspecified", nameId: "Pneumonia (Radang Paru)" },
    { code: "J20.9", name: "Acute bronchitis, unspecified", nameId: "Bronkitis Akut" },
    { code: "J21.9", name: "Acute bronchiolitis, unspecified", nameId: "Bronkiolitis Akut" },
    { code: "J30.4", name: "Allergic rhinitis, unspecified", nameId: "Rinitis Alergi" },
    { code: "J42", name: "Unspecified chronic bronchitis", nameId: "Bronkitis Kronis" },
    { code: "J44.9", name: "Chronic obstructive pulmonary disease, unspecified", nameId: "PPOK (Penyakit Paru Obstruktif Kronik)" },
    { code: "J45.9", name: "Asthma, unspecified", nameId: "Asma Bronkial" },
    { code: "J46", name: "Status asthmaticus", nameId: "Status Asmatikus (Serangan Asma Berat)" },

    // ═══ Chapter XI: Diseases of the digestive system (K00-K93) ═══
    { code: "K02.9", name: "Dental caries, unspecified", nameId: "Karies Gigi" },
    { code: "K04.0", name: "Pulpitis", nameId: "Pulpitis (Sakit Gigi Berlubang)" },
    { code: "K05.0", name: "Acute gingivitis", nameId: "Gingivitis (Radang Gusi)" },
    { code: "K12.0", name: "Recurrent oral aphthae", nameId: "Sariawan (Stomatitis)" },
    { code: "K21.0", name: "Gastro-oesophageal reflux disease with oesophagitis", nameId: "GERD (Asam Lambung Naik)" },
    { code: "K25.9", name: "Gastric ulcer, unspecified", nameId: "Tukak Lambung" },
    { code: "K29.1", name: "Other acute gastritis", nameId: "Gastritis Akut" },
    { code: "K29.5", name: "Chronic gastritis, unspecified", nameId: "Gastritis Kronis" },
    { code: "K29.7", name: "Gastritis, unspecified", nameId: "Gastritis (Maag)" },
    { code: "K30", name: "Functional dyspepsia", nameId: "Dispepsia (Gangguan Pencernaan)" },
    { code: "K35.9", name: "Acute appendicitis, unspecified", nameId: "Apendisitis Akut (Usus Buntu)" },
    { code: "K40.9", name: "Unilateral or unspecified inguinal hernia", nameId: "Hernia Inguinalis" },
    { code: "K52.9", name: "Noninfective gastroenteritis and colitis, unspecified", nameId: "Gastroenteritis Non-Infeksi" },
    { code: "K58.9", name: "Irritable bowel syndrome without diarrhoea", nameId: "Sindrom Iritasi Usus (IBS)" },
    { code: "K59.0", name: "Constipation", nameId: "Konstipasi (Sembelit)" },
    { code: "K64.9", name: "Haemorrhoids, unspecified", nameId: "Wasir/Ambeien (Hemoroid)" },
    { code: "K70.1", name: "Alcoholic hepatitis", nameId: "Hepatitis Alkoholik" },
    { code: "K73.9", name: "Chronic hepatitis, unspecified", nameId: "Hepatitis Kronis" },
    { code: "K74.6", name: "Other and unspecified cirrhosis of liver", nameId: "Sirosis Hati" },
    { code: "K80.2", name: "Calculus of gallbladder without cholecystitis", nameId: "Batu Empedu" },
    { code: "K83.1", name: "Obstruction of bile duct", nameId: "Kolestasis Kronis" },
    { code: "K85.9", name: "Acute pancreatitis, unspecified", nameId: "Pankreatitis Akut" },

    // ═══ Chapter XII: Diseases of the skin (L00-L99) ═══
    { code: "L01.0", name: "Impetigo", nameId: "Impetigo" },
    { code: "L02.9", name: "Cutaneous abscess, furuncle and carbuncle", nameId: "Bisul (Furunkel)" },
    { code: "L20.9", name: "Atopic dermatitis, unspecified", nameId: "Dermatitis Atopik (Eksim)" },
    { code: "L23.9", name: "Allergic contact dermatitis, unspecified", nameId: "Dermatitis Kontak Alergi" },
    { code: "L30.9", name: "Dermatitis, unspecified", nameId: "Dermatitis" },
    { code: "L40.9", name: "Psoriasis, unspecified", nameId: "Psoriasis" },
    { code: "L50.9", name: "Urticaria, unspecified", nameId: "Urtikaria (Biduran)" },
    { code: "L60.0", name: "Ingrowing nail", nameId: "Kuku Tumbuh ke Dalam" },
    { code: "L70.0", name: "Acne vulgaris", nameId: "Jerawat (Acne Vulgaris)" },
    { code: "L72.1", name: "Trichilemmal cyst", nameId: "Kista Epidermoid" },

    // ═══ Chapter XIII: Diseases of the musculoskeletal system (M00-M99) ═══
    { code: "M06.9", name: "Rheumatoid arthritis, unspecified", nameId: "Rematik (Artritis Reumatoid)" },
    { code: "M10.9", name: "Gout, unspecified", nameId: "Asam Urat (Gout)" },
    { code: "M13.9", name: "Arthritis, unspecified", nameId: "Radang Sendi (Artritis)" },
    { code: "M15.9", name: "Polyarthrosis, unspecified", nameId: "Poliartrosis" },
    { code: "M19.9", name: "Arthrosis, unspecified", nameId: "Osteoartritis (Pengapuran Sendi)" },
    { code: "M47.8", name: "Other spondylosis", nameId: "Spondilosis (Saraf Leher Terjepit)" },
    { code: "M54.2", name: "Cervicalgia", nameId: "Nyeri Leher (Servikal)" },
    { code: "M54.5", name: "Low back pain", nameId: "Nyeri Punggung Bawah (LBP)" },
    { code: "M54.9", name: "Dorsalgia, unspecified", nameId: "Nyeri Punggung" },
    { code: "M62.8", name: "Other specified disorders of muscle", nameId: "Gangguan Otot Lain" },
    { code: "M75.1", name: "Rotator cuff syndrome", nameId: "Sindrom Rotator Cuff" },
    { code: "M79.1", name: "Myalgia", nameId: "Nyeri Otot (Mialgia)" },
    { code: "M79.3", name: "Panniculitis, unspecified", nameId: "Panikulitis" },

    // ═══ Chapter XIV: Diseases of the genitourinary system (N00-N99) ═══
    { code: "N18.9", name: "Chronic kidney disease, unspecified", nameId: "Gagal Ginjal Kronis (CKD)" },
    { code: "N20.0", name: "Calculus of kidney", nameId: "Batu Ginjal" },
    { code: "N30.0", name: "Acute cystitis", nameId: "Sistitis Akut (Infeksi Kandung Kemih)" },
    { code: "N39.0", name: "Urinary tract infection, site not specified", nameId: "Infeksi Saluran Kemih (ISK)" },
    { code: "N76.0", name: "Acute vaginitis", nameId: "Vaginitis Akut" },
    { code: "N92.1", name: "Excessive and frequent menstruation with irregular cycle", nameId: "Menstruasi Tidak Teratur" },

    // ═══ Chapter XV: Pregnancy, childbirth and the puerperium (O00-O99) ═══
    { code: "O21.0", name: "Mild hyperemesis gravidarum", nameId: "Hiperemesis Gravidarum (Mual Hamil)" },
    { code: "O26.8", name: "Other specified pregnancy-related conditions", nameId: "Komplikasi Kehamilan Lain" },
    { code: "O80", name: "Single spontaneous delivery", nameId: "Persalinan Normal" },

    // ═══ Chapter XVII: Congenital malformations (Q00-Q99) ═══
    { code: "Q66.0", name: "Talipes equinovarus", nameId: "Kaki Pengkor Bawaan" },

    // ═══ Chapter XVIII: Symptoms, signs and abnormal findings (R00-R99) ═══
    { code: "R00.0", name: "Tachycardia, unspecified", nameId: "Takikardia (Jantung Cepat)" },
    { code: "R05", name: "Cough", nameId: "Batuk" },
    { code: "R06.0", name: "Dyspnoea", nameId: "Sesak Napas (Dispnea)" },
    { code: "R10.4", name: "Other and unspecified abdominal pain", nameId: "Nyeri Perut" },
    { code: "R11", name: "Nausea and vomiting", nameId: "Mual dan Muntah" },
    { code: "R17", name: "Unspecified jaundice", nameId: "Penyakit Kuning (Ikterus)" },
    { code: "R42", name: "Dizziness and giddiness", nameId: "Pusing (Dizziness)" },
    { code: "R50.9", name: "Fever, unspecified", nameId: "Demam" },
    { code: "R51", name: "Headache", nameId: "Sakit Kepala (Cephalgia)" },
    { code: "R52.9", name: "Pain, unspecified", nameId: "Nyeri (tidak spesifik)" },
    { code: "R53", name: "Malaise and fatigue", nameId: "Lemas dan Kelelahan" },
    { code: "R55", name: "Syncope and collapse", nameId: "Pingsan (Sinkop)" },
    { code: "R63.0", name: "Anorexia", nameId: "Kurang Nafsu Makan" },

    // ═══ Chapter XIX: Injury, poisoning (S00-T98) ═══
    { code: "S00.0", name: "Superficial injury of scalp", nameId: "Luka Superfisial Kulit Kepala" },
    { code: "S61.0", name: "Open wound of finger(s)", nameId: "Luka Terbuka Jari" },
    { code: "T14.0", name: "Superficial injury of unspecified body region", nameId: "Luka Superfisial" },
    { code: "T14.1", name: "Open wound of unspecified body region", nameId: "Luka Terbuka" },
    { code: "T30.0", name: "Burn of unspecified body region, unspecified degree", nameId: "Luka Bakar" },
    { code: "T78.2", name: "Anaphylactic shock, unspecified", nameId: "Syok Anafilaksis" },
    { code: "T78.4", name: "Allergy, unspecified", nameId: "Reaksi Alergi" },
    { code: "T88.7", name: "Unspecified adverse effect of drug or medicament", nameId: "Reaksi Obat / Alergi Obat" },

    // ═══ Chapter XXI: Factors influencing health status (Z00-Z99) ═══
    { code: "Z00.0", name: "General medical examination", nameId: "Pemeriksaan Kesehatan Umum (MCU)" },
    { code: "Z23", name: "Need for immunization", nameId: "Imunisasi" },
    { code: "Z30.0", name: "General counselling and advice on contraception", nameId: "Konsultasi KB" },
    { code: "Z76.0", name: "Issue of repeat prescription", nameId: "Resep Ulang" },
];

/**
 * Search ICD-10 database by code or name (Indonesian/English)
 * @param {string} query - Search query
 * @param {number} limit - Max results (default 15)
 * @returns {Array} Matching ICD-10 entries
 */
export function searchICD10(query: string, limit: number = 15): any[] {
    if (!query || query.trim().length < 1) return [];
    const q = query.toLowerCase().trim();

    return ICD10_DATABASE
        .filter(entry =>
            entry.code.toLowerCase().includes(q) ||
            entry.nameId.toLowerCase().includes(q) ||
            entry.name.toLowerCase().includes(q)
        )
        .slice(0, limit);
}

/**
 * Get ICD-10 entry by exact code
 * @param {string} code - ICD-10 code
 * @returns {Object|null}
 */
export function getICD10ByCode(code: string): any | null {
    return ICD10_DATABASE.find(e => e.code === code) || null;
}

/**
 * Format ICD-10 entry for display
 * @param {Object} entry - ICD-10 entry
 * @returns {string} Formatted string "K29.7 — Gastritis (Maag)"
 */
export function formatICD10(entry: any): string {
    if (!entry) return '';
    return `${entry.code} — ${entry.nameId}`;
}

export default ICD10_DATABASE;

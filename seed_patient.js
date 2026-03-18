/**
 * Seed script for testing SAPA application (Nakes & Doctor Dashboard).
 * Run this in the BROWSER CONSOLE (F12 -> Console) while on localhost:4200.
 * 
 * Usage: Copy all code below → paste into browser console → press Enter.
 * 
 * Includes 6 dummy patients with all required fields:
 * NIK, BPJS, Alamat lengkap, vital signs, anamnesis, diagnoses
 */
const seedPatients = [
    // ─── Pasien 1: Vertigo + Hipertensi (Severity: HIGH) ─────────────────
    {
        id: (Date.now()).toString(),
        name: "Ahmad Wijaya",
        time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        severity: "high",
        predicted: "Vertigo",
        patientData: {
            nik: "3374012803970001",
            namaLengkap: "Ahmad Wijaya",
            jenisKelamin: "L",
            alamat: "Jl. Merdeka No. 12A",
            kelurahan: "Karangrejo",
            kecamatan: "Gajahmungkur",
            kabupaten: "Semarang",
            provinsi: "Jawa Tengah",
            kodePos: "50231",
            noHP: "088891765416",
            noBPJS: "0001234567891",
            beratBadan: "65",
            tinggiBadan: "170",
            suhuBadan: "36.5",
            tekananDarah: "160/100",
            usia: "27",
            keluhan_utama: "Pusing berputar sejak 2 hari yang lalu, mual muntah, sulit berdiri tegak",
            durasi: "2 hari",
        },
        summary: {
            resumeMedis: "Pasien laki-laki 27 tahun datang dengan keluhan pusing berputar (vertigo) yang memberat sejak 2 hari. Disertai mual muntah. Riwayat hipertensi. Tekanan darah 160/100 mmHg. Suspek BPPV dengan komorbid hipertensi.",
            icdTags: [
                { code: "H81.1", label: "Benign Paroxysmal Positional Vertigo" },
                { code: "I10", label: "Hipertensi Esensial" }
            ],
            diagnoses: [
                { name: "Vertigo (BPPV)", icd: "H81.1", score: 85 },
                { name: "Hipertensi", icd: "I10", score: 72 },
                { name: "Migrain", icd: "G43.9", score: 15 }
            ],
            rasaFields: {
                keluhan_utama: "Pusing berputar sejak 2 hari yang lalu, mual muntah, sulit berdiri tegak",
                durasi: "2 hari",
                lokasi_keluhan: "Kepala",
                keparahan: "Berat (7/10)",
                gejala_penyerta: "Mual, muntah, susah berdiri",
                riwayat_penyakit: "Hipertensi",
                riwayat_alergi: "Tidak ada",
            }
        },
        messages: [
            { role: "ai", text: "Halo, Kak! Saya RASA. Ceritakan keluhan pasien.", time: "08:00" },
            { role: "user", text: "Pasien mengeluh pusing berputar sejak 2 hari yang lalu. Mual muntah, sulit berdiri.", time: "08:01" },
            { role: "ai", text: "Baik. Berapa lama durasi pusing berputarnya setiap episode?", time: "08:01" },
            { role: "user", text: "Sekitar 30 detik sampai 1 menit, terutama saat berubah posisi.", time: "08:02" },
            { role: "ai", text: "Apakah ada riwayat penyakit sebelumnya seperti hipertensi atau diabetes?", time: "08:02" },
            { role: "user", text: "Ya, pasien punya riwayat hipertensi. Tidak ada alergi obat.", time: "08:03" }
        ]
    },

    // ─── Pasien 2: DBD (Severity: HIGH) ───────────────────────────────────
    {
        id: (Date.now() + 1).toString(),
        name: "Siti Rahayu",
        time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        severity: "high",
        predicted: "Demam Berdarah Dengue",
        patientData: {
            nik: "3301234567890001",
            namaLengkap: "Siti Rahayu",
            jenisKelamin: "P",
            alamat: "Jl. Anggrek No. 55",
            kelurahan: "Banyumanik",
            kecamatan: "Banyumanik",
            kabupaten: "Semarang",
            provinsi: "Jawa Tengah",
            kodePos: "50266",
            noHP: "081234567890",
            noBPJS: "0009876543210",
            beratBadan: "55",
            tinggiBadan: "160",
            suhuBadan: "38.9",
            tekananDarah: "100/70",
            usia: "35",
            keluhan_utama: "Demam tinggi mendadak 3 hari, nyeri sendi seluruh tubuh, muncul bintik merah di lengan dan dada",
            durasi: "3 hari",
        },
        summary: {
            resumeMedis: "Pasien perempuan 35 tahun dengan demam tinggi mendadak hari ke-3 (suhu 38.9°C), nyeri retroorbital, mialgia, artralgia, dan ruam petekie di lengan dan dada. Suspek Dengue Hemorrhagic Fever. Perlu cek darah lengkap segera (trombosit & hematokrit).",
            icdTags: [
                { code: "A91", label: "Dengue Haemorrhagic Fever" },
                { code: "A90", label: "Dengue Fever" }
            ],
            diagnoses: [
                { name: "Demam Berdarah Dengue (DBD)", icd: "A91", score: 82 },
                { name: "Dengue Fever", icd: "A90", score: 60 },
                { name: "Demam Tifoid", icd: "A01.0", score: 25 }
            ],
            rasaFields: {
                keluhan_utama: "Demam tinggi mendadak 3 hari, nyeri sendi, bintik merah",
                durasi: "3 hari",
                lokasi_keluhan: "Seluruh tubuh, lengan, dada",
                keparahan: "Berat (8/10)",
                gejala_penyerta: "Nyeri mata, nyeri otot, ruam petekie",
                riwayat_penyakit: "Tidak ada",
                riwayat_alergi: "Tidak ada",
            }
        },
        messages: [
            { role: "ai", text: "Halo Kak! Ceritakan keluhan pasien.", time: "09:00" },
            { role: "user", text: "Pasien demam tinggi 3 hari, nyeri sendi, bintik merah di badan.", time: "09:01" },
            { role: "ai", text: "Apakah demamnya naik turun atau terus-menerus tinggi?", time: "09:01" },
            { role: "user", text: "Terus-menerus tinggi, tidak turun meski sudah minum paracetamol.", time: "09:02" },
        ]
    },

    // ─── Pasien 3: Dispepsia/GERD (Severity: MEDIUM) ────────────────────
    {
        id: (Date.now() + 2).toString(),
        name: "Budi Santoso",
        time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        severity: "medium",
        predicted: "GERD",
        patientData: {
            nik: "3175098765432100",
            namaLengkap: "Budi Santoso",
            jenisKelamin: "L",
            alamat: "Jl. Pemuda No. 88",
            kelurahan: "Pandansari",
            kecamatan: "Semarang Tengah",
            kabupaten: "Semarang",
            provinsi: "Jawa Tengah",
            kodePos: "50134",
            noHP: "085678901234",
            noBPJS: "0001122334455",
            beratBadan: "78",
            tinggiBadan: "175",
            suhuBadan: "36.7",
            tekananDarah: "130/85",
            usia: "42",
            keluhan_utama: "Nyeri dan panas di ulu hati, mulut pahit, perut kembung, kadang mual",
            durasi: "1 minggu",
        },
        summary: {
            resumeMedis: "Pasien laki-laki 42 tahun dengan keluhan nyeri epigastrium berulang sejak 1 minggu, disertai heartburn, mulut pahit saat bangun tidur, dan kembung. Riwayat makan tidak teratur dan sering telat makan. Tidak ada alarm symptom.",
            icdTags: [
                { code: "K21.0", label: "GERD dengan Esofagitis" },
                { code: "K30", label: "Dispepsia Fungsional" }
            ],
            diagnoses: [
                { name: "GERD (Asam Lambung)", icd: "K21.0", score: 68 },
                { name: "Gastritis", icd: "K29.7", score: 55 },
                { name: "Dispepsia", icd: "K30", score: 40 }
            ],
            rasaFields: {
                keluhan_utama: "Nyeri ulu hati, mulut pahit, perut kembung, mual",
                durasi: "1 minggu",
                lokasi_keluhan: "Ulu hati, dada bagian bawah",
                keparahan: "Sedang (5/10)",
                gejala_penyerta: "Kembung, mulut pahit, mual",
                riwayat_penyakit: "Maag kronis",
                riwayat_alergi: "Tidak ada",
            }
        },
        messages: [
            { role: "ai", text: "Halo Kak! Ceritakan keluhan pasien.", time: "10:00" },
            { role: "user", text: "Pasien nyeri ulu hati, dada panas, mulut pahit terutama pagi hari.", time: "10:01" },
        ]
    },

    // ─── Pasien 4: ISPA / Infeksi Saluran Pernapasan (Severity: LOW) ────
    {
        id: (Date.now() + 3).toString(),
        name: "Dewi Lestari",
        time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        severity: "low",
        predicted: "ISPA",
        patientData: {
            nik: "3374056789012345",
            namaLengkap: "Dewi Lestari",
            jenisKelamin: "P",
            alamat: "Jl. Cendana No. 7",
            kelurahan: "Tembalang",
            kecamatan: "Tembalang",
            kabupaten: "Semarang",
            provinsi: "Jawa Tengah",
            kodePos: "50275",
            noHP: "087712345678",
            noBPJS: "0007654321098",
            beratBadan: "50",
            tinggiBadan: "155",
            suhuBadan: "37.8",
            tekananDarah: "110/70",
            usia: "23",
            keluhan_utama: "Pilek, batuk kering, n tenggorokan gatal dan sakit, sedikit demam sejak kemarin",
            durasi: "2 hari",
        },
        summary: {
            resumeMedis: "Pasien perempuan 23 tahun datang dengan keluhan pilek, batuk kering, nyeri tenggorokan, dan demam ringan (37.8°C) sejak 2 hari. Tidak ada sesak napas. Riwayat kontak dengan penderita flu di tempat kerja 5 hari yang lalu.",
            icdTags: [
                { code: "J06.9", label: "Infeksi Respirasi Atas Akut" },
                { code: "J00", label: "Nasofaringitis Akut (Common Cold)" }
            ],
            diagnoses: [
                { name: "ISPA (Infeksi Saluran Pernapasan Atas)", icd: "J06.9", score: 75 },
                { name: "Faringitis Akut", icd: "J02.9", score: 50 },
                { name: "Influenza", icd: "J11.1", score: 35 }
            ],
            rasaFields: {
                keluhan_utama: "Pilek, batuk kering, tenggorokan sakit, demam ringan",
                durasi: "2 hari",
                lokasi_keluhan: "Hidung, tenggorokan",
                keparahan: "Ringan (3/10)",
                gejala_penyerta: "Bersin-bersin, hidung tersumbat",
                riwayat_penyakit: "Tidak ada",
                riwayat_alergi: "Tidak ada",
            }
        },
        messages: [
            { role: "ai", text: "Halo Kak! Ceritakan keluhan pasien.", time: "11:00" },
            { role: "user", text: "Pasien pilek batuk, tenggorokan sakit, sedikit demam sejak kemarin.", time: "11:01" },
        ]
    },

    // ─── Pasien 5: Diare Akut (Severity: MEDIUM) ────────────────────────
    {
        id: (Date.now() + 4).toString(),
        name: "Rudi Hermawan",
        time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        severity: "medium",
        predicted: "Diare Akut",
        patientData: {
            nik: "3374023456789012",
            namaLengkap: "Rudi Hermawan",
            jenisKelamin: "L",
            alamat: "Jl. Veteran No. 33",
            kelurahan: "Pleburan",
            kecamatan: "Semarang Selatan",
            kabupaten: "Semarang",
            provinsi: "Jawa Tengah",
            kodePos: "50249",
            noHP: "081398765432",
            noBPJS: "0005544332211",
            beratBadan: "60",
            tinggiBadan: "168",
            suhuBadan: "37.5",
            tekananDarah: "120/80",
            usia: "31",
            keluhan_utama: "Diare lebih dari 5 kali sejak tadi malam, perut mulas dan kram, sedikit mual",
            durasi: "Sejak tadi malam (±10 jam)",
        },
        summary: {
            resumeMedis: "Pasien laki-laki 31 tahun dengan keluhan diare akut > 5x/hari sejak 10 jam yang lalu, konsistensi cair tanpa darah, disertai kram perut dan mual ringan. Riwayat makan di luar (warteg) semalam. Tanda-tanda dehidrasi ringan.",
            icdTags: [
                { code: "A09", label: "Gastroenteritis & Kolitis Infeksi Lainnya" },
                { code: "K59.1", label: "Diare Fungsional" }
            ],
            diagnoses: [
                { name: "Diare Akut (Gastroenteritis)", icd: "A09", score: 78 },
                { name: "Keracunan Makanan", icd: "A05.9", score: 55 },
                { name: "Kolitis", icd: "K52.9", score: 20 }
            ],
            rasaFields: {
                keluhan_utama: "Diare >5x sejak tadi malam, perut mulas dan kram, mual",
                durasi: "±10 jam",
                lokasi_keluhan: "Perut",
                keparahan: "Sedang (6/10)",
                gejala_penyerta: "Mual, kram perut, lemas",
                riwayat_penyakit: "Tidak ada",
                riwayat_alergi: "Tidak ada",
            }
        },
        messages: [
            { role: "ai", text: "Halo Kak! Ceritakan keluhan pasien.", time: "13:00" },
            { role: "user", text: "Pasien diare lebih dari 5 kali dari tadi malam, perut mulas, mual.", time: "13:01" },
        ]
    },

    // ─── Pasien 6: Diabetes (Severity: HIGH) ────────────────────────────
    {
        id: (Date.now() + 5).toString(),
        name: "Sunarti Wulandari",
        time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
        severity: "high",
        predicted: "Diabetes Mellitus",
        patientData: {
            nik: "3374065432109876",
            namaLengkap: "Sunarti Wulandari",
            jenisKelamin: "P",
            alamat: "Jl. Singosari No. 21",
            kelurahan: "Wonotingal",
            kecamatan: "Candisari",
            kabupaten: "Semarang",
            provinsi: "Jawa Tengah",
            kodePos: "50251",
            noHP: "082211122333",
            noBPJS: "0008877665544",
            beratBadan: "72",
            tinggiBadan: "158",
            suhuBadan: "36.8",
            tekananDarah: "140/90",
            usia: "54",
            keluhan_utama: "Sering haus, sering buang air kecil terutama malam hari, pandangan kabur, mudah lelah dan luka di kaki susah sembuh",
            durasi: "Sudah 2 minggu",
        },
        summary: {
            resumeMedis: "Pasien perempuan 54 tahun dengan keluhan polidipsi, poliuria (terutama nokturnal), penglihatan buram, astenia, dan luka di kaki yang sulit sembuh sejak 2 minggu. Riwayat keluarga DM (+). Tekanan darah 140/90 mmHg. Suspek Diabetes Mellitus tipe 2 dengan komplikasi awal.",
            icdTags: [
                { code: "E11", label: "Diabetes Mellitus Tipe 2" },
                { code: "I10", label: "Hipertensi Esensial" }
            ],
            diagnoses: [
                { name: "Diabetes Mellitus Tipe 2", icd: "E11", score: 88 },
                { name: "Hipertensi", icd: "I10", score: 70 },
                { name: "Neuropati Perifer", icd: "E11.4", score: 45 }
            ],
            rasaFields: {
                keluhan_utama: "Sering haus, sering BAK malam, buram, lelah, luka susah sembuh",
                durasi: "2 minggu",
                lokasi_keluhan: "Seluruh tubuh, kaki, mata",
                keparahan: "Berat (7/10)",
                gejala_penyerta: "Polidipsi, poliuria, penglihatan buram",
                riwayat_penyakit: "Riwayat keluarga DM, hipertensi",
                riwayat_alergi: "Tidak ada",
            }
        },
        messages: [
            { role: "ai", text: "Halo Kak! Ceritakan keluhan pasien.", time: "14:00" },
            { role: "user", text: "Pasien sering haus, sering kencing terutama malam, pandangan kabur, luka di kaki tidak sembuh-sembuh.", time: "14:01" },
            { role: "ai", text: "Sudah berapa lama keluhan ini berlangsung? Apakah ada riwayat keluarga dengan diabetes?", time: "14:01" },
            { role: "user", text: "Sekitar 2 minggu. Ya, ayah pasien juga punya diabetes.", time: "14:02" },
        ]
    }
];

// ═══ Inject ke localStorage ═══════════════════════════════
localStorage.setItem('sapa_patients', JSON.stringify(seedPatients));

// ═══ Konfirmasi ═══════════════════════════════════════════
console.log(`
✅ SAPA Seed Data Berhasil!
══════════════════════════════════════
📋 ${seedPatients.length} pasien berhasil ditambahkan:

${seedPatients.map((p, i) => `  ${i + 1}. ${p.name} (${p.severity.toUpperCase()}) → ${p.predicted}`).join('\n')}

💡 Refresh halaman atau kembali ke Dashboard Dokter
   untuk melihat daftar pasien.
══════════════════════════════════════
`);

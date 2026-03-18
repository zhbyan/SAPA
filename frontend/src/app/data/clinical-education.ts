/**
 * SAPA Clinical Education Mapping
 * ================================
 * Mapping edukasi pasien untuk 41 penyakit di knowledge base SAPA.
 *
 * Sumber referensi:
 * - Kemenkes RI — Panduan Praktik Klinis (PPK) untuk Fasyankes Primer
 * - WHO — Clinical Practice Guidelines
 * - PERKENI — Konsensus Pengelolaan DM di Indonesia
 * - PERDOSSI — Pedoman Tatalaksana Penyakit Saraf
 * - PERDOSKI — Pedoman Diagnosis & Tatalaksana Dermatologi
 * - PERKI — Pedoman Tatalaksana Sindrom Koroner Akut
 * - PGI — Konsensus Gastroenterologi
 * - PDPI — Pedoman Diagnosis & Penatalaksanaan Paru
 * - PAPDI — Buku Ajar Ilmu Penyakit Dalam
 * - Harrison's Principles of Internal Medicine, 21st Ed
 * - JNC 8 — Guideline for Management of High Blood Pressure
 * - GINA — Global Initiative for Asthma
 */

export const CLINICAL_EDUCATION: Record<string, { edukasi: string[], tindakLanjut: string, sumber: string }> = {

    // ══════════════════════════════════════════════
    // PENYAKIT INFEKSI
    // ══════════════════════════════════════════════

    "Demam Berdarah Dengue (DBD)": {
        edukasi: [
            "Minum banyak cairan: air putih, oralit, jus buah segar (minimal 2-3 liter/hari)",
            "Kompres hangat (bukan dingin) di dahi dan lipatan tubuh bila suhu ≥38.5°C",
            "Istirahat total (bed rest) selama masa demam",
            "Kontrol hitung trombosit dan hematokrit setiap hari pada fase kritis (hari ke-3 sampai 7)",
            "Segera ke IGD jika muncul tanda bahaya: nyeri perut hebat, muntah persisten, perdarahan, gelisah, tangan/kaki dingin, penurunan kesadaran",
            "Hindari obat golongan NSAID (aspirin, ibuprofen) — hanya paracetamol untuk penurun demam"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI Tatalaksana DBD; WHO Dengue Guidelines 2009"
    },

    "Tifus (Demam Tifoid)": {
        edukasi: [
            "Istirahat total (bed rest) sampai demam turun minimal 7 hari",
            "Makan makanan lunak rendah serat (bubur, nasi tim) untuk mengurangi beban usus",
            "Minum obat antibiotik sampai habis sesuai resep, jangan berhenti meski merasa sudah membaik",
            "Perbanyak minum air putih untuk mencegah dehidrasi",
            "Jaga kebersihan makanan dan minuman (cuci tangan, masak air sampai mendidih)",
            "Kontrol ulang setelah pengobatan selesai untuk memastikan bakteri telah eradikasi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; PAPDI Buku Ajar Ilmu Penyakit Dalam"
    },

    "TBC (Tuberkulosis)": {
        edukasi: [
            "Minum OAT (Obat Anti Tuberkulosis) setiap hari tanpa terputus selama 6-8 bulan",
            "Jangan berhenti minum obat meskipun merasa sudah sehat — risiko resistensi obat",
            "Tutup mulut dan hidung saat batuk/bersin (etika batuk)",
            "Pastikan ventilasi rumah baik dan terkena sinar matahari",
            "Makan makanan bergizi tinggi protein untuk mempercepat penyembuhan",
            "Periksakan dahak (BTA) ulang pada bulan ke-2, ke-5, dan akhir pengobatan"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "Program DOTS Kemenkes RI; WHO TB Treatment Guidelines 2022"
    },

    "ISPA/Influenza": {
        edukasi: [
            "Istirahat yang cukup (tidur 7-9 jam/hari)",
            "Perbanyak minum air hangat untuk mengencerkan dahak",
            "Makan makanan bergizi dan buah-buahan kaya vitamin C",
            "Gunakan masker saat berinteraksi dengan orang lain untuk mencegah penularan",
            "Hindari paparan udara dingin, asap, dan debu",
            "Segera kembali jika demam >3 hari, sesak napas, atau batuk darah"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI untuk Fasyankes Primer; WHO IMCI Guidelines"
    },

    "Pneumonia (Radang Paru)": {
        edukasi: [
            "Habiskan antibiotik sesuai resep dokter, jangan berhenti meski merasa membaik",
            "Istirahat total, hindari aktivitas berat selama masa pemulihan",
            "Minum air putih minimal 2 liter/hari untuk membantu mengencerkan dahak",
            "Posisi semi-fowler (setengah duduk) saat tidur untuk membantu pernapasan",
            "Segera kembali jika sesak napas memburuk, demam tidak turun >48 jam setelah antibiotik, atau batuk darah",
            "Vaksinasi pneumokokus dan influenza dianjurkan setelah sembuh"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PDPI Pedoman Pneumonia Komunitas; WHO Pneumonia Fact Sheet"
    },

    "Malaria": {
        edukasi: [
            "Minum obat antimalaria sampai habis sesuai resep (jangan berhenti saat merasa membaik)",
            "Gunakan kelambu berinsektisida saat tidur untuk mencegah infeksi ulang",
            "Hindari gigitan nyamuk: pakai lotion antinyamuk, kenakan pakaian lengan panjang sore/malam hari",
            "Segera kembali jika demam muncul kembali setelah pengobatan selesai",
            "Makan teratur dan minum banyak cairan untuk menjaga stamina"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI Malaria; WHO Malaria Treatment Guidelines 2022"
    },

    "Cacar Air": {
        edukasi: [
            "Isolasi di rumah selama 5-7 hari atau sampai semua lesi mengering dan berkrusta",
            "Jangan menggaruk lesi untuk menghindari infeksi sekunder dan bekas luka",
            "Potong kuku pendek dan jaga kebersihan tangan",
            "Mandi dengan air hangat (boleh ditambah PK/betadine encer) untuk menjaga kebersihan kulit",
            "Minum obat sesuai resep (antiviral jika diresepkan, antihistamin untuk gatal)",
            "Hindari kontak dengan ibu hamil, bayi, dan orang immunocompromised"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; IDAI Pedoman Penyakit Infeksi Anak"
    },

    "HIV/AIDS": {
        edukasi: [
            "Minum ARV setiap hari pada jam yang sama, jangan pernah terputus",
            "Kontrol rutin ke klinik VCT setiap bulan untuk monitoring CD4 dan viral load",
            "Gunakan kondom saat berhubungan seksual untuk mencegah penularan",
            "Jangan berbagi jarum suntik, silet, atau alat tajam lainnya",
            "Jaga pola makan bergizi dan tidur cukup untuk menjaga daya tahan tubuh",
            "Segera ke dokter jika ada infeksi oportunistik (demam berkepanjangan, diare, batuk kronis)"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "Permenkes RI No. 21/2013 tentang Penanggulangan HIV/AIDS; WHO ART Guidelines"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT METABOLIK & ENDOKRIN
    // ══════════════════════════════════════════════

    "Diabetes Melitus": {
        edukasi: [
            "Atur pola makan: diet rendah gula dan karbohidrat sederhana, perbanyak sayur dan buah",
            "Olahraga teratur minimal 150 menit/minggu (jalan kaki 30 menit, 5x/minggu)",
            "Periksa gula darah mandiri secara rutin (puasa dan 2 jam setelah makan)",
            "Perawatan kaki harian: periksa luka/lecet, jangan berjalan tanpa alas kaki, potong kuku lurus",
            "Minum obat antidiabetik/suntik insulin sesuai resep, jangan ubah dosis sendiri",
            "Kontrol HbA1c setiap 3 bulan, periksa mata dan ginjal setiap tahun"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "Konsensus PERKENI 2021; ADA Standards of Medical Care in Diabetes"
    },

    "Hipertensi": {
        edukasi: [
            "Diet rendah garam: batasi konsumsi garam <5 gram/hari (1 sendok teh)",
            "Kurangi makanan berlemak, gorengan, dan makanan olahan/instan",
            "Olahraga aerobik teratur 30 menit/hari (jalan cepat, bersepeda, berenang)",
            "Kontrol tekanan darah rutin di rumah, catat hasilnya",
            "Minum obat antihipertensi secara teratur, jangan berhenti tanpa instruksi dokter",
            "Kelola stres: teknik relaksasi, tidur cukup 7-8 jam/hari"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "JNC 8 Guidelines; PPK Kemenkes RI Hipertensi; Konsensus InaSH"
    },

    "Hipertiroid": {
        edukasi: [
            "Minum obat antitiroid (PTU/Methimazole) sesuai resep, jangan ubah dosis sendiri",
            "Hindari makanan tinggi yodium berlebihan (rumput laut, garam beryodium berlebih)",
            "Jaga asupan kalori tinggi karena metabolisme meningkat",
            "Hindari kafein dan stimulan yang bisa memperburuk jantung berdebar",
            "Kontrol fungsi tiroid (T3, T4, TSH) secara berkala sesuai jadwal",
            "Segera ke dokter jika denyut jantung sangat cepat, demam tinggi, atau penurunan kesadaran (krisis tiroid)"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PERKENI Pedoman Tiroid; ATA Guidelines for Hyperthyroidism"
    },

    "Hipotiroid": {
        edukasi: [
            "Minum Levothyroxine setiap pagi saat perut kosong, 30 menit sebelum makan",
            "Jangan minum obat tiroid bersamaan dengan suplemen kalsium, zat besi, atau antasida",
            "Kontrol TSH secara berkala (setiap 6-8 minggu saat penyesuaian dosis, lalu setiap 6 bulan)",
            "Jaga pola makan seimbang, cukup serat untuk mengatasi sembelit",
            "Olahraga ringan teratur untuk menjaga metabolisme dan berat badan"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PERKENI; ATA Guidelines for Hypothyroidism"
    },

    "Hipoglikemia (Gula Darah Rendah)": {
        edukasi: [
            "Kenali tanda hipoglikemia: gemetar, keringat dingin, jantung berdebar, lemas, bingung",
            "Selalu bawa makanan/minuman manis (permen, jus, gula) untuk penanganan darurat",
            "Jika gejala muncul: segera minum 15 gram gula cepat serap (3 sendok gula + air, atau 150ml jus)",
            "Periksa ulang gula darah 15 menit setelah penanganan",
            "Makan teratur 3x sehari dengan selingan snack, jangan melewatkan waktu makan",
            "Konsultasikan penyesuaian dosis obat/insulin dengan dokter jika sering terjadi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PERKENI Konsensus DM; ADA Hypoglycemia Management"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT PENCERNAAN
    // ══════════════════════════════════════════════

    "Gastritis (Maag)": {
        edukasi: [
            "Makan teratur dan porsi kecil tapi sering (5-6x/hari)",
            "Hindari makanan pedas, asam, berminyak, dan kopi saat perut kosong",
            "Jangan minum obat NSAID (ibuprofen, aspirin) tanpa perintah dokter",
            "Hindari alkohol dan merokok",
            "Makan minimal 2-3 jam sebelum tidur, jangan langsung berbaring setelah makan",
            "Kelola stres: stres berlebihan memperburuk gejala maag"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; PGI Konsensus Gastritis; ACG Guidelines"
    },

    "GERD (Asam Lambung)": {
        edukasi: [
            "Tinggikan kepala tempat tidur 15-20 cm (gunakan bantal atau balok di kaki tempat tidur)",
            "Hindari makan 2-3 jam sebelum tidur",
            "Hindari makanan pemicu: cokelat, mint, kafein, makanan berlemak, minuman bersoda",
            "Makan porsi kecil tapi sering, kunyah makanan perlahan",
            "Turunkan berat badan jika obesitas, hindari pakaian ketat di perut",
            "Minum obat PPI (omeprazole/lansoprazole) 30 menit sebelum makan pagi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "ACG Guidelines for GERD; PGI Konsensus GERD Indonesia"
    },

    "Gastroenteritis (Muntaber)": {
        edukasi: [
            "Rehidrasi oral: minum oralit setiap kali BAB cair (200 ml per episode)",
            "Tetap makan seperti biasa (jangan puasa), pilih makanan lunak mudah dicerna",
            "Cuci tangan dengan sabun sebelum makan dan setelah dari toilet",
            "Hindari susu dan makanan berlemak selama diare akut",
            "Segera ke dokter jika: diare >3 hari, demam tinggi, BAB berdarah, tanda dehidrasi berat (mata cekung, tidak kencing >8 jam)",
            "Zinc supplement 20mg/hari selama 10 hari (untuk anak sesuai dosis)"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "WHO/UNICEF ORS-Zinc Protocol; PPK Kemenkes RI Diare"
    },

    "Kolestasis Kronis": {
        edukasi: [
            "Diet rendah lemak untuk mengurangi beban empedu",
            "Hindari alkohol sepenuhnya untuk melindungi hati",
            "Minum obat asam ursodeoksikolat sesuai resep dokter",
            "Perhatikan tanda perburukan: kulit gatal hebat, kuning makin gelap, tinja pucat/dempul",
            "Kontrol fungsi hati secara berkala sesuai jadwal dokter"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PAPDI; AASLD Practice Guidance on Cholestatic Liver Disease"
    },

    "Wasir/Ambeien": {
        edukasi: [
            "Perbanyak konsumsi serat (sayur, buah, gandum utuh) minimal 25-30 gram/hari",
            "Minum air putih 8-10 gelas/hari untuk melunakkan tinja",
            "Jangan mengejan terlalu kuat saat BAB, jangan duduk terlalu lama di toilet",
            "Rendam area anus di air hangat (sitz bath) 15-20 menit, 2-3x/hari",
            "Olahraga teratur, hindari duduk/berdiri terlalu lama",
            "Segera kembali jika perdarahan banyak atau benjolan tidak bisa masuk kembali"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; ASCRS Clinical Practice Guidelines for Hemorrhoids"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT HATI (HEPATITIS)
    // ══════════════════════════════════════════════

    "Penyakit Kuning": {
        edukasi: [
            "Istirahat total, hindari aktivitas berat",
            "Hindari alkohol dan obat-obatan hepatotoksik sepenuhnya",
            "Makan makanan ringan bergizi, porsi kecil tapi sering",
            "Kontrol fungsi hati (bilirubin, SGOT, SGPT) secara berkala",
            "Segera kembali jika kuning makin gelap, nyeri perut hebat, atau penurunan kesadaran"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; PAPDI"
    },

    "Hepatitis A": {
        edukasi: [
            "Istirahat total selama fase akut (2-4 minggu), hindari aktivitas berat",
            "Hindari alkohol dan obat hepatotoksik selama 6 bulan setelah sembuh",
            "Makan makanan bergizi, hindari makanan berlemak berlebihan",
            "Cuci tangan dengan sabun setelah BAB dan sebelum makan/menyiapkan makanan",
            "Vaksinasi Hepatitis A untuk anggota keluarga dan kontak dekat"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPHI Pedoman Hepatitis; WHO Hepatitis A Fact Sheet"
    },

    "Hepatitis B": {
        edukasi: [
            "Kontrol rutin fungsi hati dan viral load HBV DNA setiap 3-6 bulan",
            "Minum obat antiviral (jika diresepkan) secara teratur tanpa terputus",
            "Hindari alkohol sepenuhnya",
            "Jangan berbagi sikat gigi, pisau cukur, atau benda tajam lainnya",
            "Gunakan kondom saat berhubungan seksual, pasangan dianjurkan vaksinasi HBV",
            "Skrining hepatoma (USG + AFP) setiap 6 bulan jika sirosis atau HBsAg positif >20 tahun"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPHI Konsensus Hepatitis B; APASL Guidelines for HBV Management"
    },

    "Hepatitis C": {
        edukasi: [
            "Jalani pengobatan DAA (Direct-Acting Antiviral) sesuai resep selama 8-12 minggu",
            "Minum obat setiap hari pada jam yang sama, jangan melewatkan dosis",
            "Hindari alkohol sepenuhnya selama dan setelah pengobatan",
            "Jangan berbagi jarum suntik, alat tato, atau benda tajam",
            "Kontrol viral load HCV RNA untuk memastikan SVR (Sustained Virological Response)"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPHI; WHO Guidelines for HCV Treatment; AASLD/IDSA HCV Guidance"
    },

    "Hepatitis D": {
        edukasi: [
            "Hepatitis D hanya terjadi bersamaan dengan infeksi Hepatitis B",
            "Minum obat antiviral sesuai resep dokter secara teratur",
            "Hindari alkohol dan obat hepatotoksik",
            "Vaksinasi Hepatitis B pada keluarga/kontak dekat untuk mencegah koinfeksi",
            "Kontrol fungsi hati secara rutin"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "WHO; PPHI; EASL Clinical Practice Guidelines on HDV"
    },

    "Hepatitis E": {
        edukasi: [
            "Istirahat total dan makan makanan bergizi selama fase akut",
            "Pastikan air minum dimasak hingga mendidih, hindari makan makanan mentah",
            "Jaga kebersihan sanitasi dan cuci tangan yang baik",
            "Hindari alkohol selama sakit dan pemulihan",
            "Umumnya sembuh sendiri dalam 4-6 minggu, kontrol jika gejala memburuk"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "WHO Hepatitis E Fact Sheet; PPK Kemenkes RI"
    },

    "Hepatitis Alkoholik": {
        edukasi: [
            "Berhenti total konsumsi alkohol — ini adalah langkah paling penting",
            "Makan makanan bergizi tinggi protein dan kalori untuk memperbaiki gizi",
            "Minum suplemen vitamin B1 (thiamine) dan asam folat sesuai resep",
            "Kontrol fungsi hati secara berkala",
            "Pertimbangkan konseling atau program rehabilitasi alkohol",
            "Segera kembali jika perut membesar, muntah darah, atau penurunan kesadaran"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "AASLD Practice Guidance on Alcohol-Associated Liver Disease; PPHI"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT KARDIOVASKULAR
    // ══════════════════════════════════════════════

    "Serangan Jantung": {
        edukasi: [
            "Minum obat jantung (aspirin, statin, beta-blocker, ACE inhibitor) sesuai resep TANPA BERHENTI",
            "Kontrol faktor risiko: berhenti merokok, diet rendah lemak jenuh dan kolesterol",
            "Rehabilitasi jantung: olahraga bertahap sesuai anjuran dokter, mulai dari jalan kaki ringan",
            "Segera hubungi ambulans (119) jika nyeri dada muncul kembali yang tidak hilang dalam 15 menit",
            "Kontrol rutin tekanan darah, gula darah, dan profil lipid",
            "Kurangi stres, tidur cukup, hindari aktivitas berat mendadak"
        ],
        tindakLanjut: "Rujuk Spesialis",
        sumber: "PERKI Pedoman Tatalaksana SKA; ESC Guidelines for ACS Management"
    },

    "Varises": {
        edukasi: [
            "Gunakan stoking kompresi (compression stockings) saat beraktivitas",
            "Tinggikan kaki 15-20 cm saat duduk atau tidur untuk membantu aliran darah balik",
            "Hindari berdiri atau duduk terlalu lama tanpa bergerak, selingi dengan jalan kaki",
            "Olahraga ringan teratur: jalan kaki, berenang, bersepeda",
            "Jaga berat badan ideal",
            "Segera kembali jika kaki bengkak bertambah, kulit berubah warna, atau muncul luka"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; ESVS Clinical Practice Guidelines on Chronic Venous Disease"
    },

    "Kelumpuhan (Pendarahan Otak)": {
        edukasi: [
            "Ikuti program rehabilitasi medik (fisioterapi) secara rutin untuk memulihkan fungsi motorik",
            "Minum obat pencegah stroke berulang (antihipertensi, antikoagulan) sesuai resep",
            "Kontrol tekanan darah ketat: target <140/90 mmHg",
            "Berhenti merokok dan hindari alkohol",
            "Modifikasi diet: rendah garam, rendah lemak, tinggi serat",
            "Perhatikan tanda stroke berulang (FAST): Face drooping, Arm weakness, Speech difficulty, Time to call emergency"
        ],
        tindakLanjut: "Rujuk Spesialis",
        sumber: "PERDOSSI Guideline Stroke; AHA/ASA Guidelines for Stroke Prevention"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT PERNAPASAN
    // ══════════════════════════════════════════════

    "Asma Bronkial": {
        edukasi: [
            "Selalu bawa inhaler darurat (reliever/SABA) ke mana pun pergi",
            "Gunakan inhaler controller (ICS) setiap hari sesuai resep, meski tidak sesak",
            "Kenali dan hindari pemicu asma: debu, asap rokok, udara dingin, bulu hewan, serbuk sari",
            "Teknik inhaler yang benar: kocok, buang napas penuh, hirup dalam-dalam, tahan 10 detik",
            "Rencana aksi asma: jika sesak tidak membaik setelah 3x semprot reliever tiap 20 menit, segera ke IGD",
            "Kontrol rutin setiap 1-3 bulan untuk penyesuaian step therapy"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "GINA 2023 Report; PDPI Pedoman Asma Dewasa"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT NEUROLOGIS
    // ══════════════════════════════════════════════

    "Migrain": {
        edukasi: [
            "Kenali dan hindari pencetus migrain: kurang tidur, stres, makanan tertentu (cokelat, keju, MSG), cahaya terang",
            "Catat diary migrain: waktu serangan, pemicu, durasi, intensitas nyeri",
            "Saat serangan: istirahat di ruangan gelap dan tenang, kompres dingin di dahi",
            "Minum obat analgesik sesegera mungkin saat aura/tanda awal serangan muncul",
            "Tidur teratur 7-8 jam, hindari tidur terlalu lama di akhir pekan",
            "Jika serangan >4x/bulan, konsultasikan obat pencegah migrain ke dokter"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PERDOSSI Pedoman Nyeri Kepala; IHS Classification of Headache Disorders (ICHD-3)"
    },

    "Vertigo": {
        edukasi: [
            "Hindari perubahan posisi kepala yang mendadak (bangun tidur pelan-pelan, duduk dulu sebelum berdiri)",
            "Lakukan manuver Epley atau Brandt-Daroff di rumah sesuai instruksi dokter",
            "Istirahat baring (bed rest) saat serangan akut, jangan memaksakan aktivitas",
            "Hindari menyetir kendaraan atau bekerja di ketinggian selama masih sering kambuh",
            "Kurangi konsumsi kafein, alkohol, dan garam berlebih",
            "Segera kembali jika disertai kelemahan anggota gerak, bicara pelo, atau penglihatan ganda"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PERDOSSI; Bárány Society Classification of Vestibular Disorders; AAO-HNS BPPV Guidelines"
    },

    "Saraf Leher Terjepit": {
        edukasi: [
            "Hindari posisi leher yang tetap terlalu lama (misal menunduk lihat HP/laptop)",
            "Lakukan peregangan leher ringan secara berkala (setiap 30-60 menit saat bekerja)",
            "Gunakan bantal yang menopang lekukan leher natural (bantal ortopedi)",
            "Kompres hangat di area leher selama 15-20 menit, 2-3x/hari",
            "Hindari mengangkat beban berat yang membebani leher dan bahu",
            "Ikuti program fisioterapi jika diresepkan"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PERDOSSI; Harrison's Principles of Internal Medicine"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT KULIT
    // ══════════════════════════════════════════════

    "Infeksi Jamur": {
        edukasi: [
            "Jaga kulit tetap kering, terutama di lipatan tubuh (ketiak, selangkangan, sela jari kaki)",
            "Ganti pakaian dalam dan kaus kaki setiap hari, gunakan yang berbahan katun",
            "Oleskan obat antijamur (krim/salep) sesuai resep, teruskan 1-2 minggu setelah lesi hilang",
            "Jangan berbagi handuk, pakaian, atau alat pribadi lainnya",
            "Hindari menggaruk area yang terinfeksi untuk mencegah penyebaran",
            "Gunakan sandal di tempat umum (kolam renang, kamar mandi umum)"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK PERDOSKI; WHO Guidelines on Dermatophytosis"
    },

    "Alergi": {
        edukasi: [
            "Identifikasi dan hindari alergen pemicu (makanan, debu, obat, bulu hewan, dll)",
            "Minum obat antihistamin sesuai resep saat gejala muncul",
            "Bersihkan rumah secara rutin, cuci sprei dan sarung bantal setiap minggu dengan air panas",
            "Gunakan masker saat terpapar debu atau polusi",
            "Segera ke IGD jika terjadi reaksi anafilaksis: sesak napas, bengkak wajah/lidah, tekanan darah turun drastis",
            "Catat riwayat alergi di kartu identitas atau gelang alergi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; PERAMULNI Guidelines; WAO White Book on Allergy"
    },

    "Reaksi Obat/Alergi": {
        edukasi: [
            "CATAT nama obat yang menyebabkan alergi dan informasikan ke setiap dokter/apoteker",
            "Hentikan obat yang dicurigai segera dan hubungi dokter",
            "Gunakan gelang atau kartu alergi obat yang selalu dibawa",
            "Minum obat antihistamin/steroid sesuai resep untuk meredakan reaksi",
            "Segera ke IGD jika muncul: sesak napas, bengkak bibir/lidah, ruam di seluruh tubuh (Stevens-Johnson Syndrome), demam tinggi",
            "Jangan minum obat yang sama atau satu golongan tanpa konsultasi dokter"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; Harrison's; WHO Drug Safety Guidelines"
    },

    "Psoriasis": {
        edukasi: [
            "Jaga agar kulit tetap lembab: gunakan pelembab/moisturizer segera setelah mandi",
            "Hindari menggaruk atau mengelupas sisik kulit secara paksa",
            "Hindari pencetus flare: stres, infeksi tenggorokan, alkohol, merokok",
            "Oleskan obat topikal (steroid/calcipotriol) sesuai resep, jangan dihentikan mendadak",
            "Paparan sinar matahari pagi (15-20 menit) dapat membantu, tetapi hindari sunburn",
            "Psoriasis adalah penyakit kronis yang bisa dikontrol — konsistensi terapi penting"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK PERDOSKI; AAD Guidelines for Psoriasis Management"
    },

    "Impetigo": {
        edukasi: [
            "Cuci area luka dengan sabun antiseptik dan air bersih 2x/hari",
            "Oleskan salep antibiotik (mupirocin/fusidic acid) sesuai resep",
            "Potong kuku pendek dan jangan menggaruk lesi untuk mencegah penyebaran",
            "Jangan berbagi handuk, pakaian, atau alat tidur dengan orang lain",
            "Anak boleh kembali ke sekolah setelah 24 jam pengobatan antibiotik atau lesi mengering",
            "Cuci tangan pakai sabun setelah menyentuh area yang terinfeksi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK PERDOSKI; WHO IMCI Guidelines"
    },

    "Jerawat": {
        edukasi: [
            "Cuci wajah 2x/hari dengan sabun/facial wash lembut (jangan berlebihan)",
            "Jangan memencet atau memecahkan jerawat — risiko infeksi dan bekas luka",
            "Gunakan produk berbahan noncomedogenic dan oil-free",
            "Oleskan obat jerawat (benzoyl peroxide/retinoid/antibiotik topikal) sesuai resep sebelum tidur",
            "Hindari menyentuh wajah terlalu sering dengan tangan",
            "Hasil pengobatan jerawat biasanya baru terlihat setelah 6-8 minggu, bersabar dan konsisten"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK PERDOSKI; AAD Acne Clinical Guidelines"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT MUSKULOSKELETAL
    // ══════════════════════════════════════════════

    "Osteoartritis": {
        edukasi: [
            "Jaga berat badan ideal — setiap penurunan 5 kg mengurangi beban lutut secara signifikan",
            "Olahraga low-impact: berenang, bersepeda statis, yoga, jalan kaki ringan",
            "Hindari aktivitas yang membebani sendi: jongkok, naik-turun tangga berlebihan, berlari",
            "Kompres hangat sebelum aktivitas, kompres dingin setelah aktivitas jika bengkak",
            "Latihan penguatan otot quadriceps untuk menopang sendi lutut",
            "Minum obat pereda nyeri (paracetamol/NSAID) sesuai resep, jangan tanpa instruksi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "IRA Pedoman OA; ACR/AF Guidelines for Management of OA; OARSI Guidelines"
    },

    "Radang Sendi": {
        edukasi: [
            "Minum obat antiinflamasi/DMARD sesuai resep secara teratur",
            "Istirahatkan sendi yang meradang, hindari gerakan berlebihan",
            "Kompres hangat untuk kaku pagi, kompres dingin untuk bengkak akut",
            "Latihan range of motion ringan untuk mencegah kekakuan sendi",
            "Kontrol rutin untuk monitoing efek samping obat (fungsi hati, ginjal, darah lengkap)",
            "Jaga berat badan ideal untuk mengurangi beban sendi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "IRA Pedoman Artritis; ACR Guidelines for RA Management"
    },

    // ══════════════════════════════════════════════
    // PENYAKIT UROLOGI
    // ══════════════════════════════════════════════

    "Infeksi Saluran Kemih": {
        edukasi: [
            "Habiskan antibiotik sesuai resep walaupun gejala sudah membaik",
            "Minum air putih minimal 8-10 gelas/hari untuk membantu menggelontor bakteri",
            "Jangan menahan kencing terlalu lama",
            "Bersihkan area genital dari depan ke belakang (terutama wanita) setiap selesai BAB/BAK",
            "Buang air kecil setelah berhubungan seksual",
            "Hindari penggunaan sabun/douche vagina yang mengiritasi"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; IAUI Pedoman ISK; EAU Guidelines on Urological Infections"
    },

    // ══════════════════════════════════════════════
    // DISPEPSIA (sering muncul sebagai prediksi)
    // ══════════════════════════════════════════════

    "Dispepsia": {
        edukasi: [
            "Makan teratur dan porsi kecil tapi sering (5-6x/hari)",
            "Hindari makanan pedas, asam, berminyak, dan kopi saat perut kosong",
            "Jangan minum obat NSAID tanpa resep dokter",
            "Hindari alkohol dan merokok",
            "Jangan langsung berbaring setelah makan, tunggu minimal 2-3 jam",
            "Kelola stres: stres berlebihan memperburuk gejala dispepsia"
        ],
        tindakLanjut: "Pulang & Rawat Jalan",
        sumber: "PPK Kemenkes RI; PGI Konsensus Dispepsia; Rome IV Criteria"
    },
};

/**
 * Mendapatkan edukasi berdasarkan nama diagnosis.
 * Melakukan fuzzy match terhadap key di CLINICAL_EDUCATION.
 * @param {string} diagnosisName - Nama penyakit dari AI prediction
 * @returns {{ edukasi: string[], tindakLanjut: string, sumber: string } | null}
 */
export function getEducationForDiagnosis(diagnosisName: string): { edukasi: string[], tindakLanjut: string, sumber: string } | null {
    if (!diagnosisName) return null;

    // Exact match
    if (CLINICAL_EDUCATION[diagnosisName]) {
        return CLINICAL_EDUCATION[diagnosisName];
    }

    // Fuzzy match: cek apakah key mengandung diagnosisName atau sebaliknya
    const nameLower = diagnosisName.toLowerCase();
    for (const [key, value] of Object.entries(CLINICAL_EDUCATION)) {
        const keyLower = key.toLowerCase();
        if (keyLower.includes(nameLower) || nameLower.includes(keyLower)) {
            return value;
        }
    }

    // Match berdasarkan sinonim umum
    const synonymMap: Record<string, string> = {
        "maag": "Gastritis (Maag)",
        "asam lambung": "GERD (Asam Lambung)",
        "flu": "ISPA/Influenza",
        "pilek": "ISPA/Influenza",
        "tipes": "Tifus (Demam Tifoid)",
        "dbd": "Demam Berdarah Dengue (DBD)",
        "kencing manis": "Diabetes Melitus",
        "darah tinggi": "Hipertensi",
        "tb": "TBC (Tuberkulosis)",
        "flek paru": "TBC (Tuberkulosis)",
        "stroke": "Kelumpuhan (Pendarahan Otak)",
        "muntaber": "Gastroenteritis (Muntaber)",
        "pusing berputar": "Vertigo",
        "bppv": "Vertigo",
        "wasir": "Wasir/Ambeien",
        "ambeien": "Wasir/Ambeien",
        "isk": "Infeksi Saluran Kemih",
        "anyang-anyangan": "Infeksi Saluran Kemih",
    };

    for (const [synonym, diseaseKey] of Object.entries(synonymMap)) {
        if (nameLower.includes(synonym)) {
            return CLINICAL_EDUCATION[diseaseKey] || null;
        }
    }

    return null;
}

/**
 * Mendapatkan default tindak lanjut berdasarkan diagnosis.
 * @param {string} diagnosisName
 * @returns {string}
 */
export function getDefaultTindakLanjut(diagnosisName: string): string {
    const education = getEducationForDiagnosis(diagnosisName);
    return education?.tindakLanjut || "Pulang & Rawat Jalan";
}

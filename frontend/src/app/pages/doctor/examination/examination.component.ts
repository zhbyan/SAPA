import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { PatientService } from '../../../services/patient.service';
import { searchICD10, formatICD10 } from '../../../data/icd10-database';
import { getEducationForDiagnosis, getDefaultTindakLanjut } from '../../../data/clinical-education';
import { LucideAngularModule, Edit, Brain, AlertCircle, FileCheck, Plus, Check, ArrowLeft, Printer, Save, Search } from 'lucide-angular';

@Component({
  selector: 'app-examination',
  standalone: true,
  imports: [CommonModule, FormsModule, LucideAngularModule],
  templateUrl: './examination.component.html',
  styleUrl: './examination.component.css'
})
export class ExaminationComponent implements OnInit {
  tabs = [
    { id: 's', label: 'Subjektif', letter: 'S' },
    { id: 'o', label: 'Objektif', letter: 'O' },
    { id: 'a', label: 'Assessment', letter: 'A' },
    { id: 'p', label: 'Plan', letter: 'P' },
  ];
  activeTab = 's';
  patient: any = null;
  today = new Date().toLocaleDateString('id-ID');

  // Track save status for each tab
  savedTabs: Record<string, boolean> = { s: false, o: false, a: false, p: false };

  // S: Subjektif
  subjData = { keluhanUtama: '', durasi: '', lokasiKeluhan: '', keparahan: '', faktor: '', gejala: '' };

  // O: Objektif
  objData: Record<string, string> = {
    td: '', nadi: '', suhu: '', rr: '', spo2: '',
    kesadaran: 'Compos Mentis', statusGizi: '', keadaanSakit: 'Sedang', tandaVisual: '',
    hg: '', leukosit: '', trombosit: '', hematokrit: '',
    gds: '', kolesterol: '', kreatinin: '', sgot: '',
  };

  // A: Assessment
  assData: Record<string, string> = { dxUtama: '', dxSekunder: '', dxBanding: '', statusKasus: 'Kasus Baru', prognosis: '', analisis: '' };

  // P: Plan
  planData = {
    obat: [
      { nama: '', dosis: '', frekuensi: '', durasi: '' },
      { nama: '', dosis: '', frekuensi: '', durasi: '' },
    ] as Record<string, string>[],
    edukasiItems: [] as string[],
    edukasiChecked: [] as boolean[],
    tindakLanjut: '',
    rujukTujuan: '',
    rawatAlasan: '',
  };

  // A: ICD-10 search — dictionary-based for dynamic template access
  icdSearches: Record<string, string> = { searchUtama: '', searchSekunder: '', searchBanding: '' };
  icdShowStates: Record<string, boolean> = { showUtama: false, showSekunder: false, showBanding: false };
  icdResults: Record<string, any[]> = { searchUtama: [], searchSekunder: [], searchBanding: [] };

  vitalFields = [
    { label: 'Tekanan Darah', key: 'td', unit: 'mmHg', placeholder: '120/80' },
    { label: 'Nadi', key: 'nadi', unit: 'x/mnt', placeholder: '80' },
    { label: 'Suhu', key: 'suhu', unit: '°C', placeholder: '36.5' },
    { label: 'RR', key: 'rr', unit: 'x/mnt', placeholder: '20' },
    { label: 'SpO2', key: 'spo2', unit: '%', placeholder: '98' },
  ];

  hemaFields = [
    { label: 'Hemoglobin', key: 'hg', unit: 'g/dl' },
    { label: 'Leukosit', key: 'leukosit', unit: '/μl' },
    { label: 'Trombosit', key: 'trombosit', unit: '/μl' },
    { label: 'Hematokrit', key: 'hematokrit', unit: '%' },
  ];

  kimiaFields = [
    { label: 'GDS', key: 'gds', unit: 'mg/dl' },
    { label: 'Kolesterol Total', key: 'kolesterol', unit: 'mg/dl' },
    { label: 'Kreatinin', key: 'kreatinin', unit: 'mg/dl' },
    { label: 'SGOT', key: 'sgot', unit: 'U/L' },
  ];

  constructor(private route: ActivatedRoute, private router: Router, private patientService: PatientService) {}

  ngOnInit() {
    const id = this.route.snapshot.paramMap.get('id') || '';
    this.patient = this.patientService.getPatientById(id);
    if (!this.patient) return;

    const pd = this.patient.patientData || {};
    const summary = this.patient.summary || {};
    const diagnoses = summary.diagnoses || [];
    const rasaFields = summary.rasaFields || {};
    const gejalaFromChat = (this.patient.messages || []).filter((m: any) => m.role === 'user').map((m: any) => m.text).join(', ');

    // S Auto-fill
    this.subjData = {
      keluhanUtama: rasaFields.keluhan_utama || pd.keluhan_utama || gejalaFromChat || 'Tidak ada data',
      durasi: rasaFields.durasi || pd.durasi || 'Tidak diketahui',
      lokasiKeluhan: rasaFields.lokasi_keluhan || '',
      keparahan: rasaFields.keparahan || '',
      faktor: rasaFields.riwayat_penyakit || rasaFields.riwayat_alergi
        ? `Riwayat: ${rasaFields.riwayat_penyakit || '-'}. Alergi: ${rasaFields.riwayat_alergi || '-'}`
        : 'Belum teridentifikasi',
      gejala: rasaFields.gejala_penyerta || gejalaFromChat || pd.keluhan_utama || '',
    };

    // O Auto-fill
    this.objData = { ...this.objData, td: pd.tekananDarah || '', suhu: pd.suhuBadan || '',
      statusGizi: pd.beratBadan && pd.tinggiBadan ? `Baik (BB: ${pd.beratBadan}kg, TB: ${pd.tinggiBadan}cm)` : '' };

    // A Auto-fill
    if (diagnoses.length > 0) {
      this.assData = { ...this.assData,
        dxUtama: `${diagnoses[0].icd} - ${diagnoses[0].name}`,
        dxSekunder: diagnoses[1] ? `${diagnoses[1].icd} - ${diagnoses[1].name}` : '',
        analisis: summary.resumeMedis || '' };
    }

    // P Auto-fill
    if (diagnoses.length > 0) {
      const topDx = diagnoses[0].name;
      const education = getEducationForDiagnosis(topDx);
      const defaultTL = getDefaultTindakLanjut(topDx);
      this.planData = { ...this.planData,
        edukasiItems: education?.edukasi || [],
        edukasiChecked: (education?.edukasi || []).map(() => true),
        tindakLanjut: defaultTL };
    }
  }

  get diagnoses(): any[] { return this.patient?.summary?.diagnoses || []; }

  tabColor(tabId: string): string {
    const colors: Record<string, string> = { s: '#38bfa8', o: '#3bbac7', a: '#fc8822', p: '#b327fc' };
    return colors[tabId] || '#187850';
  }

  getActiveTab() { return this.tabs.find(t => t.id === this.activeTab)!; }

  // ICD-10 search (template uses icdResults dictionary directly)

  selectICD10(field: string, entry: any, searchField: string, showField: string) {
    this.assData[field] = formatICD10(entry);
    this.icdSearches[searchField] = '';
    this.icdShowStates[showField] = false;
  }

  clearICD10(field: string, searchField: string) {
    this.assData[field] = '';
    this.icdSearches[searchField] = '';
  }

  // Template helper methods for ICD-10 dropdowns
  updateIcdResults(searchKey: string) {
    const modelMap: Record<string, string> = { searchUtama: 'dxUtama', searchSekunder: 'dxSekunder', searchBanding: 'dxBanding' };
    const query = this.icdSearches[searchKey] || this.assData[modelMap[searchKey]] || '';
    this.icdResults[searchKey] = searchICD10(query);
  }

  hideIcdDropdown(showKey: string) {
    setTimeout(() => { this.icdShowStates[showKey] = false; }, 200);
  }

  selectIcd(model: string, searchKey: string, showKey: string, entry: any) {
    this.assData[model] = formatICD10(entry);
    this.icdSearches[searchKey] = '';
    this.icdShowStates[showKey] = false;
  }

  // Subjective fields for template iteration
  subjFieldsConfig = [
    { icon: '⚠️', label: 'KELUHAN UTAMA', key: 'keluhanUtama' as keyof typeof this.subjData },
    { icon: '⏱', label: 'DURASI', key: 'durasi' as keyof typeof this.subjData },
    { icon: '📍', label: 'LOKASI KELUHAN', key: 'lokasiKeluhan' as keyof typeof this.subjData },
    { icon: '📊', label: 'KEPARAHAN', key: 'keparahan' as keyof typeof this.subjData },
    { icon: '⚡', label: 'FAKTOR / RIWAYAT', key: 'faktor' as keyof typeof this.subjData },
    { icon: '🩺', label: 'GEJALA PENYERTA', key: 'gejala' as keyof typeof this.subjData },
  ];

  addObat() { this.planData.obat.push({ nama: '', dosis: '', frekuensi: '', durasi: '' }); }
  removeObat(i: number) { this.planData.obat.splice(i, 1); }
  toggleEdukasi(i: number) { this.planData.edukasiChecked[i] = !this.planData.edukasiChecked[i]; }

  getEducationSource(): string {
    if (this.diagnoses[0]) {
      const edu = getEducationForDiagnosis(this.diagnoses[0].name);
      return edu?.sumber || 'PPK Kemenkes RI';
    }
    return 'PPK Kemenkes RI';
  }

  getEduSource(): string {
    return this.getEducationSource();
  }

  handlePartialSave() {
    this.savedTabs[this.activeTab] = true;
    const tabName = this.tabs.find(t => t.id === this.activeTab)?.label;
    alert(`Data bagian ${tabName} berhasil disimpan sementara.`);
  }

  handleComplete() {
    const unsavedTabs = this.tabs.filter(t => !this.savedTabs[t.id]);
    
    if (unsavedTabs.length > 0) {
      const tabNames = unsavedTabs.map(t => t.label).join(', ');
      alert(`Tidak dapat menyelesaikan pemeriksaan.\nBagian berikut belum disimpan: ${tabNames}\n\nMohon buka setiap bagian dan klik "Simpan" terlebih dahulu.`);
      return;
    }

    const id = this.route.snapshot.paramMap.get('id') || '';
    this.patientService.completePatient(id);
    alert('Seluruh data rekam medis SOAP telah disimpan dan pemeriksaan selesai.');
    this.router.navigate(['/doctor']);
  }
}

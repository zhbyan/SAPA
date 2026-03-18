import { Component, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../../../environments/environment';
import { PatientService } from '../../../services/patient.service';
import { LucideAngularModule, Send, FileText, Edit, User, ChevronRight, Loader2, Check } from 'lucide-angular';

@Component({
  selector: 'app-triage',
  standalone: true,
  imports: [CommonModule, FormsModule, LucideAngularModule],
  templateUrl: './triage.component.html',
  styleUrl: './triage.component.css'
})
export class TriageComponent implements AfterViewChecked {
  @ViewChild('chatEnd') chatEnd!: ElementRef;
  tabs = ['Data Pasien', 'Isi Keluhan', 'Ringkasan Pasien'];
  activeTab = 0;

  // Tab 1: Data Pasien
  patientData: Record<string, string> = {
    nik: '', namaLengkap: '', jenisKelamin: '',
    alamat: '', kelurahan: '', kecamatan: '',
    kabupaten: '', provinsi: '', kodePos: '',
    noHP: '', noBPJS: '',
    beratBadan: '', tinggiBadan: '', suhuBadan: '',
    tekananDarah: '', usia: '',
  };

  requiredFields: Record<string, string> = {
    nik: 'Nomor Induk Keluarga', namaLengkap: 'Nama Lengkap', jenisKelamin: 'Jenis Kelamin',
    alamat: 'Alamat', kelurahan: 'Kelurahan', kecamatan: 'Kecamatan',
    kabupaten: 'Kabupaten/Kota', provinsi: 'Provinsi', kodePos: 'Kode Pos',
    noHP: 'Nomor Handphone', noBPJS: 'Nomor BPJS',
    beratBadan: 'Berat Badan', tinggiBadan: 'Tinggi Badan', suhuBadan: 'Suhu Badan',
    tekananDarah: 'Tekanan Darah', usia: 'Usia',
  };
  validationErrors: Record<string, boolean> = {};

  // Tab 2: Chat
  messages: { role: string; text: string; time: string }[] = [];
  chatInput = '';
  isSending = false;
  sessionId = `session-${Date.now()}-${Math.random().toString(36).slice(2)}`;
  fieldStatus: any = null;

  // Tab 3: Summary
  summary: any = null;

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient, private router: Router, private patientService: PatientService) {}

  ngAfterViewChecked() {
    this.chatEnd?.nativeElement?.scrollIntoView({ behavior: 'smooth' });
  }

  getTime(): string {
    return new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
  }

  // Tab 1 → Tab 2
  async nextTab() {
    if (this.activeTab === 0) {
      const errors: Record<string, boolean> = {};
      const missing: string[] = [];
      for (const [field, label] of Object.entries(this.requiredFields)) {
        if (!this.patientData[field]?.toString().trim()) {
          errors[field] = true;
          missing.push(label);
        }
      }
      if (missing.length > 0) {
        this.validationErrors = errors;
        alert(`Data belum lengkap! Silakan isi:\n• ${missing.join('\n• ')}`);
        return;
      }
      this.validationErrors = {};
    }

    if (this.activeTab < 2) this.activeTab++;

    // Create RASA session when entering chat tab
    if (this.activeTab === 1 && this.messages.length === 0) {
      const name = this.patientData['namaLengkap'] || 'Kak';
      try {
        const res: any = await this.http.post(`${this.apiUrl}/chat/create`, {
          session_id: this.sessionId, message: '', nakes_name: name,
        }).toPromise();
        this.messages.push({ role: 'ai', text: res.reply, time: this.getTime() });
        if (res.field_status) this.fieldStatus = res.field_status;
      } catch {
        this.messages.push({
          role: 'ai',
          text: `Halo, ${name}! 👋\nSaya RASA, asisten klinis SAPA.\n\nSilakan ceritakan keluhan utama pasien yang akan diperiksa ya.`,
          time: this.getTime()
        });
      }
    }
  }

  async sendMessage() {
    if (!this.chatInput.trim() || this.isSending) return;
    const userMsg = { role: 'user', text: this.chatInput.trim(), time: this.getTime() };
    this.messages.push(userMsg);
    this.chatInput = '';
    this.isSending = true;

    try {
      const res: any = await this.http.post(`${this.apiUrl}/chat`, {
        session_id: this.sessionId, message: userMsg.text, nakes_name: this.patientData['namaLengkap'] || 'Kak',
      }).toPromise();
      this.messages.push({ role: 'ai', text: res.reply, time: this.getTime() });
      if (res.field_status) this.fieldStatus = res.field_status;
      if (res.analysis) this.summary = { ...this.summary, ...res.analysis };
    } catch {
      this.messages.push({ role: 'ai', text: 'Maaf Kak, ada gangguan sementara 🙏 Silakan coba lagi ya.', time: this.getTime() });
    } finally {
      this.isSending = false;
    }
  }

  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  async generateReport() {
    this.isSending = true;
    try {
      const complaintText = this.messages.filter(m => m.role === 'user').map(m => m.text).join('. ');
      let mlDx: any[] = [];
      try {
        const mlRes: any = await this.http.post(`${this.apiUrl}/predict`, { text: complaintText }).toPromise();
        mlDx = (mlRes?.predictions || []).map((d: any) => ({
          name: d.disease || '—', icd: d.icd10 || '—',
          score: typeof d.probability === 'number' ? Math.round(d.probability * 10) / 10 : parseFloat(d.probability) || 0,
        }));
      } catch (e) { console.warn('ML prediction failed:', e); }

      let rasaFields: any = {};
      let resumeMedis = '';
      let rasaDiagnoses: any[] = [];
      try {
        const chatRes: any = await this.http.post(`${this.apiUrl}/chat/generate-report`, { session_id: this.sessionId }).toPromise();
        const analysis = chatRes.analysis || {};
        rasaFields = chatRes.field_status?.required || {};
        resumeMedis = analysis.resume_medis || chatRes.reply || '';
        rasaDiagnoses = (analysis.diagnoses || []).map((d: any) => ({
          name: d.name || '—', icd: d.icd10 || '—',
          score: d.probability === 'Tinggi' ? 75 : d.probability === 'Sedang' ? 50 : d.probability === 'Rendah' ? 25 : 0,
        }));
      } catch (e) { console.warn('RASA report failed:', e); }

      const finalDiagnoses = mlDx.length > 0 ? mlDx : rasaDiagnoses;
      const genderText = this.patientData['jenisKelamin'] === 'L' ? 'laki-laki' : 'perempuan';

      this.summary = {
        resumeMedis: resumeMedis || `Pasien ${genderText} ${this.patientData['usia'] || '—'} tahun datang dengan keluhan: ${complaintText.substring(0, 200)}`,
        icdTags: finalDiagnoses.slice(0, 5).map((d: any) => ({ code: d.icd || '—', label: d.name || '—' })),
        diagnoses: finalDiagnoses,
        rasaFields: {
          keluhan_utama: rasaFields.keluhan_utama || complaintText || '',
          durasi: rasaFields.durasi || '', lokasi_keluhan: rasaFields.lokasi_keluhan || '',
          keparahan: rasaFields.keparahan || '', gejala_penyerta: rasaFields.gejala_penyerta || '',
          riwayat_penyakit: rasaFields.riwayat_penyakit || '', riwayat_alergi: rasaFields.riwayat_alergi || '',
        },
      };
      this.activeTab = 2;
    } catch (err) {
      console.error('Generate report error:', err);
      const complaintText = this.messages.filter(m => m.role === 'user').map(m => m.text).join('. ');
      let fallbackDx: any[] = [];
      try {
        const mlRes: any = await this.http.post(`${this.apiUrl}/predict`, { text: complaintText }).toPromise();
        fallbackDx = (mlRes?.predictions || []).map((d: any) => ({
          name: d.disease || '—', icd: d.icd10 || '—',
          score: typeof d.probability === 'number' ? Math.round(d.probability * 10) / 10 : parseFloat(d.probability) || 0,
        }));
      } catch { /* truly failed */ }
      const genderText = this.patientData['jenisKelamin'] === 'L' ? 'laki-laki' : 'perempuan';
      this.summary = {
        resumeMedis: `Pasien ${genderText} ${this.patientData['usia'] || '—'} tahun datang dengan keluhan: ${complaintText.substring(0, 200)}`,
        icdTags: fallbackDx.slice(0, 5).map((d: any) => ({ code: d.icd, label: d.name })),
        diagnoses: fallbackDx,
        rasaFields: { keluhan_utama: complaintText || '', durasi: '', lokasi_keluhan: '', keparahan: '', gejala_penyerta: '', riwayat_penyakit: '', riwayat_alergi: '' },
      };
      this.activeTab = 2;
    } finally {
      this.isSending = false;
    }
  }

  sendToDoctor() {
    if (!this.summary?.diagnoses || this.summary.diagnoses.length === 0) {
      alert('Tidak dapat mengirim. Prediksi diagnosis AI belum tersedia atau gagal. Silakan coba buat laporan kembali.');
      return;
    }
    const newPatient = {
      id: Date.now().toString(),
      name: this.patientData['namaLengkap'] || 'Pasien Anonim',
      time: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }),
      severity: this.summary?.diagnoses?.[0]?.score >= 60 ? 'high' : this.summary?.diagnoses?.[0]?.score >= 30 ? 'medium' : 'low',
      predicted: this.summary?.diagnoses?.[0]?.name || 'Belum diketahui',
      patientData: this.patientData,
      summary: this.summary,
      messages: this.messages,
    };
    this.patientService.addPatient(newPatient);
    alert('Data pasien berhasil dikirim ke antrian Dokter!');
    this.router.navigate(['/']);
  }

  getFieldEntries(): [string, any][] {
    return this.fieldStatus?.required ? Object.entries(this.fieldStatus.required) : [];
  }

  getBarGradient(i: number): string {
    const gradients = [
      'linear-gradient(to top, #ef4444, #f87171)',
      'linear-gradient(to top, #fb923c, #fdba74)',
      'linear-gradient(to top, #10b981, #6ee7b7)',
    ];
    return gradients[i] || gradients[2];
  }

  getBarGlow(i: number): string {
    const glows = [
      '0 4px 14px -2px rgba(239,68,68,0.35)',
      '0 4px 14px -2px rgba(251,146,60,0.3)',
      '0 4px 14px -2px rgba(16,185,129,0.3)',
    ];
    return glows[i] || glows[2];
  }

  getBarHeight(score: number): number {
    return Math.max(score * 0.85, 16);
  }

  truncate(text: string, len: number): string {
    return text.length > len ? text.slice(0, len) + '…' : text;
  }

  getRegistrationDate(): string {
    return new Date().toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  }

  getGenderLabel(): string {
    return this.patientData['jenisKelamin'] === 'L' ? 'Laki-Laki' : this.patientData['jenisKelamin'] === 'P' ? 'Perempuan' : '—';
  }

  getAddressLabel(): string {
    return [this.patientData['alamat'], this.patientData['kabupaten'], this.patientData['provinsi']].filter(Boolean).join(', ') || '—';
  }

  getNikMasked(): string {
    const nik = this.patientData['nik'];
    return nik ? `${nik.substring(0, 6)}xxxxxxxx${nik.slice(-1)}` : '—';
  }

  getPatientNumber(): string {
    return String(Date.now()).slice(-6);
  }

  getFirstName(): string {
    return this.patientData['namaLengkap']?.split(' ')[0] || 'Kak';
  }

  getScoreClass(score: number): string {
    if (score >= 60) return 'score-high';
    if (score >= 30) return 'score-medium';
    return 'score-low';
  }
}

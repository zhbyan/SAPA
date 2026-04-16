import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { PatientService } from '../../../services/patient.service';
import { LucideAngularModule } from 'lucide-angular';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  waitingPatients: any[] = [];
  completedPatients: any[] = [];
  
  // Status filter saat ini: 'antrian' atau 'selesai'
  activeTab: 'antrian' | 'selesai' = 'antrian';
  
  // Variabel untuk menyimpan data pasien yang akan ditampilkan di popup modal
  selectedPatient: any = null;
  
  today = new Date().toLocaleDateString('id-ID', { day: '2-digit', month: '2-digit', year: 'numeric' });

  constructor(private router: Router, private patientService: PatientService) {}

  ngOnInit() {
    // Mengambil data dari localStorage saat halaman pertama kali dimuat
    this.waitingPatients = this.patientService.getWaitingPatients();
    this.completedPatients = this.patientService.getCompletedPatients();
  }

  // ==========================================
  // FUNGSI NAVIGASI & FILTER TAB
  // ==========================================

  setTab(tab: 'antrian' | 'selesai') {
    this.activeTab = tab;
  }

  // Mengembalikan list pasien sesuai tab yang sedang aktif
  get currentPatients() {
    return this.activeTab === 'antrian' ? this.waitingPatients : this.completedPatients;
  }

  get totalPasien() { 
    return this.waitingPatients.length + this.completedPatients.length; 
  }
  
  get dalamAntrian() { 
    return this.waitingPatients.filter((p: any) => p.severity === 'high').length || Math.min(this.waitingPatients.length, 2); 
  }

  // ==========================================
  // FUNGSI AKSI (KLIK PASIEN)
  // ==========================================

  openPatient(patient: any) {
    if (this.activeTab === 'antrian') {
      // Jika pasien dari antrian diklik, arahkan ke halaman pemeriksaan/isian
      this.router.navigate(['/doctor/examine', patient.id], { queryParams: { status: this.activeTab } });
    } else {
      // Jika pasien dari tab selesai diklik, buka Modal Popup Detail
      this.selectedPatient = patient;
      const modal = document.getElementById('detail_patient_modal') as HTMLDialogElement;
      if (modal) {
        modal.showModal();
      }
    }
  }

  closeDetailModal() {
    const modal = document.getElementById('detail_patient_modal') as HTMLDialogElement;
    if (modal) {
      modal.close();
    }
    // Hapus data yang dipilih setelah animasi modal menutup (200ms) agar tidak "berkedip"
    setTimeout(() => {
      this.selectedPatient = null;
    }, 200);
  }

  // ==========================================
  // FUNGSI BANTUAN UI (HELPER METHODS)
  // ==========================================

  getDiagnoses(patient: any): any[] {
    return patient?.summary?.diagnoses?.slice(0, 3) || [];
  }

  getGejala(patient: any): string {
    const gejala =
      patient.patientData?.keluhan_utama ||
      patient.summary?.rasaFields?.keluhan_utama ||
      '';
    if (!gejala) return '';
    return gejala.length > 80 ? gejala.slice(0, 80) + '...' : gejala;
  }

  getPatientNumber(patient: any): string {
    return String(patient.id).slice(-2);
  }

  getPatientId6(patient: any): string {
    return String(patient.id).slice(-6);
  }

  getBarHeight(score: number): number {
    return Math.max(score * 0.85, 16);
  }

  getBarGradient(i: number): string {
    const g = [
      'linear-gradient(to top, #ef4444, #f87171)', 
      'linear-gradient(to top, #fb923c, #fdba74)', 
      'linear-gradient(to top, #10b981, #6ee7b7)'
    ];
    return g[i] || g[2];
  }

  getBarGlow(i: number): string {
    const g = [
      '0 4px 14px -2px rgba(239,68,68,0.35)', 
      '0 4px 14px -2px rgba(251,146,60,0.3)', 
      '0 4px 14px -2px rgba(16,185,129,0.3)'
    ];
    return g[i] || g[2];
  }

  truncateName(name: string): string {
    return name.length > 12 ? name.slice(0, 12) + '…' : name;
  }
}
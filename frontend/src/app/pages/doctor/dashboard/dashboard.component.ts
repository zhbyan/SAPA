import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { PatientService } from '../../../services/patient.service';
import { LucideAngularModule, ArrowUpRight, Calendar, X, Download } from 'lucide-angular'; // <-- Download ditambahkan

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  // Tambahkan icon yang digunakan ke variabel lokal agar aman dirender HTML
  readonly icons = { ArrowUpRight, Calendar, X, Download };

  waitingPatients: any[] = [];
  completedPatients: any[] = [];
  
  activeTab: 'antrian' | 'selesai' = 'antrian';
  selectedPatient: any = null;
  
  today = new Date().toLocaleDateString('id-ID', { day: '2-digit', month: '2-digit', year: 'numeric' });

  constructor(private router: Router, private patientService: PatientService) {}

  ngOnInit() {
    this.waitingPatients = this.patientService.getWaitingPatients();
    this.completedPatients = this.patientService.getCompletedPatients();
  }

  setTab(tab: 'antrian' | 'selesai') {
    this.activeTab = tab;
  }

  get currentPatients() {
    return this.activeTab === 'antrian' ? this.waitingPatients : this.completedPatients;
  }

  get totalPasien() { 
    return this.waitingPatients.length + this.completedPatients.length; 
  }
  
  get dalamAntrian() { 
    return this.waitingPatients.filter((p: any) => p.severity === 'high').length || Math.min(this.waitingPatients.length, 2); 
  }

  openPatient(patient: any) {
    if (this.activeTab === 'antrian') {
      this.router.navigate(['/doctor/examine', patient.id], { queryParams: { status: this.activeTab } });
    } else {
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
    setTimeout(() => {
      this.selectedPatient = null;
    }, 200);
  }

  // ==========================================
  // FUNGSI DOWNLOAD / CETAK PDF (BARU)
  // ==========================================
  downloadPDF() {
    const content = document.getElementById('printable-soap')?.innerHTML;
    if (!content) return;

    // Membuka jendela baru khusus untuk di-print
    const printWindow = window.open('', '_blank', 'height=800,width=1000');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Rekam Medis - ${this.selectedPatient?.name || 'Pasien'}</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
              @media print {
                body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
              }
            </style>
          </head>
          <body class="p-10 font-sans text-slate-800">
            <div class="max-w-4xl mx-auto">
              <div class="border-b-2 border-slate-800 pb-4 mb-6 flex justify-between items-end">
                <div>
                  <h1 class="text-3xl font-black text-slate-900">RS Budiman</h1>
                  <p class="text-slate-500 mt-1">Laporan Rekam Medis (SOAP)</p>
                </div>
                <div class="text-right text-sm text-slate-500">
                  Tanggal Cetak: ${new Date().toLocaleDateString('id-ID')}
                </div>
              </div>
              
              ${content}
              
              <div class="mt-16 pt-8 border-t border-slate-200 text-right">
                <p class="text-slate-500 mb-16">Dokter Pemeriksa,</p>
                <p class="font-bold text-slate-800">(_______________________)</p>
              </div>
            </div>
            
            <script>
              // Tunggu 1 detik agar Tailwind selesai dimuat, lalu panggil menu Print browser
              setTimeout(() => {
                window.print();
                window.close();
              }, 1000);
            </script>
          </body>
        </html>
      `);
      printWindow.document.close();
    }
  }

  // Helper Methods
  getDiagnoses(patient: any): any[] { return patient?.summary?.diagnoses?.slice(0, 3) || []; }
  getGejala(patient: any): string {
    const gejala = patient.patientData?.keluhan_utama || patient.summary?.rasaFields?.keluhan_utama || '';
    if (!gejala) return '';
    return gejala.length > 80 ? gejala.slice(0, 80) + '...' : gejala;
  }
  getPatientNumber(patient: any): string { return String(patient.id).slice(-2); }
  getPatientId6(patient: any): string { return String(patient.id).slice(-6); }
  getBarHeight(score: number): number { return Math.max(score * 0.85, 16); }
  getBarGradient(i: number): string {
    const g = ['linear-gradient(to top, #ef4444, #f87171)', 'linear-gradient(to top, #fb923c, #fdba74)', 'linear-gradient(to top, #10b981, #6ee7b7)'];
    return g[i] || g[2];
  }
  getBarGlow(i: number): string {
    const g = ['0 4px 14px -2px rgba(239,68,68,0.35)', '0 4px 14px -2px rgba(251,146,60,0.3)', '0 4px 14px -2px rgba(16,185,129,0.3)'];
    return g[i] || g[2];
  }
}
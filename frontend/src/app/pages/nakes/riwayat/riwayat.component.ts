import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PatientService } from '../../../services/patient.service';

@Component({
  selector: 'app-riwayat',
  standalone: true,
  imports: [CommonModule], // Dibuat super aman, tanpa modul tambahan yang bikin crash
  templateUrl: './riwayat.component.html',
  styleUrl: './riwayat.component.css'
})
export class RiwayatComponent implements OnInit {
  completedPatients: any[] = [];
  selectedHistoryPatient: any = null;

  constructor(private patientService: PatientService) {}

  ngOnInit() {
    // Tarik data dengan pengamanan ganda
    const data = this.patientService.getCompletedPatients();
    this.completedPatients = data ? data : [];
  }

  openHistoryDetail(patient: any) {
    this.selectedHistoryPatient = patient;
    const modal = document.getElementById('history_detail_modal') as HTMLDialogElement;
    if (modal) modal.showModal();
  }

  closeHistoryDetail() {
    const modal = document.getElementById('history_detail_modal') as HTMLDialogElement;
    if (modal) modal.close();
    setTimeout(() => { this.selectedHistoryPatient = null; }, 200);
  }

  getPatientId6(patient: any): string {
    return patient && patient.id ? String(patient.id).slice(-6) : '-';
  }

  // FUNGSI CETAK PDF
  downloadPDF() {
    const content = document.getElementById('printable-triage')?.innerHTML;
    if (!content) return;

    const printWindow = window.open('', '_blank', 'height=800,width=1000');
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>Data Triage - ${this.selectedHistoryPatient?.name || 'Pasien'}</title>
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
                  <p class="text-slate-500 mt-1">Laporan Data Triage (Keperawatan)</p>
                </div>
                <div class="text-right text-sm text-slate-500">
                  Tanggal Cetak: ${new Date().toLocaleDateString('id-ID')}
                </div>
              </div>
              
              ${content}
              
              <div class="mt-16 pt-8 border-t border-slate-200 text-right">
                <p class="text-slate-500 mb-16">Tenaga Kesehatan,</p>
                <p class="font-bold text-slate-800">(_______________________)</p>
              </div>
            </div>
            <script>
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
}
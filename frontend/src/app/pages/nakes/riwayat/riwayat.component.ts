import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PatientService } from '../../../services/patient.service';
import { LucideAngularModule } from 'lucide-angular';

@Component({
  selector: 'app-riwayat',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  templateUrl: './riwayat.component.html'
})
export class RiwayatComponent implements OnInit {
  completedPatients: any[] = [];
  selectedHistoryPatient: any = null;

  constructor(private patientService: PatientService) {}

  ngOnInit() {
    this.completedPatients = this.patientService.getCompletedPatients() || [];
  }

  // Membuka popup Detail Triage di halaman ini
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
}
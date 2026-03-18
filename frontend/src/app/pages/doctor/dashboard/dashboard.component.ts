import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { PatientService } from '../../../services/patient.service';
import { LucideAngularModule, Calendar, ArrowUpRight } from 'lucide-angular';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, LucideAngularModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  patients: any[] = [];
  completedCount = 0;
  today = new Date().toLocaleDateString('id-ID', { day: '2-digit', month: '2-digit', year: 'numeric' });

  constructor(private router: Router, private patientService: PatientService) {}

  ngOnInit() {
    this.patients = this.patientService.getWaitingPatients();
    this.completedCount = this.patientService.getCompletedPatients().length;
  }

  get totalPasien() { return this.patients.length + this.completedCount; }
  get dalamAntrian() { return this.patients.filter((p: any) => p.severity === 'high').length || Math.min(this.patients.length, 2); }

  openPatient(patient: any) {
    this.router.navigate(['/doctor/examine', patient.id]);
  }

  getDiagnoses(patient: any): any[] {
    return patient.summary?.diagnoses?.slice(0, 3) || [];
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
    const g = ['linear-gradient(to top, #ef4444, #f87171)', 'linear-gradient(to top, #fb923c, #fdba74)', 'linear-gradient(to top, #10b981, #6ee7b7)'];
    return g[i] || g[2];
  }

  getBarGlow(i: number): string {
    const g = ['0 4px 14px -2px rgba(239,68,68,0.35)', '0 4px 14px -2px rgba(251,146,60,0.3)', '0 4px 14px -2px rgba(16,185,129,0.3)'];
    return g[i] || g[2];
  }

  truncateName(name: string): string {
    return name.length > 12 ? name.slice(0, 12) + '…' : name;
  }
}

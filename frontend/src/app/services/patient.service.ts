import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class PatientService {

  getWaitingPatients(): any[] {
    return JSON.parse(localStorage.getItem('sapa_patients') || '[]');
  }

  getCompletedPatients(): any[] {
    return JSON.parse(localStorage.getItem('sapa_completed') || '[]');
  }

  addPatient(patient: any): void {
    const existing = this.getWaitingPatients();
    localStorage.setItem('sapa_patients', JSON.stringify([patient, ...existing]));
  }

  getPatientById(id: string): any | null {
    const patients = this.getWaitingPatients();
    return patients.find((p: any) => String(p.id) === String(id)) || null;
  }

  completePatient(id: string): void {
    const waiting = this.getWaitingPatients();
    const completed = this.getCompletedPatients();
    const idx = waiting.findIndex((p: any) => String(p.id) === String(id));
    if (idx !== -1) {
      const [done] = waiting.splice(idx, 1);
      done.soapCompleted = true;
      done.completedAt = new Date().toISOString();
      completed.unshift(done);
      localStorage.setItem('sapa_patients', JSON.stringify(waiting));
      localStorage.setItem('sapa_completed', JSON.stringify(completed));
    }
  }
}

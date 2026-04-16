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
    const waiting = this.getWaitingPatients();
    const completed = this.getCompletedPatients();
    const allPatients = [...waiting, ...completed];
    return allPatients.find((p: any) => String(p.id) === String(id)) || null;
  }

  // FUNGSI BARU: Simpan SOAP dan langsung pindahkan ke Selesai dengan aman
  saveSOAPAndComplete(id: string, soapData: any): void {
    const waiting = this.getWaitingPatients();
    const completed = this.getCompletedPatients();
    
    // Cari pasien di antrean
    const idx = waiting.findIndex((p: any) => String(p.id) === String(id));
    
    if (idx !== -1) {
      // 1. Ambil data pasien
      let patient = waiting[idx];
      
      // 2. Gabungkan data lama dengan data SOAP baru
      patient = { 
        ...patient, 
        ...soapData, 
        soapCompleted: true, 
        completedAt: new Date().toISOString() 
      };
      
      // 3. Hapus dari antrean, masukkan ke daftar Selesai
      waiting.splice(idx, 1);
      completed.unshift(patient);
      
      // 4. Simpan ke LocalStorage secara bersamaan
      localStorage.setItem('sapa_patients', JSON.stringify(waiting));
      localStorage.setItem('sapa_completed', JSON.stringify(completed));
    }
  }

  // Fungsi lama tetap ada untuk kompatibilitas
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
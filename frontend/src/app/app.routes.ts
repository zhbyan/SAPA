import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', loadComponent: () => import('./pages/login/login.component').then(m => m.LoginComponent) },
  {
    path: '',
    loadComponent: () => import('./layouts/nurse-layout/nurse-layout.component').then(m => m.NurseLayoutComponent),
    canActivate: [authGuard],
    data: { role: 'nakes' },
    children: [
      { path: '', loadComponent: () => import('./pages/nakes/triage/triage.component').then(m => m.TriageComponent) },
    ]
  },
  {
    path: 'doctor',
    loadComponent: () => import('./layouts/doctor-layout/doctor-layout.component').then(m => m.DoctorLayoutComponent),
    canActivate: [authGuard],
    data: { role: 'dokter' },
    children: [
      { path: '', loadComponent: () => import('./pages/doctor/dashboard/dashboard.component').then(m => m.DashboardComponent) },
      { path: 'examine/:id', loadComponent: () => import('./pages/doctor/examination/examination.component').then(m => m.ExaminationComponent) },
    ]
  },
  { path: '**', redirectTo: 'login' }
];

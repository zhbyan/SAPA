import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { LucideAngularModule, Home, Settings, HelpCircle, LogOut, Stethoscope, Search, Bell } from 'lucide-angular';

@Component({
  selector: 'app-doctor-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, FormsModule, LucideAngularModule],
  templateUrl: './doctor-layout.component.html',
  styleUrl: './doctor-layout.component.css'
})
export class DoctorLayoutComponent {
  readonly icons = { Home, Settings, HelpCircle, LogOut, Stethoscope, Search, Bell };
  menuGroups: Record<string, any[]> = {
    'MENU': [{ label: 'Dashboard', icon: 'home', path: '/doctor' }],
    'UMUM': [{ label: 'Pengaturan', icon: 'settings', path: '/doctor/settings' }, { label: 'Bantuan', icon: 'help-circle', path: '/doctor/help' }],
  };
  searchQuery = '';

  constructor(public auth: AuthService, public router: Router) {}

  get initials() { return this.auth.getInitials(); }
  isActive(path: string): boolean { return this.router.url === path; }
  logout() { this.auth.logout(); }
  objectEntries(obj: Record<string, any[]>): [string, any[]][] { return Object.entries(obj); }
}

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LucideAngularModule, Home, ClipboardList, HelpCircle, Settings, LogOut, Bell, Stethoscope } from 'lucide-angular';

@Component({
  selector: 'app-nurse-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, LucideAngularModule],
  templateUrl: './nurse-layout.component.html',
  styleUrl: './nurse-layout.component.css'
})
export class NurseLayoutComponent {
  readonly icons = { Home, ClipboardList, HelpCircle, Settings, LogOut, Bell, Stethoscope };
  menuGroups: Record<string, { label: string; icon: string; path: string }[]> = {
    'MENU': [{ label: 'Dasbor', icon: 'home', path: '/' }],
    'ADMINISTRASI': [{ label: 'Pendaftaran Pasien', icon: 'clipboard-list', path: '/' }, { label: 'Bantuan', icon: 'help-circle', path: '/' }],
    'UMUM': [{ label: 'Pengaturan', icon: 'settings', path: '/' }, { label: 'Bantuan', icon: 'help-circle', path: '/' }],
  };

  constructor(public auth: AuthService, public router: Router) {}

  get initials() { return this.auth.getInitials(); }

  isActive(path: string): boolean { return this.router.url === path; }

  logout() { this.auth.logout(); }

  objectEntries(obj: Record<string, any[]>): [string, any[]][] { return Object.entries(obj); }
}

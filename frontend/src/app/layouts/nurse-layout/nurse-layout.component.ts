import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LucideAngularModule, Home, ClipboardList, HelpCircle, Settings, LogOut, Bell, Stethoscope, History } from 'lucide-angular';

@Component({
  selector: 'app-nurse-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, LucideAngularModule],
  templateUrl: './nurse-layout.component.html',
  styleUrl: './nurse-layout.component.css'
})
export class NurseLayoutComponent {
  readonly icons = { Home, ClipboardList, HelpCircle, Settings, LogOut, Bell, Stethoscope, History };
  
  menuGroups = [
    {
      title: 'MENU',
      items: [
        { label: 'Dasbor', icon: 'home', path: '/' }
      ]
    },
    {
      title: 'ADMINISTRASI',
      items: [
        // Path diperbaiki menjadi /pendaftaran
        { label: 'Pendaftaran Pasien', icon: 'clipboard-list', path: '/pendaftaran' },
        { label: 'Riwayat Pasien', icon: 'user', path: '/riwayat' } 
      ]
    },
    {
      title: 'UMUM',
      items: [
        { label: 'Pengaturan', icon: 'settings', path: '/pengaturan' },
        { label: 'Bantuan', icon: 'help-circle', path: '/bantuan' }
      ]
    }
  ];

  constructor(
    public auth: AuthService, 
    public router: Router
  ) {}

  get initials() { return this.auth.getInitials(); }
  
  // Logika active menu yang benar
  isActive(item: any): boolean { 
    return this.router.url === item.path; 
  }
  
  logout() { this.auth.logout(); }
  
  handleMenuClick(item: any) {
    if (item.path) {
      this.router.navigate([item.path]);
    }
  }
}
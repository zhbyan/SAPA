import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

export interface User {
  username: string;
  role: 'nakes' | 'dokter';
  name: string;
  nip: string;
}

interface UserRecord extends User {
  password: string;
}

const USERS: UserRecord[] = [
  { username: 'nakes1', password: 'nakes123', role: 'nakes', name: 'Suster Ani', nip: '198901012020012001' },
  { username: 'nakes2', password: 'nakes123', role: 'nakes', name: 'Perawat Budi', nip: '199005052021011002' },
  { username: 'dokter1', password: 'dokter123', role: 'dokter', name: 'dr. Andi Wijaya, Sp.PD', nip: '197508082010011003' },
  { username: 'dokter2', password: 'dokter123', role: 'dokter', name: 'dr. Sari Rahmawati', nip: '198203152015022004' },
];

@Injectable({ providedIn: 'root' })
export class AuthService {
  user: User | null = null;

  constructor(private router: Router) {
    const saved = localStorage.getItem('sapa_user');
    if (saved) {
      try { this.user = JSON.parse(saved); } catch { this.user = null; }
    }
  }

  get isLoggedIn(): boolean { return !!this.user; }

  login(username: string, password: string): { success: boolean; error?: string; user?: User } {
    const found = USERS.find(u => u.username === username && u.password === password);
    if (found) {
      const { password: _, ...userData } = found;
      this.user = userData as User;
      localStorage.setItem('sapa_user', JSON.stringify(this.user));
      return { success: true, user: this.user };
    }
    return { success: false, error: 'Username atau password salah' };
  }

  logout(): void {
    this.user = null;
    localStorage.removeItem('sapa_user');
    this.router.navigate(['/login']);
  }

  getInitials(): string {
    if (!this.user?.name) return 'NK';
    return this.user.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  }
}

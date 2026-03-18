import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { LucideAngularModule, Stethoscope, LogIn, Eye, EyeOff, AlertCircle } from 'lucide-angular';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, LucideAngularModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  readonly icons = { Stethoscope, LogIn, Eye, EyeOff, AlertCircle };
  username = '';
  password = '';
  showPassword = false;
  error = '';
  isLoading = false;

  constructor(private auth: AuthService, private router: Router) {
    if (auth.isLoggedIn) {
      router.navigate([auth.user?.role === 'dokter' ? '/doctor' : '/']);
    }
  }

  async handleSubmit() {
    this.error = '';
    this.isLoading = true;
    await new Promise(r => setTimeout(r, 500));
    const result = this.auth.login(this.username, this.password);
    if (result.success) {
      this.router.navigate([result.user?.role === 'dokter' ? '/doctor' : '/']);
    } else {
      this.error = result.error || 'Login gagal';
    }
    this.isLoading = false;
  }

  quickLogin(user: string, pass: string) {
    this.username = user;
    this.password = pass;
  }
}

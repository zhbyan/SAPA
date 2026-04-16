import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { PatientService } from '../../../services/patient.service';
import { LucideAngularModule, Users, CheckCircle, Clock, ArrowRight, UserPlus } from 'lucide-angular';

@Component({
  selector: 'app-dashboard-nakes',
  standalone: true,
  imports: [CommonModule, RouterLink, LucideAngularModule],
  templateUrl: './dashboard-nakes.component.html',
  styleUrl: './dashboard-nakes.component.css'
})
export class DashboardNakesComponent implements OnInit {
  readonly icons = { Users, CheckCircle, Clock, ArrowRight, UserPlus };
  
  waitingCount = 0;
  completedCount = 0;
  today = new Date().toLocaleDateString('id-ID', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });

  constructor(public auth: AuthService, private patientService: PatientService) {}

  ngOnInit() {
    this.waitingCount = this.patientService.getWaitingPatients().length;
    this.completedCount = this.patientService.getCompletedPatients().length;
  }
}
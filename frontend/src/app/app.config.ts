import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';
import { LUCIDE_ICONS, LucideIconProvider } from 'lucide-angular';
import {
  Stethoscope, LogIn, Eye, EyeOff, AlertCircle,
  Home, ClipboardList, HelpCircle, Settings, LogOut, Bell,
  Search, Calendar, ArrowUpRight,
  Send, FileText, Edit, User, ChevronRight, Loader2, Check,
  Brain, FileCheck, Plus, ArrowLeft, Printer, Save,
} from 'lucide-angular';

const usedIcons = {
  Stethoscope, LogIn, Eye, EyeOff, AlertCircle,
  Home, ClipboardList, HelpCircle, Settings, LogOut, Bell,
  Search, Calendar, ArrowUpRight,
  Send, FileText, Edit, User, ChevronRight, Loader2, Check,
  Brain, FileCheck, Plus, ArrowLeft, Printer, Save,
};

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
    { provide: LUCIDE_ICONS, multi: true, useValue: new LucideIconProvider(usedIcons) },
  ]
};

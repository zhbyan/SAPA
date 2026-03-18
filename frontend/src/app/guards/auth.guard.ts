import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const authGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (!auth.isLoggedIn) {
    router.navigate(['/login']);
    return false;
  }

  const allowedRole = route.data?.['role'] as string | undefined;
  if (allowedRole && auth.user?.role !== allowedRole) {
    router.navigate([auth.user?.role === 'dokter' ? '/doctor' : '/']);
    return false;
  }

  return true;
};

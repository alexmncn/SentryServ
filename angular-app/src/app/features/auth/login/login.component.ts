import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { trigger, style, transition, animate } from '@angular/animations';

import { AuthService } from '../../../core/services/auth/auth.service';
import { LoadingOverlayComponent } from '../../../shared/loading-overlay/loading-overlay.component';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterOutlet, CommonModule, ReactiveFormsModule, LoadingOverlayComponent],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  animations: [
    trigger('errorAnimation', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate('150ms ease-in', style({ height: '*', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('0ms ease-out', style({ height: '0', opacity: 0 }))
      ])
    ])
  ]
})
export class LoginComponent {
  loginForm: FormGroup;

  passwordMinLen = 4;

  defaultRedirectRoute = '/home';

  // loading overlay
  isLoading = false;
  loadingInfo = '';



  constructor(private authService: AuthService, private router: Router, private fb: FormBuilder) { 
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(this.passwordMinLen)]]
    });
  }

  sendLogin() {
    if (this.loginForm.valid) {
      this.isLoading = true;
      this.loadingInfo = 'Proce sando...';

      this.authService.login(this.loginForm.value.username, this.loginForm.value.password)
        .subscribe({
          next: (response) => {
            // Save the token with AuthService
            this.authService.storeToken(response.token, response.expires_at);
            this.authService.setUsername(response.username);

            // redirect
            const redirectUrl = this.authService.redirectUrl || this.defaultRedirectRoute;
            this.router.navigate([redirectUrl]);
            this.isLoading = false;
          },
          error: (error) => {
            console.log(error.error.message);
            this.isLoading = false;
          },
          complete: () => {
          }
        });
    }
  }
}

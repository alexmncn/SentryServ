import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { trigger, style, transition, animate } from '@angular/animations';

import { AuthService } from '../../../core/services/auth/auth.service';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterOutlet, CommonModule, ReactiveFormsModule],
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


  constructor(private authService: AuthService, private router: Router, private fb: FormBuilder) { 
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(this.passwordMinLen)]]
    });
  }

  sendLogin() {
    if (this.loginForm.valid) {
      console.log(this.loginForm.value);
      this.authService.login(this.loginForm.value.username, this.loginForm.value.password)
        .subscribe({
          next: (response) => {
            console.log(response);
            // Save the token with AuthService
            this.authService.storeToken(response.token, response.expires_at);
            this.authService.setUsername(response.username);
            this.router.navigate(['home']);
          },
          error: (error) => {
            alert(error.error.message);
          },
          complete: () => {
          }
        });
  
      }
    }
}

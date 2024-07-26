import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { trigger, style, transition, animate } from '@angular/animations';

import { AuthService } from '../../../core/services/auth/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [RouterOutlet, CommonModule, ReactiveFormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css',
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
export class RegisterComponent {
  registerForm: FormGroup;

  passwordMinLen = 4;
  password_match = true;

  defaultRedirectRoute = 'login'


  constructor(private authService: AuthService, private router: Router, private fb: FormBuilder) { 
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(this.passwordMinLen)]],
      confirm_password: ['', Validators.required]
    });
  }

  sendRegister() {
    if (this.registerForm.valid) {
      if (this.registerForm.value.password == this.registerForm.value.confirm_password) {
        this.authService.register(this.registerForm.value.username, this.registerForm.value.password)
          .subscribe({
            next: (response) => {
              console.log(response);
              alert(response.message)
              // redirect
              const redirectUrl = this.authService.redirectUrl || this.defaultRedirectRoute;
              this.router.navigate([redirectUrl]);
            },
            error: (error) => {
              alert(error.error.message);
            },
            complete: () => {
            }
          });
      } else {
        alert('las contraseñas no coinciden');
        this.password_match = false;
      }

    }
  }
}

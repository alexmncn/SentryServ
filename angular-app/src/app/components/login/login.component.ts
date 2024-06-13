import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth/auth.service';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [RouterOutlet, CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  formData = {
    username: '',
    password: ''
  };

  constructor(private authService: AuthService, private router: Router) { }

  login(): void {
    this.authService.login(this.formData.username, this.formData.password)
      .subscribe({
        next: (response) => {
          // Save the token with AuthService
          this.authService.storeToken(response.token);
          this.authService.setUsername(response.username);
          this.router.navigate(['home']);
        },
        error: (error) => {
          console.error(error.error.message);
        },
        complete: () => {
        }
      });
  }
}

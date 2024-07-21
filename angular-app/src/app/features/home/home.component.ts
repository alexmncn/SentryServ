import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';

import { AuthService } from '../../core/services/auth/auth.service';


@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  public username: any;

  constructor(private authService: AuthService) { }

  ngOnInit(): void {
    this.username = this.authService.getUsername();
  }

  logout(): void {
    this.authService.logoutReq()
      .subscribe({
        next: (response) => {
          console.log(response);
          this.authService.logout();
          window.location.reload();
        },
        error: (error) => {
          console.error(error);
        },
        complete: () => {
        }
      });
    
  }
}

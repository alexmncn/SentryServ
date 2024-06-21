import { Component, HostListener } from '@angular/core';
import { MatDivider } from '@angular/material/divider';

@Component({
  selector: 'app-about',
  standalone: true,
  imports: [MatDivider],
  templateUrl: './about.component.html',
  styleUrl: './about.component.css'
})
export class AboutComponent {
  headerShrunk = false;

  @HostListener('window:scroll', [])
  onWindowScroll() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
    this.headerShrunk = scrollTop > 50;
  }
}

import { Component, ElementRef, Renderer2, HostListener } from '@angular/core';
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
  headerMarginPos = 1;

  sections!: HTMLElement[];

  constructor(private el: ElementRef, private renderer: Renderer2) {}

  ngAfterViewInit(): void {
    this.sections = Array.from(this.el.nativeElement.querySelectorAll('section'));
  }

  @HostListener('window:scroll', [])
  checkScroll() {
    const windowHeight = window.innerHeight;
    // Fix header
    const scrollTop = window.scrollY || document.documentElement.scrollTop || document.body.scrollTop || 0;
    this.headerShrunk = scrollTop > 50;

    const documentHeight = document.documentElement.scrollHeight;
    const windowCenter = window.scrollY + (windowHeight / 2);

    let closestSection: HTMLElement | null = null;
    let minDistance = Number.MAX_VALUE;

    // Check if the scroll is at the top or bottom of the page
    const atTop = scrollTop === 0;
    const atBottom = (windowHeight + scrollTop) >= documentHeight;

    if (atTop) {
      closestSection = this.sections[0];
    } else if (atBottom) {
      closestSection = this.sections[this.sections.length - 1];
    } else {
      // Find the closest section to the window center
      this.sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        const sectionCenter = sectionTop + (sectionHeight / 2);
        
        const distance = Math.abs(windowCenter - sectionCenter);
        if (distance < minDistance) {
          minDistance = distance;
          closestSection = section;
        }
      });
    }

    // Apply the class to the closest section and remove it from others
    this.sections.forEach(section => {
      if (section === closestSection) {
        // section
        this.renderer.addClass(section, 'section-focus');
        // link
        document.getElementById(section.id+'_link')?.classList.add('selected');
        //this.renderer.addClass(section+'_link', 'selected');
      } else {
        this.renderer.removeClass(section, 'section-focus');
        // link
        document.getElementById(section.id+'_link')?.classList.remove('selected');
        //this.renderer.removeClass(section+'_link', 'selected');
      }
    });
  }

  scrollToSection(id: string): void {
    const element = document.getElementById(id);
    if (element) {
      const headerOffset = this.headerMarginPos; // Ajuste por el margen del encabezado si es necesario
      const elementPosition = element.getBoundingClientRect().top + window.scrollY;
      const offsetPosition = elementPosition - (window.innerHeight / 2) + (element.clientHeight / 2) - headerOffset;
    
      window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
    }
  }


}

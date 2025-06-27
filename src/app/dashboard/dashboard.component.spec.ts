import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardComponent } from './dashboard.component';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have 4 users', () => {
    expect(component.users.length).toBe(4);
  });

  it('should render user names in the table', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Aliceeee');
    expect(compiled.textContent).toContain('Bob');
    expect(compiled.textContent).toContain('Charlie');
    expect(compiled.textContent).toContain('Diana');
  });

  it('should display correct status for each user', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('Active');
    expect(compiled.textContent).toContain('Inactive');
    expect(compiled.textContent).toContain('Pending');
  });
});

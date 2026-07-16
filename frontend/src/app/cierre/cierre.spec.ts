import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Cierre } from './cierre';

describe('Cierre', () => {
  let component: Cierre;
  let fixture: ComponentFixture<Cierre>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Cierre],
    }).compileComponents();

    fixture = TestBed.createComponent(Cierre);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

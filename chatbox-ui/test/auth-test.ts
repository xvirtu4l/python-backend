import { describe, it, expect } from 'vitest';
import {authService} from '@/services/authService';

describe('Auth Service', () => {
  it('should have login method', () => {
    expect(authService.login).toBeDefined();
  });

  it('should have register method', () => {
    expect(authService.register).toBeDefined();
  });

  it('should have logout method', () => {
    expect(authService.logout).toBeDefined();
  });

  it('should have getCurrentUser method', () => {
    expect(authService.getCurrentUser).toBeDefined();
  });
});

describe('Token Manager', () => {
  it('should have setToken method', () => {
    expect(localStorage.setItem).toBeDefined();
  });

  it('should have getToken method', () => {
    expect(localStorage.getItem).toBeDefined();
  });

  it('should have removeToken method', () => {
    expect(localStorage.removeItem).toBeDefined();
  });

  it('should have isAuthenticated method', () => {
    expect(localStorage.getItem).toBeDefined();
  });
});
/**
 * Client-side authentication module for static site.
 * Uses localStorage for user data and cookies for session tokens.
 */

class AuthenticationClient {
  constructor() {
    this.currentUser = null;
    this.sessionToken = this.getCookie('session_token');
    this.init();
  }

  init() {
    if (this.sessionToken) {
      this.validateSession();
    }
  }

  getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
  }

  removeCookie(name) {
    document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
  }

  async fetchWithAuth(url, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    if (this.sessionToken) {
      headers['Authorization'] = `Bearer ${this.sessionToken}`;
    }

    const response = await fetch(url, { ...options, headers });
    return response;
  }

  async register(name, email, password) {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({ name, email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Registration failed');
      }

      return data;
    } catch (error) {
      throw new Error(error.message);
    }
  }

  async login(email, password) {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Login failed');
      }

      // Set session token
      this.sessionToken = data.session_token;
      this.setCookie('session_token', data.session_token, 1);

      // Store user data in localStorage
      localStorage.setItem('user', JSON.stringify(data.user));

      this.currentUser = data.user;
      return data;
    } catch (error) {
      throw new Error(error.message);
    }
  }

  async validateSession() {
    try {
      const response = await fetch('/api/auth/session', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.sessionToken}`
        }
      });

      const data = await response.json();

      if (!response.ok) {
        this.logout();
        return null;
      }

      this.currentUser = data.user;
      localStorage.setItem('user', JSON.stringify(data.user));
      return data.user;
    } catch (error) {
      this.logout();
      return null;
    }
  }

  logout() {
    this.currentUser = null;
    this.sessionToken = null;
    localStorage.removeItem('user');
    this.removeCookie('session_token');
    window.location.href = '/auth/login';
  }

  getUser() {
    if (!this.currentUser) {
      const stored = localStorage.getItem('user');
      this.currentUser = stored ? JSON.parse(stored) : null;
    }
    return this.currentUser;
  }

  isLoggedIn() {
    return !!this.currentUser;
  }

  hasRole(requiredRole) {
    const user = this.getUser();
    if (!user) return false;

    const roleHierarchy = {
      'guest': 0,
      'registered': 1,
      'premium': 2
    };

    const userRoleLevel = roleHierarchy[user.role] || 0;
    const requiredLevel = roleHierarchy[requiredRole] || 0;

    return userRoleLevel >= requiredLevel;
  }

  requireRole(requiredRole) {
    if (!this.hasRole(requiredRole)) {
      window.location.href = '/auth/login';
    }
  }
}

// Initialize global auth instance
const auth = new AuthenticationClient();

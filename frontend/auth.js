// frontend/auth.js
const API_BASE_URL = "https://pi-forge-quantum-genesis-production.up.railway.app";

class AuthService {
    constructor() {
        this.token = localStorage.getItem('authToken');
        this.user = JSON.parse(localStorage.getItem('userData') || 'null');
    }

    // Store token and user data
    setAuth(token, userData) {
        this.token = token;
        this.user = userData;
        localStorage.setItem('authToken', token);
        localStorage.setItem('userData', JSON.stringify(userData));
    }

    // Remove auth data (logout)
    clearAuth() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
    }

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.token;
    }

    // Get auth headers for API calls
    getAuthHeaders() {
        return {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
        };
    }

    // Make authenticated API request
    async authenticatedFetch(endpoint, options = {}) {
        if (!this.isAuthenticated()) {
            throw new Error('Not authenticated');
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                ...options.headers,
                ...this.getAuthHeaders()
            }
        });

        if (response.status === 401) {
            this.clearAuth();
            window.location.href = '/login.html';
            return;
        }

        return response;
    }

    // Login method
    async login(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.setAuth(data.token, data.user);
                return { success: true, user: data.user };
            } else {
                return { success: false, error: data.error };
            }
        } catch (error) {
            return { success: false, error: 'Network error' };
        }
    }
}

// Create global auth instance
const authService = new AuthService();

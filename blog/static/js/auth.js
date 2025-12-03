// JWT Token Management Utilities

const TokenManager = {
    // Token storage keys
    ACCESS_TOKEN_KEY: 'access_token',
    REFRESH_TOKEN_KEY: 'refresh_token',
    USERNAME_KEY: 'username',
    USER_ID_KEY: 'user_id',

    // Store tokens in localStorage
    setTokens(accessToken, refreshToken, username, userId) {
        localStorage.setItem(this.ACCESS_TOKEN_KEY, accessToken);
        localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken);
        localStorage.setItem(this.USERNAME_KEY, username);
        localStorage.setItem(this.USER_ID_KEY, userId);
    },

    // Get access token
    getAccessToken() {
        return localStorage.getItem(this.ACCESS_TOKEN_KEY);
    },

    // Get refresh token
    getRefreshToken() {
        return localStorage.getItem(this.REFRESH_TOKEN_KEY);
    },

    // Get username
    getUsername() {
        return localStorage.getItem(this.USERNAME_KEY);
    },

    // Get user ID
    getUserId() {
        return localStorage.getItem(this.USER_ID_KEY);
    },

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.getAccessToken();
    },

    // Clear all tokens (logout)
    clearTokens() {
        localStorage.removeItem(this.ACCESS_TOKEN_KEY);
        localStorage.removeItem(this.REFRESH_TOKEN_KEY);
        localStorage.removeItem(this.USERNAME_KEY);
        localStorage.removeItem(this.USER_ID_KEY);
    },

    // Refresh access token
    async refreshAccessToken() {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) {
            return false;
        }

        try {
            const response = await fetch('/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem(this.ACCESS_TOKEN_KEY, data.access);
                return true;
            } else {
                // Refresh token is invalid, clear all tokens
                this.clearTokens();
                return false;
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            return false;
        }
    },

    // Make authenticated fetch request
    async authenticatedFetch(url, options = {}) {
        const accessToken = this.getAccessToken();

        if (!accessToken) {
            throw new Error('No access token available');
        }

        // Add Authorization header
        const headers = {
            ...options.headers,
            'Authorization': `Bearer ${accessToken}`
        };

        const response = await fetch(url, {
            ...options,
            headers
        });

        // If unauthorized, try to refresh token and retry
        if (response.status === 401) {
            const refreshed = await this.refreshAccessToken();
            if (refreshed) {
                // Retry with new token
                const newAccessToken = this.getAccessToken();
                headers['Authorization'] = `Bearer ${newAccessToken}`;
                return fetch(url, {
                    ...options,
                    headers
                });
            } else {
                // Redirect to login
                window.location.href = '/accounts/login/';
                throw new Error('Authentication failed');
            }
        }

        return response;
    }
};

// Export for use in other scripts
window.TokenManager = TokenManager;

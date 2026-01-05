/**
 * Authentication Logic
 */

class AuthService {
    constructor() {
        this.loginForm = document.getElementById('loginForm');
        this.loginBtn = document.getElementById('loginBtn');
        this.emailInput = document.getElementById('email');
        this.passwordInput = document.getElementById('password');
        this.card = document.getElementById('loginCard');

        if (this.loginForm) {
            this.initLogin();
        }

        // Global Logout Handler
        this.initLogout();
    }

    initLogin() {
        this.loginForm.addEventListener('submit', (e) => this.handleLogin(e));

        // Input focus effects
        [this.emailInput, this.passwordInput].forEach(input => {
            input.addEventListener('focus', () => {
                input.parentElement.classList.add('glow');
            });
            input.addEventListener('blur', () => {
                input.parentElement.classList.remove('glow');
            });
        });
    }

    initLogout() {
        // Listen for logout button clicks anywhere in the app
        document.addEventListener('click', (e) => {
            const logoutBtn = e.target.closest('#logoutBtn');
            if (logoutBtn) {
                this.handleLogout();
            }
        });
    }

    handleLogout() {
        if (confirm("Are you sure you want to sign out?")) {
            // Clear session/tokens if applicable
            localStorage.removeItem('user_session');
            // Redirect to login
            window.location.href = '/pages/login.html';
        }
    }

    async handleLogin(e) {
        e.preventDefault();

        const email = this.emailInput.value;
        const password = this.passwordInput.value;

        // Set Loading State
        this.setLoading(true);

        try {
            // Simulate API Call (Replace with real backend later)
            await new Promise(resolve => setTimeout(resolve, 1500));

            // Mock Validation
            if (email && password.length >= 6) {
                // Success
                this.showSuccess();
                setTimeout(() => {
                    // FIX: Updated path to use mounted /pages/
                    window.location.href = '/pages/dashboard.html';
                }, 1000);
            } else {
                throw new Error("Invalid credentials");
            }

        } catch (error) {
            // Error Handling
            this.triggerShake();
            this.showError(error.message);
            this.setLoading(false);
        }
    }

    setLoading(isLoading) {
        if (isLoading) {
            this.loginBtn.disabled = true;
            this.loginBtn.innerHTML = '<div class="spinner"></div> Processing...';
        } else {
            this.loginBtn.disabled = false;
            this.loginBtn.innerHTML = '<span>LOGIN</span> <i class="fas fa-arrow-right"></i>';
        }
    }

    triggerShake() {
        this.card.classList.remove('animate-shake');
        void this.card.offsetWidth; // Trigger reflow
        this.card.classList.add('animate-shake');
    }

    showSuccess() {
        this.loginBtn.innerHTML = '<i class="fas fa-check"></i> Success!';
        this.loginBtn.style.background = 'var(--status-success)';
    }

    showError(msg) {
        // Simple toast or alert can be added here
        console.error(msg);
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    new AuthService();
});

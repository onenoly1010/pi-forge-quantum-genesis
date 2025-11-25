// Quantum Forge Shield - Viral Widget for Pi SDK Payment Protection
// Intercepts Pi SDK createPayment calls, displays protection badge, and performs security analysis

const QuantumForgeShield = {
    // Configuration
    config: {
        apiEndpoint: '/api/analyze',
        badgeId: 'quantum-forge-shield-badge',
        badgeTimeout: 5000, // Auto-hide badge after 5 seconds on success
        enabled: true
    },

    // Original Pi.createPayment reference
    originalCreatePayment: null,

    // Initialize the shield
    init() {
        if (!this.config.enabled) {
            console.log('[QuantumForgeShield] Shield is disabled');
            return;
        }

        // Wait for Pi SDK to be available
        if (typeof window.Pi !== 'undefined' && window.Pi.createPayment) {
            this.interceptPiSDK();
            this.injectStyles();
            console.log('[QuantumForgeShield] Shield initialized successfully');
        } else {
            // Retry after Pi SDK loads
            const checkInterval = setInterval(() => {
                if (typeof window.Pi !== 'undefined' && window.Pi.createPayment) {
                    clearInterval(checkInterval);
                    this.interceptPiSDK();
                    this.injectStyles();
                    console.log('[QuantumForgeShield] Shield initialized (delayed)');
                }
            }, 100);

            // Stop checking after 10 seconds
            setTimeout(() => clearInterval(checkInterval), 10000);
        }
    },

    // Intercept Pi SDK createPayment method
    interceptPiSDK() {
        this.originalCreatePayment = window.Pi.createPayment.bind(window.Pi);
        
        window.Pi.createPayment = async (paymentData, callbacks) => {
            console.log('[QuantumForgeShield] Intercepted createPayment call');
            
            // Show analyzing badge
            this.showBadge('analyzing');

            try {
                // Perform security analysis
                const analysisResult = await this.analyzeTransaction(paymentData);

                if (analysisResult.blocked) {
                    // Transaction blocked - show blocked badge
                    this.showBadge('blocked', analysisResult.reason);
                    console.warn('[QuantumForgeShield] Transaction blocked:', analysisResult.reason);
                    
                    // Call error callback if provided
                    if (callbacks && callbacks.onPaymentError) {
                        callbacks.onPaymentError({
                            type: 'QUANTUM_FORGE_BLOCKED',
                            message: analysisResult.reason || 'Transaction blocked by security analysis'
                        });
                    }
                    
                    return null;
                }

                // Transaction approved - show protected badge
                this.showBadge('protected', analysisResult.message);

                // Wrap callbacks with shield monitoring
                const wrappedCallbacks = this.wrapCallbacks(callbacks);

                // Call original createPayment
                return await this.originalCreatePayment(paymentData, wrappedCallbacks);

            } catch (error) {
                console.error('[QuantumForgeShield] Analysis error:', error);
                
                // On analysis error, show warning but allow transaction to proceed
                this.showBadge('warning', 'Analysis unavailable - proceeding with caution');
                
                // Call original createPayment
                return await this.originalCreatePayment(paymentData, callbacks);
            }
        };
    },

    // Analyze transaction through backend API
    async analyzeTransaction(paymentData) {
        const headers = {
            'Content-Type': 'application/json'
        };

        // Add authorization token if available
        const authToken = this.getAuthToken();
        if (authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
        }

        // Add CSRF token if available
        const csrfToken = this.getCsrfToken();
        if (csrfToken) {
            headers['X-CSRF-Token'] = csrfToken;
        }

        const response = await fetch(this.config.apiEndpoint, {
            method: 'POST',
            headers: headers,
            credentials: 'same-origin',
            body: JSON.stringify({
                amount: paymentData.amount,
                memo: paymentData.memo,
                metadata: paymentData.metadata,
                timestamp: Date.now()
            })
        });

        if (!response.ok) {
            throw new Error(`Analysis API returned ${response.status}`);
        }

        return await response.json();
    },

    // Get authentication token from storage or global context
    getAuthToken() {
        // Check localStorage first
        const storedToken = localStorage.getItem('access_token') || localStorage.getItem('jwt_token');
        if (storedToken) {
            return storedToken;
        }
        // Check global window context
        if (window.authToken) {
            return window.authToken;
        }
        return null;
    },

    // Get CSRF token from meta tag or cookie
    getCsrfToken() {
        // Check meta tag
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) {
            return metaTag.getAttribute('content');
        }
        // Check cookie
        const match = document.cookie.match(/csrf[_-]?token=([^;]+)/i);
        if (match) {
            return match[1];
        }
        return null;
    },

    // Wrap payment callbacks with additional monitoring
    wrapCallbacks(callbacks) {
        if (!callbacks) {
            return callbacks;
        }

        return {
            onReadyForServerApproval: (paymentId) => {
                console.log('[QuantumForgeShield] Payment ready for approval:', paymentId);
                if (callbacks.onReadyForServerApproval) {
                    callbacks.onReadyForServerApproval(paymentId);
                }
            },
            onPaymentSuccess: (payment) => {
                console.log('[QuantumForgeShield] Payment successful');
                this.showBadge('success', 'Transaction completed securely');
                if (callbacks.onPaymentSuccess) {
                    callbacks.onPaymentSuccess(payment);
                }
            },
            onPaymentError: (error) => {
                console.error('[QuantumForgeShield] Payment error:', error);
                this.showBadge('error', 'Transaction failed');
                if (callbacks.onPaymentError) {
                    callbacks.onPaymentError(error);
                }
            },
            onIncompletePaymentFound: (payment) => {
                console.log('[QuantumForgeShield] Incomplete payment found');
                if (callbacks.onIncompletePaymentFound) {
                    callbacks.onIncompletePaymentFound(payment);
                }
            }
        };
    },

    // Show/update the protection badge
    showBadge(status, message) {
        let badge = document.getElementById(this.config.badgeId);

        if (!badge) {
            badge = document.createElement('div');
            badge.id = this.config.badgeId;
            document.body.appendChild(badge);
        }

        // Clear existing classes
        badge.className = 'quantum-forge-shield-badge';
        
        // Set status-specific styles and content
        const statusConfig = {
            analyzing: {
                class: 'analyzing',
                icon: '🔍',
                text: message || 'Analyzing transaction...'
            },
            protected: {
                class: 'protected',
                icon: '🛡️',
                text: message || 'Protected by Quantum Forge'
            },
            blocked: {
                class: 'blocked',
                icon: '🚫',
                text: message || 'Transaction blocked'
            },
            warning: {
                class: 'warning',
                icon: '⚠️',
                text: message || 'Caution advised'
            },
            success: {
                class: 'success',
                icon: '✅',
                text: message || 'Transaction secure'
            },
            error: {
                class: 'error',
                icon: '❌',
                text: message || 'Transaction error'
            }
        };

        const config = statusConfig[status] || statusConfig.protected;
        badge.classList.add(config.class);
        badge.innerHTML = `
            <span class="shield-icon">${config.icon}</span>
            <span class="shield-text">${config.text}</span>
        `;
        
        badge.style.display = 'flex';

        // Auto-hide badge after timeout for success states
        if (status === 'protected' || status === 'success') {
            const badgeId = this.config.badgeId;
            setTimeout(() => {
                const currentBadge = document.getElementById(badgeId);
                if (currentBadge) {
                    currentBadge.style.display = 'none';
                }
            }, this.config.badgeTimeout);
        }
    },

    // Hide the badge
    hideBadge() {
        const badge = document.getElementById(this.config.badgeId);
        if (badge) {
            badge.style.display = 'none';
        }
    },

    // Inject CSS styles for the badge
    injectStyles() {
        if (document.getElementById('quantum-forge-shield-styles')) {
            return; // Styles already injected
        }

        const style = document.createElement('style');
        style.id = 'quantum-forge-shield-styles';
        style.textContent = `
            .quantum-forge-shield-badge {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                font-weight: 500;
                z-index: 10000;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                transition: all 0.3s ease;
                animation: slideIn 0.3s ease;
            }

            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            .quantum-forge-shield-badge .shield-icon {
                font-size: 18px;
            }

            .quantum-forge-shield-badge .shield-text {
                white-space: nowrap;
            }

            .quantum-forge-shield-badge.analyzing {
                background: linear-gradient(135deg, #3498db, #2980b9);
                color: white;
            }

            .quantum-forge-shield-badge.protected {
                background: linear-gradient(135deg, #2ecc71, #27ae60);
                color: white;
            }

            .quantum-forge-shield-badge.blocked {
                background: linear-gradient(135deg, #e74c3c, #c0392b);
                color: white;
            }

            .quantum-forge-shield-badge.warning {
                background: linear-gradient(135deg, #f39c12, #e67e22);
                color: white;
            }

            .quantum-forge-shield-badge.success {
                background: linear-gradient(135deg, #9b59b6, #8e44ad);
                color: white;
            }

            .quantum-forge-shield-badge.error {
                background: linear-gradient(135deg, #e74c3c, #c0392b);
                color: white;
            }

            /* Pulse animation for analyzing state */
            .quantum-forge-shield-badge.analyzing::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                border-radius: 8px;
                animation: pulse 1.5s infinite;
                pointer-events: none;
            }

            @keyframes pulse {
                0% {
                    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.4);
                }
                70% {
                    box-shadow: 0 0 0 10px rgba(52, 152, 219, 0);
                }
                100% {
                    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0);
                }
            }
        `;

        document.head.appendChild(style);
    },

    // Disable the shield
    disable() {
        this.config.enabled = false;
        if (this.originalCreatePayment && window.Pi) {
            window.Pi.createPayment = this.originalCreatePayment;
        }
        this.hideBadge();
        console.log('[QuantumForgeShield] Shield disabled');
    },

    // Enable the shield
    enable() {
        this.config.enabled = true;
        this.init();
        console.log('[QuantumForgeShield] Shield enabled');
    }
};

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => QuantumForgeShield.init());
} else {
    QuantumForgeShield.init();
}

// Export for global use
window.QuantumForgeShield = QuantumForgeShield;

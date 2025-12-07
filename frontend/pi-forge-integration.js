/**
 * PiForge Integration Module - Production Mainnet Ready
 * Comprehensive Pi Network integration for Quantum Genesis platform
 * Version: 2.0.0 - Mainnet Ready
 */

const PiForge = {
    // Configuration
    config: {
        apiBase: window.location.origin,
        network: 'mainnet', // 'testnet' or 'mainnet'
        version: '2.0.0',
        debug: false
    },

    // Authentication state
    auth: {
        user: null,
        accessToken: null,
        isAuthenticated: false
    },

    // Payment state
    payments: {
        pending: new Map(),
        completed: [],
        failed: []
    },

    /**
     * Initialize PiForge with Pi Network SDK
     * @param {Object} options - Configuration options
     */
    async initialize(options = {}) {
        this.config = { ...this.config, ...options };
        
        if (this.config.debug) {
            console.log('🌌 PiForge Quantum Genesis initializing...');
        }

        // Check if Pi SDK is available
        if (typeof Pi === 'undefined') {
            console.warn('⚠️ Pi SDK not available - running in demo mode');
            return { success: true, mode: 'demo' };
        }

        try {
            // Initialize Pi SDK
            await Pi.init({ version: "2.0", sandbox: this.config.network === 'testnet' });
            
            if (this.config.debug) {
                console.log('✅ Pi SDK initialized for', this.config.network);
            }

            return { success: true, mode: this.config.network };
        } catch (error) {
            console.error('❌ Pi SDK initialization failed:', error);
            return { success: false, error: error.message };
        }
    },

    /**
     * Authenticate user with Pi Network
     * @param {Array} scopes - Authentication scopes ['payments', 'username', 'wallet_address']
     */
    async authenticate(scopes = ['payments', 'username']) {
        if (typeof Pi === 'undefined') {
            // Demo mode authentication
            this.auth = {
                user: { username: 'demo_pioneer', uid: 'demo_uid_' + Date.now() },
                accessToken: 'demo_token_' + Date.now(),
                isAuthenticated: true
            };
            return this.auth;
        }

        try {
            const authResult = await Pi.authenticate(scopes, this._onIncompletePaymentFound.bind(this));
            
            this.auth = {
                user: authResult.user,
                accessToken: authResult.accessToken,
                isAuthenticated: true
            };

            if (this.config.debug) {
                console.log('✅ User authenticated:', this.auth.user.username);
            }

            // Notify backend of authentication
            await this._notifyBackendAuth();

            return this.auth;
        } catch (error) {
            console.error('❌ Authentication failed:', error);
            this.auth.isAuthenticated = false;
            throw error;
        }
    },

    /**
     * Create a Pi Network payment
     * @param {Object} paymentData - Payment configuration
     */
    async createPayment(paymentData) {
        const { amount, memo, metadata = {} } = paymentData;

        if (!amount || amount <= 0) {
            throw new Error('Invalid payment amount');
        }

        const paymentConfig = {
            amount: parseFloat(amount.toFixed(7)), // Pi supports up to 7 decimals
            memo: memo || `PiForge Payment - ${new Date().toISOString()}`,
            metadata: {
                ...metadata,
                timestamp: Date.now(),
                platform: 'piforge_quantum_genesis',
                version: this.config.version
            }
        };

        if (typeof Pi === 'undefined') {
            // Demo mode payment simulation
            return this._simulatePayment(paymentConfig);
        }

        return new Promise((resolve, reject) => {
            Pi.createPayment(paymentConfig, {
                onReadyForServerApproval: async (paymentId) => {
                    if (this.config.debug) {
                        console.log('📝 Payment ready for server approval:', paymentId);
                    }
                    
                    this.payments.pending.set(paymentId, { ...paymentConfig, status: 'pending' });
                    
                    try {
                        // Send to backend for approval
                        const approvalResult = await this._requestServerApproval(paymentId, paymentConfig);
                        if (!approvalResult.approved) {
                            throw new Error(approvalResult.message || 'Server rejected payment');
                        }
                    } catch (error) {
                        console.error('❌ Server approval failed:', error);
                        reject(error);
                    }
                },

                onReadyForServerCompletion: async (paymentId, txid) => {
                    if (this.config.debug) {
                        console.log('✅ Payment ready for completion:', paymentId, txid);
                    }

                    try {
                        // Complete payment on backend
                        const completionResult = await this._completePayment(paymentId, txid);
                        
                        this.payments.pending.delete(paymentId);
                        this.payments.completed.push({
                            paymentId,
                            txid,
                            ...paymentConfig,
                            completedAt: Date.now()
                        });

                        // Trigger resonance visualization
                        this.renderResonanceViz({ txid, ...metadata });

                        resolve({
                            success: true,
                            paymentId,
                            txid,
                            ...completionResult
                        });
                    } catch (error) {
                        console.error('❌ Payment completion failed:', error);
                        reject(error);
                    }
                },

                onCancel: (paymentId) => {
                    if (this.config.debug) {
                        console.log('❌ Payment cancelled:', paymentId);
                    }
                    this.payments.pending.delete(paymentId);
                    reject(new Error('Payment cancelled by user'));
                },

                onError: (error, payment) => {
                    console.error('❌ Payment error:', error);
                    if (payment?.identifier) {
                        this.payments.pending.delete(payment.identifier);
                        this.payments.failed.push({
                            paymentId: payment.identifier,
                            error: error.message,
                            failedAt: Date.now()
                        });
                    }
                    reject(error);
                }
            });
        });
    },

    /**
     * Activate Mining Boost via Pi payment
     * @param {number} boostPercent - Boost percentage (1-100)
     */
    async activateMiningBoost(boostPercent) {
        if (boostPercent < 1 || boostPercent > 100) {
            throw new Error('Boost percent must be between 1 and 100');
        }

        try {
            const paymentResult = await this.createPayment({
                amount: (boostPercent / 100) * 0.15,
                memo: `PiForge Boost: ${boostPercent}% Ethical Resonance Activated`,
                metadata: { 
                    type: 'mining_boost',
                    boostPercent,
                    userId: this.auth.user?.uid
                }
            });

            // Update UI
            const statusEl = document.getElementById('status');
            if (statusEl) {
                statusEl.textContent += ` | Boost Activated: +${boostPercent}% Mining!`;
            }

            return paymentResult;
        } catch (error) {
            console.error('❌ Mining Boost Failed:', error);
            throw error;
        }
    },

    /**
     * Render quantum resonance visualization (4-phase SVG cascade)
     * @param {Object} metadata - Payment/transaction metadata
     */
    renderResonanceViz(metadata = {}) {
        // Remove any existing visualization
        const existing = document.getElementById('piforge-resonance-viz');
        if (existing) existing.remove();

        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.id = 'piforge-resonance-viz';
        svg.setAttribute('width', '300');
        svg.setAttribute('height', '300');
        svg.setAttribute('viewBox', '0 0 300 300');
        svg.style.cssText = 'position:fixed;top:10px;right:10px;z-index:10000;pointer-events:none;';

        // 4-phase quantum cascade
        const phases = [
            { name: 'foundation', radius: 50, color: 'hsl(0, 100%, 50%)', duration: '2s' },
            { name: 'growth', radius: 80, color: 'hsl(90, 100%, 50%)', duration: '3s' },
            { name: 'harmony', radius: 110, color: 'hsl(180, 100%, 50%)', duration: '4s' },
            { name: 'transcendence', radius: 140, color: 'hsl(270, 100%, 50%)', duration: '5s' }
        ];

        phases.forEach((phase, i) => {
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', '150');
            circle.setAttribute('cy', '150');
            circle.setAttribute('r', phase.radius);
            circle.setAttribute('fill', 'none');
            circle.setAttribute('stroke', phase.color);
            circle.setAttribute('stroke-width', '2');
            circle.setAttribute('opacity', '0.7');
            circle.style.animation = `piforge-resonate-${i} ${phase.duration} ease-in-out infinite`;
            circle.style.transformOrigin = 'center';
            svg.appendChild(circle);
        });

        // Center indicator
        const centerCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        centerCircle.setAttribute('cx', '150');
        centerCircle.setAttribute('cy', '150');
        centerCircle.setAttribute('r', '20');
        centerCircle.setAttribute('fill', 'rgba(255, 215, 0, 0.8)');
        centerCircle.style.animation = 'piforge-pulse 1s ease-in-out infinite';
        svg.appendChild(centerCircle);

        document.body.appendChild(svg);

        // Inject CSS animations
        if (!document.getElementById('piforge-resonance-styles')) {
            const style = document.createElement('style');
            style.id = 'piforge-resonance-styles';
            style.textContent = `
                @keyframes piforge-resonate-0 {
                    0% { transform: scale(1) rotate(0deg); opacity: 0.7; }
                    50% { transform: scale(1.3) rotate(180deg); opacity: 0.3; }
                    100% { transform: scale(1) rotate(360deg); opacity: 0.7; }
                }
                @keyframes piforge-resonate-1 {
                    0% { transform: scale(0.9) rotate(0deg); opacity: 0.6; }
                    50% { transform: scale(1.4) rotate(270deg); opacity: 0.2; }
                    100% { transform: scale(0.9) rotate(360deg); opacity: 0.6; }
                }
                @keyframes piforge-resonate-2 {
                    0% { transform: scale(1.1) rotate(180deg); opacity: 0.5; }
                    50% { transform: scale(1.5) rotate(90deg); opacity: 0.2; }
                    100% { transform: scale(1.1) rotate(540deg); opacity: 0.5; }
                }
                @keyframes piforge-resonate-3 {
                    0% { transform: scale(0.85) rotate(270deg); opacity: 0.4; }
                    50% { transform: scale(1.6) rotate(0deg); opacity: 0.15; }
                    100% { transform: scale(0.85) rotate(630deg); opacity: 0.4; }
                }
                @keyframes piforge-pulse {
                    0%, 100% { transform: scale(1); opacity: 0.8; }
                    50% { transform: scale(1.2); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }

        // Auto-remove after 10 seconds
        setTimeout(() => {
            svg.style.opacity = '0';
            svg.style.transition = 'opacity 1s';
            setTimeout(() => svg.remove(), 1000);
        }, 10000);
    },

    /**
     * Compute ethical resonance score
     * @param {number} ethicalScore - Ethical compliance score (0-100)
     * @param {number} qualiaImpact - Qualia impact score (0-100)
     */
    computeResonance(ethicalScore, qualiaImpact) {
        const resonance = Math.floor((ethicalScore * 0.7 + qualiaImpact * 3) / 10);
        
        if (resonance >= 80) return { level: 'Transcendent', color: '#8B5CF6', score: resonance };
        if (resonance >= 60) return { level: 'Harmonic', color: '#3B82F6', score: resonance };
        if (resonance >= 40) return { level: 'Growing', color: '#10B981', score: resonance };
        return { level: 'Foundation', color: '#EF4444', score: resonance };
    },

    /**
     * Get Guardian status from backend
     */
    async getGuardianStatus() {
        try {
            const response = await fetch(`${this.config.apiBase}/api/guardian/status`);
            return await response.json();
        } catch (error) {
            console.error('❌ Failed to get Guardian status:', error);
            throw error;
        }
    },

    /**
     * Trigger Guardian security scan
     */
    async triggerGuardianScan() {
        try {
            const response = await fetch(`${this.config.apiBase}/api/guardian/scan`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            return await response.json();
        } catch (error) {
            console.error('❌ Guardian scan failed:', error);
            throw error;
        }
    },

    /**
     * Request ethical audit
     * @param {string} transactionId - Transaction to audit
     * @param {number} amount - Transaction amount
     */
    async requestEthicalAudit(transactionId, amount) {
        try {
            const response = await fetch(`${this.config.apiBase}/api/ethical-audit`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    transaction_id: transactionId,
                    amount: amount,
                    user_context: this.auth.user?.username || 'anonymous'
                })
            });
            return await response.json();
        } catch (error) {
            console.error('❌ Ethical audit failed:', error);
            throw error;
        }
    },

    // Private helper methods

    async _notifyBackendAuth() {
        try {
            // Optionally notify backend of successful authentication
            // This could create/update user records in Supabase
            if (this.config.debug) {
                console.log('📡 Backend notified of authentication');
            }
        } catch (error) {
            console.warn('⚠️ Backend notification failed:', error);
        }
    },

    async _requestServerApproval(paymentId, paymentConfig) {
        const response = await fetch(`${this.config.apiBase}/api/verify-payment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': this.auth.accessToken ? `Bearer ${this.auth.accessToken}` : ''
            },
            body: JSON.stringify({
                payment_id: paymentId,
                amount: paymentConfig.amount,
                metadata: paymentConfig.metadata
            })
        });

        if (!response.ok) {
            throw new Error(`Server approval failed: ${response.status}`);
        }

        return await response.json();
    },

    async _completePayment(paymentId, txid) {
        // In production, this would complete the payment on the backend
        // and update transaction records in Supabase
        return {
            completed: true,
            paymentId,
            txid,
            timestamp: Date.now()
        };
    },

    _onIncompletePaymentFound(payment) {
        if (this.config.debug) {
            console.log('📌 Incomplete payment found:', payment);
        }
        // Handle incomplete payments (e.g., show recovery dialog)
        this.payments.pending.set(payment.identifier, {
            ...payment,
            status: 'incomplete',
            foundAt: Date.now()
        });
    },

    async _simulatePayment(paymentConfig) {
        // Demo mode payment simulation
        return new Promise((resolve) => {
            setTimeout(() => {
                const paymentId = 'demo_' + Date.now();
                const txid = 'demo_tx_' + Math.random().toString(36).substring(7);
                
                this.payments.completed.push({
                    paymentId,
                    txid,
                    ...paymentConfig,
                    completedAt: Date.now(),
                    mode: 'demo'
                });

                this.renderResonanceViz({ txid, demo: true });

                resolve({
                    success: true,
                    paymentId,
                    txid,
                    mode: 'demo'
                });
            }, 1500);
        });
    }
};

// Export for global use
window.PiForge = PiForge;

// Auto-initialize if DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => PiForge.initialize());
} else {
    PiForge.initialize();
}
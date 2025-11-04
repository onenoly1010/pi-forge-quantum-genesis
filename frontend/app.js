// Pi Forge Quantum Genesis - Frontend
// By Kris Olofson (onenoly11)

class PiForgeApp {
    constructor() {
        this.backendUrl = process?.env?.BACKEND_URL || ''; // Force mock mode for now
        this.socket = null;
        this.mockMode = true; // Enable mock mode by default
        this.init();
    }

    init() {
        console.log('🚀 Initializing Pi Forge Quantum Genesis...');
        this.updateStatus('backend-status', 'disconnected', 'Backend: Mock Mode (Development)');
        this.setupWebSocket();
        this.loadLeaderboard();
        
        // Auto-refresh leaderboard every 30 seconds
        setInterval(() => this.loadLeaderboard(), 30000);
        
        // Add event listeners for better UX
        this.attachEventListeners();
    }

    async checkBackendStatus() {
        // Skip backend checking for now - use mock mode
        this.updateStatus('backend-status', 'disconnected', 'Backend: Mock Mode');
        console.log('🚨 Running in mock mode - Backend connection disabled');
        return;
    }

    setupWebSocket() {
        // Skip WebSocket for mock mode
        this.updateStatus('websocket-status', 'disconnected', 'WebSocket: Mock Mode');
        console.log('🔌 WebSocket disabled - Running in mock mode');
    }

    updateStatus(elementId, status, text) {
        const element = document.getElementById(elementId);
        if (element) {
            const dot = element.querySelector('.status-dot');
            element.textContent = text;
            if (dot) {
                dot.className = 'status-dot ' + status;
                element.appendChild(dot);
            }
        }
    }

    async startMining() {
        const digitsInput = document.getElementById('digitsInput');
        const resultDiv = document.getElementById('miningResult');
        const button = document.getElementById('mineBtn');
        
        const digits = parseInt(digitsInput.value);
        
        // Enhanced validation
        if (!digits || isNaN(digits) || digits < 1) {
            this.showError(resultDiv, '⚠️ Please enter a valid number (minimum 1 digit)');
            return;
        }
        
        if (digits > 1000000) {
            this.showError(resultDiv, '⚠️ Maximum 1,000,000 digits allowed');
            return;
        }

        button.disabled = true;
        button.textContent = '⛏️ Mining...';
        resultDiv.innerHTML = '<div class="pulse">🚀 Starting quantum computation...</div>';

        try {
            // Mock response only
            const data = {
                digits: digits,
                result: this.calculateMockPi(digits),
                status: "computed",
                developer: "Kris Olofson"
            };

            resultDiv.innerHTML = `
                <div style="color: #00ff88;">
                    <strong>✅ Success!</strong><br>
                    Digits: ${data.digits.toLocaleString()}<br>
                    Result: ${data.result}<br>
                    Status: ${data.status}
                </div>
            `;
            this.addEvent(`⚡ Mined ${digits.toLocaleString()} Pi digits`);
            this.loadLeaderboard(); // Refresh leaderboard

        } catch (error) {
            console.error('Mining error:', error);
            this.showError(resultDiv, `❌ Error: ${error.message}`);
        } finally {
            button.disabled = false;
            button.textContent = '🚀 Start Mining';
        }
    }

    async stakeTokens() {
        const amountInput = document.getElementById('stakeAmount');
        const button = document.getElementById('stakeBtn');
        
        const amount = parseFloat(amountInput.value);
        
        // Enhanced validation
        if (!amount || isNaN(amount) || amount <= 0) {
            alert('⚠️ Please enter a valid stake amount (positive number)');
            return;
        }
        
        if (amount > 1000000) {
            alert('⚠️ Maximum stake amount is 1,000,000 tokens');
            return;
        }

        button.disabled = true;
        button.textContent = '🔒 Staking...';

        try {
            // Mock response only
            const data = {
                status: "staked",
                amount: amount,
                user_id: "quantum_miner",
                message: "Tokens staked successfully"
            };

            alert(`✅ ${data.message}\nAmount: ${data.amount.toLocaleString()} tokens\nAPY: 5.5%`);
            this.addEvent(`💰 Staked ${amount.toLocaleString()} tokens`);
            amountInput.value = ''; // Clear input after successful stake

        } catch (error) {
            console.error('Staking error:', error);
            alert(`❌ Staking failed: ${error.message}`);
        } finally {
            button.disabled = false;
            button.textContent = '🔒 Stake Tokens';
        }
    }

    async loadLeaderboard() {
        const leaderboardDiv = document.getElementById('leaderboard');
        
        try {
            // Mock data only
            const data = {
                leaderboard: [
                    { user_id: 'quantum_miner', digits_mined: 1000000 },
                    { user_id: 'pi_explorer', digits_mined: 850000 },
                    { user_id: 'math_genius', digits_mined: 720000 },
                    { user_id: 'crypto_pioneer', digits_mined: 650000 },
                    { user_id: 'vr_miner', digits_mined: 580000 }
                ]
            };

            if (data.leaderboard && data.leaderboard.length > 0) {
                leaderboardDiv.innerHTML = data.leaderboard.map((user, index) => `
                    <div class="leaderboard-item">
                        <span>${index + 1}. ${user.user_id}</span>
                        <span>${user.digits_mined.toLocaleString()} digits</span>
                    </div>
                `).join('');
            } else {
                leaderboardDiv.innerHTML = '<div style="color: #ffa500;">No mining data yet</div>';
            }
        } catch (error) {
            console.error('Leaderboard load error:', error);
            leaderboardDiv.innerHTML = '<div style="color: #ff6b6b;">Failed to load leaderboard</div>';
        }
    }

    startVRMine() {
        this.addEvent('🕶️ Starting VR mining session...');
        
        // Mock VR mine
        setTimeout(() => {
            this.addEvent('🕶️ VR Mine: quantum_miner mined 1,247 digits');
        }, 1000);
    }

    startVRQuest() {
        this.addEvent('⚔️ Starting VR quest...');
        
        // Mock VR quest
        setTimeout(() => {
            this.addEvent('⚔️ VR Quest: quantum_miner completed quantum_computation');
        }, 1500);
    }

    addEvent(message) {
        const eventsFeed = document.getElementById('eventsFeed');
        if (eventsFeed) {
            const eventItem = document.createElement('div');
            eventItem.className = 'event-item';
            eventItem.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
            
            eventsFeed.prepend(eventItem);
            
            // Keep only last 10 events
            while (eventsFeed.children.length > 10) {
                eventsFeed.removeChild(eventsFeed.lastChild);
            }
        }
    }

    calculateMockPi(digits) {
        if (digits <= 20) {
            const pi = "3.14159265358979323846";
            return pi.substring(0, digits + 2);
        } else {
            return `3.14... [computed ${digits.toLocaleString()} digits in quantum state]`;
        }
    }
    
    showError(element, message) {
        if (element) {
            element.innerHTML = `<span style="color: #ff6b6b;">${message}</span>`;
        }
    }
    
    attachEventListeners() {
        // Allow Enter key to trigger mining
        const digitsInput = document.getElementById('digitsInput');
        if (digitsInput) {
            digitsInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.startMining();
                }
            });
        }
        
        // Allow Enter key to trigger staking
        const stakeInput = document.getElementById('stakeAmount');
        if (stakeInput) {
            stakeInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.stakeTokens();
                }
            });
        }
    }
}

// Global functions for button clicks
function startMining() {
    if (window.app) {
        window.app.startMining();
    }
}

function stakeTokens() {
    if (window.app) {
        window.app.stakeTokens();
    }
}

function startVRMine() {
    if (window.app) {
        window.app.startVRMine();
    }
}

function startVRQuest() {
    if (window.app) {
        window.app.startVRQuest();
    }
}

// Initialize app when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.app = new PiForgeApp();
    console.log('🚀 Pi Forge Quantum Genesis - Mock Mode Active');
});

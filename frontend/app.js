// Pi Forge Quantum Genesis - Frontend
// By Kris Olofson (onenoly11)

class PiForgeApp {
    constructor() {
        this.backendUrl = ''; // Force mock mode for now
        this.socket = null;
        this.init();
    }

    init() {
        this.updateStatus('backend-status', 'disconnected', 'Backend: Mock Mode (Development)');
        this.setupWebSocket();
        this.loadLeaderboard();
        
        // Auto-refresh leaderboard every 30 seconds
        setInterval(() => this.loadLeaderboard(), 30000);
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
        if (!digits || digits < 1) {
            resultDiv.innerHTML = '<span style="color: #ff6b6b;">⚠️ Please enter valid number of digits</span>';
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
                    Digits: ${data.digits}<br>
                    Result: ${data.result}<br>
                    Status: ${data.status}
                </div>
            `;
            this.addEvent(`⚡ Mined ${digits} Pi digits`);
            this.loadLeaderboard(); // Refresh leaderboard

        } catch (error) {
            console.error('Mining error:', error);
            resultDiv.innerHTML = `<span style="color: #ff6b6b;">❌ Error: ${error.message}</span>`;
        } finally {
            button.disabled = false;
            button.textContent = '🚀 Start Mining';
        }
    }

    async stakeTokens() {
        const amountInput = document.getElementById('stakeAmount');
        const button = document.getElementById('stakeBtn');
        
        const amount = parseInt(amountInput.value);
        if (!amount || amount < 1) {
            alert('Please enter a valid stake amount');
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

            alert(`✅ ${data.message}\nAmount: ${data.amount} tokens`);
            this.addEvent(`💰 Staked ${amount} tokens`);

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

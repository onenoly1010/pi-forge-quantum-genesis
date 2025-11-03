// Pi Forge Quantum Genesis - Frontend
// By Kris Olofson (onenoly11)

class PiForgeApp {
    constructor() {
        this.backendUrl = ''; // Will be set after deployment
        this.socket = null;
        this.init();
    }

    init() {
        this.checkBackendStatus();
        this.setupWebSocket();
        this.loadLeaderboard();
        
        // Auto-refresh leaderboard every 30 seconds
        setInterval(() => this.loadLeaderboard(), 30000);
    }

    async checkBackendStatus() {
        try {
            // Try multiple possible backend URLs
            const possibleUrls = [
                window.location.origin.replace('netlify.app', 'up.railway.app') + '/health',
                'https://pi-forge-quantum-genesis.up.railway.app/health',
                'https://your-app-name.railway.app/health'
            ];

            for (const url of possibleUrls) {
                try {
                    const response = await fetch(url);
                    if (response.ok) {
                        const data = await response.json();
                        this.backendUrl = url.replace('/health', '');
                        this.updateStatus('backend-status', 'connected', `Backend: ${data.status}`);
                        console.log('✅ Backend connected:', this.backendUrl);
                        return;
                    }
                } catch (e) {
                    continue;
                }
            }
            
            // If no backend found, use mock mode
            this.updateStatus('backend-status', 'disconnected', 'Backend: Mock Mode');
            console.warn('🚨 Backend not found - Running in mock mode');
        } catch (error) {
            this.updateStatus('backend-status', 'error', 'Backend: Connection Failed');
            console.error('Backend check failed:', error);
        }
    }

    setupWebSocket() {
        try {
            // Try to connect to WebSocket
            const wsUrl = this.backendUrl ? this.backendUrl.replace('https', 'wss') : 'wss://pi-forge-quantum-genesis.up.railway.app';
            this.socket = io(wsUrl, {
                transports: ['websocket'],
                timeout: 5000
            });

            this.socket.on('connect', () => {
                this.updateStatus('websocket-status', 'connected', 'WebSocket: Connected');
                console.log('✅ WebSocket connected');
            });

            this.socket.on('disconnect', () => {
                this.updateStatus('websocket-status', 'disconnected', 'WebSocket: Disconnected');
            });

            this.socket.on('mining_update', (data) => {
                this.addEvent(`🕶️ VR Mine: ${data.user_id} mined ${data.digits} digits`);
            });

            this.socket.on('quest_complete', (data) => {
                this.addEvent(`⚔️ VR Quest: ${data.user_id} completed ${data.quest}`);
            });

            this.socket.on('connected', (data) => {
                this.addEvent(`🔌 ${data.message}`);
            });

        } catch (error) {
            console.warn('WebSocket setup failed:', error);
            this.updateStatus('websocket-status', 'disconnected', 'WebSocket: Mock Mode');
        }
    }

    updateStatus(elementId, status, text) {
        const element = document.getElementById(elementId);
        const dot = element.querySelector('.status-dot');
        
        element.textContent = text;
        dot.className = 'status-dot ' + status;
        element.appendChild(dot);
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
            let response;
            if (this.backendUrl) {
                response = await fetch(`${this.backendUrl}/compute/${digits}`);
            } else {
                // Mock response
                response = {
                    ok: true,
                    json: async () => ({
                        digits: digits,
                        result: this.calculateMockPi(digits),
                        status: "computed",
                        developer: "Kris Olofson"
                    })
                };
            }

            const data = await response.json();
            
            if (response.ok) {
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
            } else {
                throw new Error(data.error || 'Mining failed');
            }
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
            let response;
            if (this.backendUrl) {
                response = await fetch(`${this.backendUrl}/stake`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: 'kris_olofson',
                        amount: amount
                    })
                });
            } else {
                // Mock response
                response = {
                    ok: true,
                    json: async () => ({
                        status: "staked",
                        amount: amount,
                        user_id: "kris_olofson",
                        message: "Tokens staked successfully"
                    })
                };
            }

            const data = await response.json();
            
            if (response.ok) {
                alert(`✅ ${data.message}\nAmount: ${data.amount} tokens`);
                this.addEvent(`💰 Staked ${amount} tokens`);
            } else {
                throw new Error(data.error || 'Staking failed');
            }
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
            let data;
            if (this.backendUrl) {
                const response = await fetch(`${this.backendUrl}/leaderboard`);
                data = await response.json();
            } else {
                // Mock data
                data = {
                    leaderboard: [
                        { user_id: 'kris_olofson', digits_mined: 1000000 },
                        { user_id: 'quantum_miner', digits_mined: 850000 },
                        { user_id: 'pi_explorer', digits_mined: 720000 },
                        { user_id: 'math_genius', digits_mined: 650000 },
                        { user_id: 'crypto_pioneer', digits_mined: 580000 }
                    ]
                };
            }

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
        
        if (this.socket && this.socket.connected) {
            this.socket.emit('vr_mine', {
                user_id: 'kris_olofson',
                digits: Math.floor(Math.random() * 10000) + 1000
            });
        } else {
            // Mock VR mine
            setTimeout(() => {
                this.addEvent('🕶️ VR Mine: kris_olofson mined 1,247 digits');
            }, 1000);
        }
    }

    startVRQuest() {
        this.addEvent('⚔️ Starting VR quest...');
        
        if (this.socket && this.socket.connected) {
            this.socket.emit('vr_quest', {
                user_id: 'kris_olofson',
                quest: 'quantum_computation'
            });
        } else {
            // Mock VR quest
            setTimeout(() => {
                this.addEvent('⚔️ VR Quest: kris_olofson completed quantum_computation');
            }, 1500);
        }
    }

    addEvent(message) {
        const eventsFeed = document.getElementById('eventsFeed');
        const eventItem = document.createElement('div');
        eventItem.className = 'event-item';
        eventItem.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        
        eventsFeed.prepend(eventItem);
        
        // Keep only last 10 events
        while (eventsFeed.children.length > 10) {
            eventsFeed.removeChild(eventsFeed.lastChild);
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
    app.startMining();
}

function stakeTokens() {
    app.stakeTokens();
}

function loadLeaderboard() {
    app.loadLeaderboard();
}

function startVRMine() {
    app.startVRMine();
}

function startVRQuest() {
    app.startVRQuest();
}

// Initialize app when page loads
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new PiForgeApp();
});

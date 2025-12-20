// Pi Forge Quantum Genesis - Frontend Application
// By Kris Olofson

class PiForgeApp {
    constructor() {
        // Configuration: set BACKEND_URL in index.html or use empty string for mock mode
        this.backendUrl = window.BACKEND_URL || ''; 
        this.socket = null;
        this.mockMode = !this.backendUrl; // Enable mock mode if no backend URL
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
        try {
            const response = await fetch(`${this.backendUrl}/health`);
            const data = await response.json();
            this.updateStatus('backend-status', 'connected', `Backend: ${data.status}`);
        } catch (error) {
            this.updateStatus('backend-status', 'disconnected', 'Backend: Offline');
        }
    }

    setupWebSocket() {
        if (!this.backendUrl) return; // Skip if in mock mode
        
        try {
            this.socket = io(this.backendUrl);
            this.socket.on('connect', () => {
                console.log('✅ WebSocket connected');
                this.addEvent('🔌 Connected to server');
            });
        } catch (error) {
            console.log('WebSocket not available, running in mock mode');
        }
    }

    async startMining() {
        const digitsInput = document.getElementById('digitsInput');
        const resultDiv = document.getElementById('miningResult');
        const button = document.getElementById('mineBtn');
        
        // Use parseInt for whole numbers (digits should be integers)
        const digits = parseInt(digitsInput.value);
        
        // Enhanced validation
        if (!digits || isNaN(digits) || digits < 1) {
            this.showError(resultDiv, '⚠️ Please enter a valid whole number (minimum 1 digit)');
            return;
        }
        
        if (digits > 1000000) {
            this.showError(resultDiv, '⚠️ Maximum 1,000,000 digits allowed');
            return;
        }

        button.disabled = true;
        button.textContent = '⚙️ Mining...';

        try {
            const data = this.backendUrl 
                ? await this.mineFromBackend(digits)
                : this.mockMine(digits);

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
        
        // Use parseFloat to allow decimal token amounts (e.g., 10.5 tokens)
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

        try {
            const data = this.backendUrl
                ? await this.stakeToBackend(amount)
                : {
                status: "staked",
                amount: amount,
                apy: 0.055,
                message: "Tokens staked successfully"
            };

            alert(`✅ ${data.message}\nAmount: ${data.amount.toLocaleString()} tokens\nAPY: 5.5%`);
            this.addEvent(`💰 Staked ${amount.toLocaleString()} tokens`);
            amountInput.value = ''; // Clear input after successful stake

        } catch (error) {
            console.error('Staking error:', error);
            alert(`❌ Error: ${error.message}`);
        } finally {
            button.disabled = false;
        }
    }

    async mineFromBackend(digits) {
        const response = await fetch(`${this.backendUrl}/compute/${digits}`);
        if (!response.ok) throw new Error('Backend request failed');
        return await response.json();
    }

    async stakeToBackend(amount) {
        const response = await fetch(`${this.backendUrl}/stake`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount, user_id: 'quantum_miner' })
        });
        if (!response.ok) throw new Error('Backend request failed');
        return await response.json();
    }

    async loadLeaderboard() {
        const tbody = document.getElementById('leaderboard-body');
        if (!tbody) return;

        try {
            const data = this.backendUrl
                ? await this.fetchLeaderboard()
                : this.mockLeaderboard();

            // Clear existing content
            tbody.innerHTML = '';
            
            // Build rows safely to prevent XSS
            data.forEach((entry, i) => {
                const row = document.createElement('tr');
                
                const rankCell = document.createElement('td');
                rankCell.textContent = i + 1;
                row.appendChild(rankCell);
                
                const userCell = document.createElement('td');
                userCell.textContent = entry.user_id;  // Safe from XSS
                row.appendChild(userCell);
                
                const digitsCell = document.createElement('td');
                digitsCell.textContent = entry.digits_mined.toLocaleString();
                row.appendChild(digitsCell);
                
                tbody.appendChild(row);
            });
        } catch (error) {
            console.error('Leaderboard error:', error);
            tbody.innerHTML = '<tr><td colspan="3">⚠️ Failed to load leaderboard</td></tr>';
        }
    }

    async fetchLeaderboard() {
        const response = await fetch(`${this.backendUrl}/leaderboard`);
        if (!response.ok) throw new Error('Failed to fetch leaderboard');
        return await response.json();
    }

    mockLeaderboard() {
        return [
            { user_id: 'quantum_miner', digits_mined: 98532 },
            { user_id: 'pi_pioneer', digits_mined: 75420 },
            { user_id: 'crypto_sage', digits_mined: 56789 }
        ];
    }

    mockMine(digits) {
        return {
            digits: digits,
            result: this.generateMockPi(digits),
            status: "success",
            mined_at: new Date().toISOString()
        };
    }

    addEvent(message) {
        const container = document.getElementById('eventFeed');
        if (!container) return;

        const event = document.createElement('div');
        event.className = 'event-item';
        event.innerHTML = `<span class="timestamp">${new Date().toLocaleTimeString()}</span> ${message}`;
        container.insertBefore(event, container.firstChild);

        // Limit to 10 events
        while (container.children.length > 10) {
            container.removeChild(container.lastChild);
        }
    }

    updateStatus(id, status, message) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = message;
            element.className = `status ${status}`;
        }
    }

    generateMockPi(digits) {
        const piConstant = "3.14159265358979323846";
        if (digits <= 20) {
            // Return digits+2 characters to include "3." plus the requested decimal places
            return piConstant.substring(0, Math.min(digits + 2, piConstant.length));
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
    window.app.startMining();
}

function stakeTokens() {
    window.app.stakeTokens();
}

function simulateVRMining() {
    if (window.app.socket) {
        window.app.socket.emit('vr_mine', { username: 'quantum_miner', amount: 100 });
    }
    window.app.addEvent('🎮 VR Mining simulation triggered');
}

function submitQuest() {
    if (window.app.socket) {
        window.app.socket.emit('vr_quest', { username: 'quantum_miner', quest: 'Quantum Calibration' });
    }
    window.app.addEvent('🎯 Quest submitted');
}

// Initialize app on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new PiForgeApp();
    console.log('🚀 Pi Forge Quantum Genesis - Mock Mode Active');
});

// PiForge Integration Module
const PiForge = {
    // Activate Mining Boost via Pi SDK
    async activateMiningBoost(boostPercent) {
        try {
            const paymentData = {
                amount: (boostPercent / 100) * 0.15, // Example: 15% boost as 0.15 Pi
                memo: `PiForge Boost: ${boostPercent}% Ethical Resonance Activated`,
                metadata: { type: 'mining_boost' }
            };
            const result = await Pi.createPayment(paymentData, {
                onReadyForServerApproval: (paymentId) => {
                    console.log('Payment ready for approval:', paymentId);
                },
                onPaymentSuccess: (payment) => {
                    document.getElementById('status').textContent += ` | Boost Activated: +${boostPercent}% Mining!`;
                    // Trigger resonance ritual viz (SVG animation)
                    PiForge.renderResonanceViz(payment.metadata);
                },
                onPaymentError: (error) => {
                    console.error('Boost Payment Error:', error);
                }
            });
        } catch (err) {
            console.error('Mining Boost Failed:', err);
        }
    },

    // Render Onion-Pi Fractal Viz (SVG Animation)
    renderResonanceViz(metadata) {
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', '300');
        svg.setAttribute('height', '300');
        svg.setAttribute('viewBox', '0 0 300 300');
        svg.style.position = 'fixed';
        svg.style.top = '10px';
        svg.style.right = '10px';
        svg.style.zIndex = '1000';

        // Simple fractal circle animation (4-phase cascade)
        for (let i = 0; i < 4; i++) {
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', 150);
            circle.setAttribute('cy', 150);
            circle.setAttribute('r', 50 + i * 30);
            circle.setAttribute('fill', 'none');
            circle.setAttribute('stroke', `hsl(${i * 90}, 100%, 50%)`);
            circle.setAttribute('stroke-width', 2);
            circle.style.animation = `resonate ${2 + i}s linear infinite`;
            svg.appendChild(circle);
        }

        document.body.appendChild(svg);

        // CSS Animation Keyframes (injected)
        const style = document.createElement('style');
        style.textContent = `
            @keyframes resonate {
                0% { transform: scale(1) rotate(0deg); opacity: 1; }
                50% { transform: scale(1.5) rotate(180deg); opacity: 0.5; }
                100% { transform: scale(1) rotate(360deg); opacity: 1; }
            }
        `;
        document.head.appendChild(style);

        // Remove after 10s
        setTimeout(() => svg.remove(), 10000);
    },

    // Ethical Scoring Helper (client-side validation)
    computeResonance(ethicalScore, qualiaImpact) {
        return Math.floor((ethicalScore * 0.7 + qualiaImpact * 3) / 10); // Simplified formula
    }
};

// Export for global use
window.PiForge = PiForge;
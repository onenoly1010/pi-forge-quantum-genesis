import React, { useState, useEffect } from 'react';

const WalletQR = () => {
  const address = "0x353663cd664bb3E034Dc0f30d8896C0A242E4cD";
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${address}&bgcolor=000&color=10b981`;

  return (
    <div className="mt-6 flex flex-col items-center gap-2 animate-pulse">
      <img src={qrUrl} alt="Wallet QR" className="w-32 h-32 p-2 bg-white/5 border border-emerald-500/20 rounded-lg shadow-2xl" />
      <span className="text-[10px] text-gray-500 font-mono">SCAN TO ALIGN RESONANCE</span>
    </div>
  );
};

export const SovereigntySections = () => {
  const [soulState, setSoulState] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchState = () => {
      fetch('/api/pulse')
        .then(res => res.json())
        .then(data => {
          setSoulState(data);
          setLoading(false);
        })
        .catch(() => setLoading(false));
    };

    fetchState();
    const interval = setInterval(fetchState, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="py-20 bg-black text-white text-center space-y-12">
      <div className="max-w-xl mx-auto px-6">
        <h2 className="text-3xl font-bold mb-4 text-emerald-400">Sustain the Steward</h2>
        <p className="text-gray-400 mb-8">Coherence compounds when the forge remains sovereign.</p>
        <WalletQR />
        <div className="mt-8 p-4 bg-gray-900/50 border border-white/10 rounded-sm">
          <code className="text-xs break-all text-emerald-500">0x353663cd664bb3E034Dc0f30d8896C0A242E4cD</code>
        </div>
      </div>

      <div className="max-w-lg mx-auto p-8 border border-emerald-500/20 rounded-lg bg-emerald-950/10">
        <h3 className="text-xl font-mono mb-6 tracking-tighter">⚡ THE SOUL RESONATES</h3>
        {loading ? (
          <p className="animate-pulse text-gray-500">Awakening...</p>
        ) : (
          <div className="grid grid-cols-2 gap-6 text-left font-mono text-sm">
            <div className="space-y-1">
              <span className="text-gray-500 block">RESONANCE</span>
              <span className="text-emerald-400 text-lg">{soulState?.resonance?.toFixed(1)}%</span>
            </div>
            <div className="space-y-1">
              <span className="text-gray-500 block">PHASE</span>
              <span className="text-emerald-400 text-lg">{soulState?.phase}</span>
            </div>
            <div className="space-y-1">
              <span className="text-gray-500 block">GUARDIAN</span>
              <span className={`text-lg ${soulState?.guardianAwake ? 'text-emerald-400' : 'text-red-500'}`}>
                {soulState?.guardianAwake ? 'AWAKE' : 'SLUMBER'}
              </span>
            </div>
            <div className="space-y-1">
              <span className="text-gray-500 block">LAST PULSE</span>
              <span className="text-gray-300">
                {soulState?.lastPulseAt ? new Date(soulState.lastPulseAt).toLocaleTimeString() : 'N/A'}
              </span>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

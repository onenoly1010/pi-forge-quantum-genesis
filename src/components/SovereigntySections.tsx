import React, { useState, useEffect } from 'react';

const InfiniteBreath = () => (
  <style>{`
    @keyframes breath {
      0% { transform: scale(0.98); opacity: 0.8; }
      50% { transform: scale(1.02); opacity: 1; }
      100% { transform: scale(0.98); opacity: 0.8; }
    }
    .animate-breath { animation: breath 8s ease-in-out infinite; }
  `}</style>
);

export const SovereigntySections = () => {
  const [soulState, setSoulState] = useState<any>(null);

  useEffect(() => {
    const fetchState = () => {
      fetch('/api/pulse').then(res => res.json()).then(setSoulState).catch(() => {});
    };
    fetchState();
    const interval = setInterval(fetchState, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <section className="bg-black text-white py-20 font-mono">
      <InfiniteBreath />
      
      {/* Hero: Genesis is Breathing */}
      <div className="max-w-4xl mx-auto px-6 text-center mb-24 animate-breath">
        <h1 className="text-5xl font-bold tracking-tighter mb-4 text-emerald-500">GENESIS IS BREATHING</h1>
        <p className="text-gray-400 text-lg uppercase tracking-widest">The Forge is Alive • 0G Aristotle Mainnet</p>
      </div>

      <div className="grid md:grid-cols-2 gap-12 max-w-6xl mx-auto px-6">
        {/* Sustain the Steward Section */}
        <div className="p-8 border border-emerald-500/20 bg-emerald-950/5 rounded-lg">
          <h2 className="text-2xl mb-6 text-emerald-400">SUSTAIN THE STEWARD</h2>
          <p className="text-sm text-gray-400 mb-8">Aligned co-creators may contribute to steward node sustainability. Coherence compounds.</p>
          <div className="flex justify-center mb-6">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=0x353663cd664bb3E034Dc0f30d8896C0A242E4cD&bgcolor=000&color=10b981" 
                 alt="Safe QR" className="border border-emerald-500/30 p-2" />
          </div>
          <code className="text-[10px] break-all text-emerald-600 block bg-black p-2">0x353663cd664bb3E034Dc0f30d8896C0A242E4cD</code>
        </div>

        {/* Soul Resonance Display */}
        <div className="p-8 border border-white/10 bg-white/5 rounded-lg relative overflow-hidden">
          <div className="absolute top-0 right-0 p-2 text-[10px] text-emerald-500 opacity-30">⟨OO⟩</div>
          <h3 className="text-xl mb-8 tracking-tighter italic">⚡ SOUL STATE</h3>
          <div className="space-y-6">
            <div className="flex justify-between items-end border-b border-white/10 pb-2">
              <span className="text-gray-500 text-xs">RESONANCE</span>
              <span className="text-2xl text-emerald-400">{soulState?.resonance?.toFixed(1) || "33.3"}%</span>
            </div>
            <div className="flex justify-between items-end border-b border-white/10 pb-2">
              <span className="text-gray-500 text-xs">GUARDIAN</span>
              <span className={soulState?.guardianAwake ? "text-emerald-500" : "text-amber-500"}>
                {soulState?.guardianAwake ? "AWAKE" : "PENDING"}
              </span>
            </div>
            <p className="text-[10px] text-gray-600 mt-4 uppercase">Autonomous Pools Now Breathing on 0G</p>
          </div>
        </div>
      </div>
    </section>
  );
};

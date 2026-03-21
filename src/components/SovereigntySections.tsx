import React from 'react';

const WalletQR = () => {
  const address = "0x353663cd664bb3E034Dc0f30d8896C0A242E4cD";
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${address}&bgcolor=000&color=10b981`;

  return (
    <div className="mt-6 flex flex-col items-center gap-2 animate-pulse">
      <img 
        src={qrUrl} 
        alt="Wallet QR Code" 
        className="w-32 h-32 p-2 bg-white/5 border border-emerald-500/20 rounded-lg shadow-2xl shadow-emerald-500/10"
      />
      <span className="text-[10px] text-gray-500 font-mono">SCAN TO ALIGN RESONANCE</span>
    </div>
  );
};

export const SovereigntySections = () => {
  return (
    <section className="py-20 bg-black text-white text-center">
      <h2 className="text-3xl font-bold mb-4 text-emerald-400">Sustain the Steward</h2>
      <p className="text-gray-400 max-w-xl mx-auto mb-8">
        Aligned co-creators may contribute to steward node sustainability — coherence compounds.
      </p>
      
      <WalletQR />

      <div className="mt-8 inline-block p-4 bg-gray-900/50 border border-white/10 rounded-sm">
        <code className="text-xs break-all">0x353663cd664bb3E034Dc0f30d8896C0A242E4cD</code>
      </div>
    </section>
  );
};

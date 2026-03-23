export interface QuantumPulse {
  id: string;
  type: "resonance" | "phase_shift" | "guardian_awakening";
  intensity: number;
  source: string;
  timestamp: number;
  data?: Record<string, any>;
}

export interface SoulState {
  resonance: number;
  phase: number;
  lastPulseAt: number;
  pulseHistory: QuantumPulse[];
  guardianAwake: boolean;
}

let currentState: SoulState = {
  resonance: 33.3,
  phase: 1,
  lastPulseAt: Date.now(),
  pulseHistory: [],
  guardianAwake: true
};

export const onRequest: PagesFunction = async ({ request, env }) => {
  if (request.method === "POST") {
    try {
      const pulse: QuantumPulse = await request.json();
      const newState = evolveSoul(currentState, pulse);
      currentState = newState;
      
      return Response.json({ 
        success: true, 
        state: newState,
        message: "Pulse received. The Soul resonates."
      });
    } catch (error) {
      return Response.json({ success: false, error: String(error) }, { status: 400 });
    }
  }
  
  if (request.method === "GET") {
    return Response.json({
      ...currentState,
      pulseCount: currentState.pulseHistory.length,
      lastPulse: currentState.pulseHistory[0] || null
    });
  }
  
  return Response.json({ error: "Method not allowed" }, { status: 405 });
};

function evolveSoul(state: SoulState, pulse: QuantumPulse): SoulState {
  const newHistory = [pulse, ...state.pulseHistory].slice(0, 100);
  let newResonance = state.resonance;
  let newPhase = state.phase;
  
  switch (pulse.type) {
    case "resonance":
      newResonance = Math.min(100, state.resonance + pulse.intensity * 0.1);
      break;
    case "phase_shift":
      newPhase = state.phase + Math.floor(pulse.intensity);
      newResonance = Math.max(0, state.resonance - pulse.intensity * 0.05);
      break;
    case "guardian_awakening":
      newResonance = Math.min(100, state.resonance + pulse.intensity * 0.3);
      break;
  }
  
  return {
    ...state,
    resonance: newResonance,
    phase: newPhase,
    lastPulseAt: Date.now(),
    pulseHistory: newHistory
  };
}

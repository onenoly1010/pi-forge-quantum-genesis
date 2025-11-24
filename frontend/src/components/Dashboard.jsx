import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [auditData, setAuditData] = useState(null);
  const [transactionResult, setTransactionResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [txLoading, setTxLoading] = useState(false);
  const [isDemoMode, setIsDemoMode] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://zealous-laughter.up.railway.app';

  // Poll the /api/status endpoint every 5 seconds with silent failover
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch(`${apiUrl}/api/status`);
        const data = await response.json();
        setAuditData(data);
        setIsDemoMode(false);
        setLoading(false);
      } catch (error) {
        // Silent failover to Demo Mode - no console spam
        setIsDemoMode(true);
        setAuditData({
          status: 'ONLINE',
          traffic: 'DEMO',
          threatLevel: 'GREEN',
          timestamp: new Date().toISOString()
        });
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);

    return () => clearInterval(interval);
  }, [apiUrl]);

  // Handle transaction test with demo fallback
  const testTransaction = async () => {
    setTxLoading(true);
    try {
      const response = await fetch(`${apiUrl}/api/audit-tx`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ txId: `test_tx_${Date.now()}` }),
      });
      const result = await response.json();
      setTransactionResult(result);
    } catch (error) {
      // Demo transaction result when backend is unavailable
      setTransactionResult({
        txId: `demo_tx_${Date.now()}`,
        ruleCheck: 'PASS',
        auditLevel: 'ETHICAL',
        gargouraSignal: 'CLEAR',
        isDemo: true
      });
    } finally {
      setTxLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <h1>Quantum Pi Forge Dashboard {isDemoMode && <span className="demo-badge">DEMO MODE</span>}</h1>
      
      {/* Gargoura Watcher Status */}
      <div className="status-card">
        <h2>Gargoura Watcher {isDemoMode && <span className="demo-indicator">(Live Demo)</span>}</h2>
        {loading ? (
          <p>Connecting to Quantum Network...</p>
        ) : auditData ? (
          <div>
            <p>Status: <span className={auditData.status === 'ONLINE' ? 'green' : 'red'}>{auditData.status}</span></p>
            <p>Traffic: {auditData.traffic}</p>
            <p>Threat Level: <span className={auditData.threatLevel === 'GREEN' ? 'green' : auditData.threatLevel === 'RED' ? 'red' : 'yellow'}>{auditData.threatLevel}</span></p>
            <p>Last Updated: {new Date(auditData.timestamp).toLocaleString()}</p>
            <p>Network Volume: &gt;145,000 {isDemoMode && '(Simulated)'}</p>
            {isDemoMode && (
              <p className="demo-note">🔶 Connected in demo mode - real data when available</p>
            )}
          </div>
        ) : (
          <p>Initializing quantum systems...</p>
        )}
      </div>

      {/* Transaction Test Button */}
      <div className="transaction-test">
        <h2>Test Transaction Ritual</h2>
        <button onClick={testTransaction} disabled={txLoading}>
          {txLoading ? 'Auditing...' : 'Simulate Transaction'}
        </button>
        
        {transactionResult && (
          <div className={`result ${transactionResult.ruleCheck === 'PASS' ? 'approved' : 'blocked'}`}> 
            <h3>Transaction Audit Result {transactionResult.isDemo && '(Demo)'}</h3>
            <p>TxID: {transactionResult.txId}</p>
            <p>Rule Check: {transactionResult.ruleCheck}</p>
            <p>Audit Level: {transactionResult.auditLevel}</p>
            <p>Gargoura Signal: {transactionResult.gargouraSignal}</p>
            {transactionResult.error && <p>Error: {transactionResult.error}</p>}
            {transactionResult.isDemo && (
              <p className="demo-note">🔶 Demo transaction - real audit when backend available</p>
            )}
          </div>
        )}
      </div>

      <style jsx>{`
        .dashboard {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          font-family: Arial, sans-serif;
        }
        .status-card, .transaction-test {
          border: 1px solid #ccc;
          padding: 20px;
          margin: 20px 0;
          border-radius: 8px;
        }
        .demo-badge {
          background: #ffc107;
          color: #000;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 14px;
          margin-left: 10px;
        }
        .demo-indicator {
          color: #666;
          font-size: 14px;
          font-weight: normal;
        }
        .demo-note {
          color: #666;
          font-style: italic;
          margin-top: 10px;
        }
        .green { color: green; }
        .red { color: red; }
        .yellow { color: orange; }
        .approved { background-color: #d4edda; border-color: #c3e6cb; }
        .blocked { background-color: #f8d7da; border-color: #f5c6cb; }
        button {
          padding: 10px 20px;
          background-color: #007bff;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
        }
        button:disabled { background-color: #ccc; cursor: not-allowed; }
      `}</style>
    </div>
  );
}
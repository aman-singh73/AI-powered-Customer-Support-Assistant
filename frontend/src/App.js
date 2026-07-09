import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [backendStatus, setBackendStatus] = useState('Checking...');
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

  useEffect(() => {
    // Test backend connection
    const checkBackend = async () => {
      try {
        const response = await fetch(`${backendUrl}/health`);
        if (response.ok) {
          const data = await response.json();
          setBackendStatus('Connected to backend successfully!');
        } else {
          setBackendStatus('Backend responded with an error.');
        }
      } catch (error) {
        setBackendStatus('Failed to connect to backend. Make sure the backend service is running.');
        console.error('Backend connection error:', error);
      }
    };

    checkBackend();
    // Check connection every 30 seconds
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, [backendUrl]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to React</h1>
        <div style={{ 
          marginTop: '20px', 
          padding: '20px', 
          borderRadius: '8px', 
          background: '#2c3e50',
          color: '#ecf0f1',
          maxWidth: '600px',
          width: '90%'
        }}>
          <h2 style={{ margin: '0 0 15px 0', color: '#3498db' }}>System Status</h2>
          <div style={{ 
            padding: '15px', 
            borderRadius: '5px', 
            background: '#34495e',
            marginBottom: '10px'
          }}>
            <p style={{ margin: '0', fontWeight: 'bold' }}>Backend Status:</p>
            <p style={{ margin: '5px 0 0 0', color: backendStatus.includes('success') ? '#2ecc71' : '#e74c3c' }}>
              {backendStatus}
            </p>
          </div>
          <div style={{ 
            padding: '15px', 
            borderRadius: '5px', 
            background: '#34495e'
          }}>
            <p style={{ margin: '0', fontWeight: 'bold' }}>Backend URL:</p>
            <p style={{ margin: '5px 0 0 0', color: '#3498db' }}>{backendUrl}</p>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
// src/App.js
import React from 'react';
import Calendar from './components/Calendar';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <img src="/canopyai-logo.png" alt="CanopyAI System" className="university-logo" />
        <div className="header-text">
          <h1>Redwood Digital University</h1>
          <h2>Academic Calendar System</h2>
          <p className="powered-by">Powered by CanopyAI</p>
        </div>
      </header>
      <Calendar />
    </div>
  );
}

export default App;

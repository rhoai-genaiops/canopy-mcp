// src/App.js
import React from 'react';
import Calendar from './components/Calendar';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <img src="/canopyai-logo.png" alt="CanopyAI University" className="university-logo" />
        <div className="header-text">
          <h1>CanopyAI University</h1>
          <h2>Academic Calendar</h2>
        </div>
      </header>
      <Calendar />
    </div>
  );
}

export default App;

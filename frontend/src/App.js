import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Home from './pages/Home';
import PDFViewer from './pages/PDFViewer';
import PersonaAnalysis from './pages/PersonaAnalysis';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="min-h-screen bg-gray-50">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/viewer" element={<PDFViewer />} />
            <Route path="/persona-analysis" element={<PersonaAnalysis />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 
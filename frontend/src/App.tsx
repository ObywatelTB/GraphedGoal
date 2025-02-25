import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import HistoryPage from './pages/HistoryPage';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>
        <footer className="footer">
          <div className="container">
            <p>&copy; {new Date().getFullYear()} GraphedGoal. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
};

export default App; 
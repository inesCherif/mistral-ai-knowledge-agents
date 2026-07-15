import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/globals.css';
import Sidebar from './components/Sidebar';
import ChatPage from './pages/ChatPage';
import ModelsPage from './pages/ModelsPage';
import ResearchPage from './pages/ResearchPage';
import GitHubPage from './pages/GitHubPage';
import ContactsPage from './pages/ContactsPage';

function App() {
  return (
    <Router>
      <div className="app-layout">
        <Sidebar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<ChatPage />} />
            <Route path="/models" element={<ModelsPage />} />
            <Route path="/research" element={<ResearchPage />} />
            <Route path="/github" element={<GitHubPage />} />
            <Route path="/contacts" element={<ContactsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

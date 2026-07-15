import React from 'react';
import { useLocation, Link } from 'react-router-dom';

const NAV_ITEMS = [
  { path: '/', icon: '💬', label: 'Chat', section: 'main' },
  { path: '/models', icon: '🧠', label: 'Models', section: 'explore' },
  { path: '/research', icon: '📄', label: 'Research', section: 'explore' },
  { path: '/github', icon: '💻', label: 'GitHub', section: 'explore' },
  { path: '/contacts', icon: '📬', label: 'Contacts', section: 'explore' },
];

function Sidebar() {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">M</div>
        <div className="sidebar-logo-text">
          Mistral<span>Bot</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="sidebar-section-label">Chat</div>
        {NAV_ITEMS.filter(n => n.section === 'main').map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="nav-item-icon">{item.icon}</span>
            {item.label}
          </Link>
        ))}

        <div className="sidebar-section-label" style={{ marginTop: 16 }}>Explore</div>
        {NAV_ITEMS.filter(n => n.section === 'explore').map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <span className="nav-item-icon">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span className="status-dot" />
        API Connected
      </div>
    </aside>
  );
}

export default Sidebar;

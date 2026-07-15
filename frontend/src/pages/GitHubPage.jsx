import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

const LANG_COLORS = {
  Python: '#3572A5',
  TypeScript: '#3178C6',
  JavaScript: '#F7DF1E',
  Jupyter: '#DA5B0B',
};

function RepoCard({ repo }) {
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <span
          style={{
            width: 10, height: 10, borderRadius: '50%',
            background: LANG_COLORS[repo.language] || '#ccc', flexShrink: 0,
          }}
        />
        <span className="meta-pill">{repo.language}</span>
        <span className="header-badge badge-github">{repo.license}</span>
      </div>

      <div className="card-title">{repo.name}</div>
      <div className="card-description">{repo.description}</div>

      <div className="flex gap-3 mb-4" style={{ fontSize: '0.82rem', color: 'var(--color-text-secondary)' }}>
        <span>⭐ {repo.stars.toLocaleString()}</span>
        <span>🍴 {repo.forks.toLocaleString()}</span>
        <span>🐛 {repo.open_issues} issues</span>
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 14 }}>
        {repo.topics.map(t => (
          <span key={t} className="meta-pill">{t}</span>
        ))}
      </div>

      <div className="flex gap-2">
        <a href={repo.url} target="_blank" rel="noopener noreferrer" className="source-chip github">
          💻 View on GitHub
        </a>
      </div>
      <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)', marginTop: 10 }}>
        Updated: {repo.last_updated}
      </div>
    </div>
  );
}

function GitHubPage() {
  const [repos, setRepos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getRepos()
      .then(setRepos)
      .catch(() => setRepos([]))
      .finally(() => setLoading(false));
  }, []);

  const totalStars = repos.reduce((a, r) => a + r.stars, 0);
  const totalForks = repos.reduce((a, r) => a + r.forks, 0);

  return (
    <div className="main-content">
      <div className="page-header">
        <div>
          <div className="page-header-title">💻 GitHub Repositories</div>
          <div className="page-header-subtitle">
            <a href="https://github.com/mistralai" target="_blank" rel="noopener noreferrer">
              github.com/mistralai
            </a>
          </div>
        </div>
      </div>

      <div className="page-content">
        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-card-icon">📦</div>
            <div className="stat-card-value">{repos.length}</div>
            <div className="stat-card-label">Repositories</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-icon">⭐</div>
            <div className="stat-card-value">{(totalStars / 1000).toFixed(1)}K</div>
            <div className="stat-card-label">Total Stars</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-icon">🍴</div>
            <div className="stat-card-value">{(totalForks / 1000).toFixed(1)}K</div>
            <div className="stat-card-label">Total Forks</div>
          </div>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: 60, color: 'var(--color-text-muted)' }}>Loading repos…</div>
        ) : (
          <div className="card-grid">
            {repos.map(r => <RepoCard key={r.id} repo={r} />)}
          </div>
        )}
      </div>
    </div>
  );
}

export default GitHubPage;

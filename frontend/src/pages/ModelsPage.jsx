import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

const TYPE_COLORS = {
  generalist: { bg: '#EFF6FF', color: '#3B82F6', label: 'Generalist' },
  moe: { bg: '#F5F3FF', color: '#8B5CF6', label: 'MoE' },
  code: { bg: '#ECFDF5', color: '#10B981', label: 'Code' },
  math: { bg: '#FFF7ED', color: '#F97316', label: 'Math' },
  embed: { bg: '#FFFBEB', color: '#D97706', label: 'Embedding' },
};

function BenchmarkBar({ value, max = 100 }) {
  return (
    <div className="bench-bar-cell">
      <span style={{ width: 40, textAlign: 'right', fontSize: '0.82rem', fontWeight: 600 }}>
        {value}
      </span>
      <div className="bench-bar-bg">
        <div className="bench-bar-fill" style={{ width: `${(value / max) * 100}%` }} />
      </div>
    </div>
  );
}

function ModelCard({ model }) {
  const [expanded, setExpanded] = useState(false);
  const typeInfo = TYPE_COLORS[model.type] || TYPE_COLORS.generalist;
  const benchKeys = Object.keys(model.benchmarks || {});

  return (
    <div className="card" style={{ cursor: 'pointer' }} onClick={() => setExpanded(!expanded)}>
      <div className="flex items-center gap-2 mb-4">
        <span
          className="header-badge"
          style={{ background: typeInfo.bg, color: typeInfo.color }}
        >
          {typeInfo.label}
        </span>
        <span className="meta-pill">{model.parameters}</span>
        {model.open_source && <span className="meta-pill">🔓 Open Source</span>}
      </div>

      <div className="card-title">{model.name}</div>
      <div className="card-description">{model.description}</div>

      <div className="card-meta">
        <span className="meta-pill">📐 {model.context_length.toLocaleString()} ctx</span>
        <span className="meta-pill">⚖️ {model.license}</span>
        <span className="meta-pill">📅 {model.release_date}</span>
      </div>

      {model.api_endpoint && (
        <div className="text-sm text-muted" style={{ marginBottom: 12 }}>
          API: <code style={{ background: '#F3F4F6', padding: '2px 6px', borderRadius: 4 }}>
            {model.api_endpoint}
          </code>
        </div>
      )}

      {expanded && benchKeys.length > 0 && (
        <div style={{ marginTop: 14, borderTop: '1px solid var(--color-border)', paddingTop: 14 }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, marginBottom: 8, color: 'var(--color-text-secondary)' }}>
            Benchmarks
          </div>
          <table style={{ width: '100%' }}>
            <tbody>
              {benchKeys.map(b => (
                <tr key={b}>
                  <td style={{ fontSize: '0.8rem', color: 'var(--color-text-secondary)', width: 100, paddingBottom: 6 }}>{b}</td>
                  <td><BenchmarkBar value={model.benchmarks[b]} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: 12 }}>
        {expanded ? '▲ Click to collapse' : '▼ Click to see benchmarks'}
      </div>
    </div>
  );
}

function ModelsPage() {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    api.getModels()
      .then(setModels)
      .catch(() => setModels([]))
      .finally(() => setLoading(false));
  }, []);

  const types = ['all', ...new Set(models.map(m => m.type))];
  const filtered = filter === 'all' ? models : models.filter(m => m.type === filter);

  return (
    <div className="main-content">
      <div className="page-header">
        <div>
          <div className="page-header-title">🧠 Mistral Models</div>
          <div className="page-header-subtitle">{models.length} models available</div>
        </div>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 8 }}>
          {types.map(t => (
            <button
              key={t}
              onClick={() => setFilter(t)}
              className={`suggestion-chip`}
              style={filter === t ? {
                borderColor: 'var(--color-primary)',
                color: 'var(--color-primary)',
                background: 'var(--color-primary-bg)',
              } : {}}
            >
              {t === 'all' ? 'All' : TYPE_COLORS[t]?.label || t}
            </button>
          ))}
        </div>
      </div>

      <div className="page-content">
        {/* Stats */}
        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-card-icon">🧠</div>
            <div className="stat-card-value">{models.length}</div>
            <div className="stat-card-label">Total Models</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-icon">🔓</div>
            <div className="stat-card-value">{models.filter(m => m.open_source).length}</div>
            <div className="stat-card-label">Open Source</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-icon">📐</div>
            <div className="stat-card-value">131K</div>
            <div className="stat-card-label">Max Context</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-icon">⭐</div>
            <div className="stat-card-value">81.2</div>
            <div className="stat-card-label">Best MMLU</div>
          </div>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: 60, color: 'var(--color-text-muted)' }}>
            Loading models…
          </div>
        ) : (
          <div className="card-grid">
            {filtered.map(model => <ModelCard key={model.id} model={model} />)}
          </div>
        )}
      </div>
    </div>
  );
}

export default ModelsPage;

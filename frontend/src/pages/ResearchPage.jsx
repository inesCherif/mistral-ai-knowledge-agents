import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

function PaperCard({ paper }) {
  const [expanded, setExpanded] = useState(false);
  const benchKeys = Object.keys(paper.benchmarks || {});

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <span className="header-badge badge-research">📄 arXiv:{paper.arxiv_id}</span>
        <span className="meta-pill">📅 {paper.published}</span>
      </div>

      <div className="card-title">{paper.title}</div>

      <div className="text-sm text-muted" style={{ marginBottom: 10 }}>
        {paper.authors.slice(0, 4).join(', ')}{paper.authors.length > 4 ? ` + ${paper.authors.length - 4} others` : ''}
      </div>

      <div className="card-description" style={{ display: expanded ? 'block' : '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
        {paper.abstract}
      </div>

      <button
        style={{ background: 'none', border: 'none', color: 'var(--color-primary)', cursor: 'pointer', fontSize: '0.8rem', padding: '4px 0', marginBottom: 12 }}
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? '▲ Show less' : '▼ Read more'}
      </button>

      {benchKeys.length > 0 && (
        <div style={{ borderTop: '1px solid var(--color-border)', paddingTop: 12, marginBottom: 12 }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', marginBottom: 8 }}>KEY BENCHMARKS</div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {benchKeys.map(b => (
              <div key={b} style={{ textAlign: 'center', padding: '8px 14px', background: 'var(--color-research-bg)', borderRadius: 8 }}>
                <div style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-research)' }}>{paper.benchmarks[b]}</div>
                <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)' }}>{b}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-2">
        <a href={paper.url} target="_blank" rel="noopener noreferrer" className="source-chip paper">
          🔗 arXiv
        </a>
        <a href={paper.pdf_url} target="_blank" rel="noopener noreferrer" className="source-chip paper">
          📄 PDF
        </a>
      </div>
    </div>
  );
}

function ResearchPage() {
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getPapers()
      .then(setPapers)
      .catch(() => setPapers([]))
      .finally(() => setLoading(false));
  }, []);

  const allBenchmarks = {};
  papers.forEach(p => {
    Object.entries(p.benchmarks || {}).forEach(([k, v]) => {
      if (!allBenchmarks[k] || v > allBenchmarks[k].value) {
        allBenchmarks[k] = { value: v, model: p.title };
      }
    });
  });

  return (
    <div className="main-content">
      <div className="page-header">
        <div>
          <div className="page-header-title">📄 Research Papers</div>
          <div className="page-header-subtitle">{papers.length} papers indexed</div>
        </div>
      </div>

      <div className="page-content">
        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-card-icon">📄</div>
            <div className="stat-card-value">{papers.length}</div>
            <div className="stat-card-label">Papers</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-icon">👥</div>
            <div className="stat-card-value">26</div>
            <div className="stat-card-label">Unique Authors</div>
          </div>
          <div className="stat-card">
            <div className="stat-card-icon">🏆</div>
            <div className="stat-card-value">81.2</div>
            <div className="stat-card-label">Best MMLU</div>
          </div>
        </div>

        {/* Benchmark Comparison Table */}
        {papers.length > 0 && (
          <div className="card mb-6">
            <div className="section-title">📊 Benchmark Comparison</div>
            <div style={{ overflowX: 'auto' }}>
              <table className="bench-table">
                <thead>
                  <tr>
                    <th>Model</th>
                    {['MMLU', 'HumanEval', 'GSM8K', 'HellaSwag', 'WinoGrande'].map(b => (
                      <th key={b}>{b}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {papers.map(p => (
                    <tr key={p.id}>
                      <td style={{ fontWeight: 600 }}>{p.title}</td>
                      {['MMLU', 'HumanEval', 'GSM8K', 'HellaSwag', 'WinoGrande'].map(b => (
                        <td key={b}>
                          {p.benchmarks?.[b] != null ? (
                            <span style={{ fontWeight: 500 }}>{p.benchmarks[b]}</span>
                          ) : (
                            <span style={{ color: 'var(--color-text-muted)' }}>—</span>
                          )}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', padding: 60, color: 'var(--color-text-muted)' }}>Loading papers…</div>
        ) : (
          <div className="card-grid">
            {papers.map(p => <PaperCard key={p.id} paper={p} />)}
          </div>
        )}
      </div>
    </div>
  );
}

export default ResearchPage;

import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

function PersonCard({ person }) {
  return (
    <div className="contact-card">
      <div
        className="contact-avatar"
        style={{ background: person.avatar_color }}
      >
        {person.avatar_initials}
      </div>
      <div className="contact-info">
        <div className="contact-name">{person.name}</div>
        <div className="contact-role">{person.role} · {person.location}</div>
        <div className="contact-bio">{person.bio}</div>
        <div className="contact-links">
          {person.linkedin && (
            <a href={person.linkedin} target="_blank" rel="noopener noreferrer" className="contact-link">
              🔗 LinkedIn
            </a>
          )}
          {person.twitter && (
            <a href={person.twitter} target="_blank" rel="noopener noreferrer" className="contact-link">
              🐦 Twitter/X
            </a>
          )}
          {person.github && (
            <a href={person.github} target="_blank" rel="noopener noreferrer" className="contact-link">
              💻 GitHub
            </a>
          )}
          {person.arxiv_author && (
            <a
              href={`https://arxiv.org/search/?query=${encodeURIComponent(person.arxiv_author)}&searchtype=author`}
              target="_blank"
              rel="noopener noreferrer"
              className="contact-link"
            >
              📄 arXiv
            </a>
          )}
        </div>
      </div>
    </div>
  );
}

function OfficialContactsSection({ contacts }) {
  const groups = { email: [], social: [], site: [] };
  contacts.forEach(c => { if (groups[c.type]) groups[c.type].push(c); });

  return (
    <div className="card mb-6">
      <div className="section-title">📞 Official Channels</div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
        {Object.entries(groups).map(([type, items]) =>
          items.length > 0 && (
            <div key={type}>
              <div style={{ fontSize: '0.72rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--color-text-muted)', marginBottom: 10 }}>
                {type === 'email' ? '✉️ Email' : type === 'social' ? '🌐 Social' : '🔗 Links'}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {items.map(c => (
                  <a key={c.label} href={c.url} target="_blank" rel="noopener noreferrer"
                    style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px', background: 'var(--color-bg)', borderRadius: 8, border: '1px solid var(--color-border)', textDecoration: 'none', transition: 'border-color 0.15s' }}
                    onMouseEnter={e => e.currentTarget.style.borderColor = 'var(--color-primary)'}
                    onMouseLeave={e => e.currentTarget.style.borderColor = 'var(--color-border)'}
                  >
                    <span style={{ fontSize: '0.82rem', color: 'var(--color-text-primary)', fontWeight: 500 }}>{c.label}</span>
                    <span style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>{c.value}</span>
                  </a>
                ))}
              </div>
            </div>
          )
        )}
      </div>
    </div>
  );
}

function ContactsPage() {
  const [team, setTeam] = useState([]);
  const [official, setOfficial] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    Promise.all([api.getTeam(), api.getOfficialContacts()])
      .then(([t, o]) => { setTeam(t); setOfficial(o); })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = team.filter(p =>
    !search || p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.role.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="main-content">
      <div className="page-header">
        <div>
          <div className="page-header-title">📬 Team & Contacts</div>
          <div className="page-header-subtitle">{team.length} key people</div>
        </div>
        <div style={{ marginLeft: 'auto' }}>
          <input
            type="text"
            placeholder="Search by name or role…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{
              border: '1.5px solid var(--color-border)', borderRadius: 8,
              padding: '8px 14px', fontSize: '0.875rem', outline: 'none',
              fontFamily: 'var(--font-sans)', width: 220,
            }}
          />
        </div>
      </div>

      <div className="page-content">
        {official.length > 0 && <OfficialContactsSection contacts={official} />}

        <div className="section-title">👥 Key Team Members</div>
        {loading ? (
          <div style={{ textAlign: 'center', padding: 60, color: 'var(--color-text-muted)' }}>Loading contacts…</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {filtered.map(p => <PersonCard key={p.id} person={p} />)}
          </div>
        )}
      </div>
    </div>
  );
}

export default ContactsPage;

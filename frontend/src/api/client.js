const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Health
  health: () => request('/health'),

  // Chat
  chat: (message, conversationId, history = []) =>
    request('/chat/', {
      method: 'POST',
      body: JSON.stringify({ message, conversation_id: conversationId, history }),
    }),

  // Models
  getModels: () => request('/models/'),
  getModel: (id) => request(`/models/${id}`),

  // Research
  getPapers: () => request('/research/papers'),
  getPaper: (id) => request(`/research/papers/${id}`),

  // GitHub
  getRepos: () => request('/github/repos'),
  getRepo: (id) => request(`/github/repos/${id}`),

  // Contacts
  getTeam: () => request('/contacts/team'),
  getPerson: (id) => request(`/contacts/team/${id}`),
  getOfficialContacts: () => request('/contacts/official'),
};

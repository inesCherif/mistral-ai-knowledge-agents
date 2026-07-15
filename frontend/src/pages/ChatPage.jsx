import React, { useState, useRef, useEffect } from 'react';
import { api } from '../api/client';

const SUGGESTIONS = [
  "What is Mistral 7B?",
  "Who founded Mistral AI?",
  "Show me Mistral research papers",
  "What GitHub repos does Mistral have?",
  "How do I contact the Mistral team?",
  "Compare Mistral models",
];

const AGENT_LABELS = {
  site_agent: { label: '🌐 Site', badge: 'site' },
  models_agent: { label: '🧠 Models', badge: 'models' },
  research_agent: { label: '📄 Research', badge: 'research' },
  github_agent: { label: '💻 GitHub', badge: 'github' },
  contact_agent: { label: '📬 Contacts', badge: 'contacts' },
};

function SourceChip({ source }) {
  const typeMap = {
    site: { icon: '🌐', cls: 'site' },
    paper: { icon: '📄', cls: 'paper' },
    github: { icon: '💻', cls: 'github' },
    contact: { icon: '👤', cls: 'contact' },
    model: { icon: '🧠', cls: 'model' },
  };
  const s = typeMap[source.type] || { icon: '🔗', cls: 'site' };
  return (
    <a
      href={source.url || '#'}
      target="_blank"
      rel="noopener noreferrer"
      className={`source-chip ${s.cls}`}
      title={source.excerpt || source.title}
    >
      {s.icon} {source.title}
    </a>
  );
}

function TypingIndicator() {
  return (
    <div className="chat-message assistant">
      <div className="message-avatar assistant">M</div>
      <div className="message-body">
        <div className="typing-indicator">
          <div className="typing-dot" />
          <div className="typing-dot" />
          <div className="typing-dot" />
        </div>
      </div>
    </div>
  );
}

function MessageBubble({ msg }) {
  const isUser = msg.role === 'user';
  const agentInfo = AGENT_LABELS[msg.agent_used] || {};

  // Format markdown-like content
  const formatContent = (text) => {
    if (!text) return '';
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br/>');
  };

  return (
    <div className={`chat-message ${isUser ? 'user' : 'assistant'}`}>
      <div className={`message-avatar ${isUser ? 'user' : 'assistant'}`}>
        {isUser ? 'U' : 'M'}
      </div>
      <div className="message-body">
        <div
          className={`message-bubble ${isUser ? 'user' : 'assistant'}`}
          dangerouslySetInnerHTML={{ __html: formatContent(msg.content) }}
        />
        {!isUser && (
          <>
            {msg.sources && msg.sources.length > 0 && (
              <div className="sources-list">
                {msg.sources.map((src, i) => <SourceChip key={i} source={src} />)}
              </div>
            )}
            <div className="message-meta">
              {agentInfo.label && (
                <span className={`header-badge badge-${agentInfo.badge}`}>
                  {agentInfo.label}
                </span>
              )}
              {msg.response_time_ms && (
                <span>{msg.response_time_ms}ms</span>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function WelcomeScreen({ onSuggest }) {
  const features = [
    { icon: '🧠', title: 'Models', desc: 'Mistral 7B, Mixtral, Large, Codestral…', q: 'What models does Mistral offer?' },
    { icon: '📄', title: 'Research', desc: 'Papers, benchmarks, arXiv', q: 'Show me Mistral research papers' },
    { icon: '💻', title: 'GitHub', desc: 'Repos, code, implementations', q: 'What GitHub repos does Mistral have?' },
    { icon: '📬', title: 'Contacts', desc: 'Team, LinkedIn, emails', q: 'Who are the founders of Mistral AI?' },
  ];

  return (
    <div className="welcome-screen">
      <div className="welcome-logo">🤖</div>
      <div>
        <div className="welcome-title">MistralBot</div>
        <div className="welcome-subtitle" style={{ marginTop: 8 }}>
          Your AI-powered knowledge base for everything about Mistral AI —
          models, research papers, GitHub repos, and team contacts.
        </div>
      </div>
      <div className="welcome-features">
        {features.map((f) => (
          <div key={f.title} className="welcome-feature" onClick={() => onSuggest(f.q)}>
            <div className="welcome-feature-icon">{f.icon}</div>
            <div className="welcome-feature-title">{f.title}</div>
            <div className="welcome-feature-desc">{f.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const bottomRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    const trimmed = (text || input).trim();
    if (!trimmed || loading) return;

    const userMsg = { role: 'user', content: trimmed };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.chat(trimmed, conversationId, messages);
      if (!conversationId) setConversationId(res.conversation_id);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.answer,
        sources: res.sources,
        agent_used: res.agent_used,
        intent: res.intent,
        response_time_ms: res.response_time_ms,
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ Error: ${err.message}. Make sure the backend is running on port 8000.`,
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const showWelcome = messages.length === 0 && !loading;

  return (
    <div className="chat-wrapper">
      <div className="page-header">
        <div>
          <div className="page-header-title">💬 Chat with MistralBot</div>
          <div className="page-header-subtitle">Ask anything about Mistral AI</div>
        </div>
      </div>

      <div className="chat-messages">
        {showWelcome ? (
          <WelcomeScreen onSuggest={(q) => sendMessage(q)} />
        ) : (
          <>
            {messages.map((msg, i) => <MessageBubble key={i} msg={msg} />)}
            {loading && <TypingIndicator />}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-area">
        {showWelcome && (
          <div className="chat-suggestions">
            {SUGGESTIONS.slice(0, 4).map((s) => (
              <button key={s} className="suggestion-chip" onClick={() => sendMessage(s)}>
                {s}
              </button>
            ))}
          </div>
        )}
        <div className="chat-input-row">
          <textarea
            ref={textareaRef}
            className="chat-input"
            placeholder="Ask about Mistral models, papers, GitHub, or team contacts…"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          <button
            className="chat-send-btn"
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
            title="Send message"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;

import React, { useState, useRef, useEffect } from 'react';

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1c1c28;
    --border: rgba(255,255,255,0.07);
    --border-hover: rgba(255,255,255,0.15);
    --accent: #c8f05a;
    --accent2: #5af0c8;
    --accent3: #f05ac8;
    --text: #f0f0f8;
    --text-muted: #666688;
    --text-dim: #44445a;
    --user-bg: linear-gradient(135deg, #1e2535 0%, #1a2040 100%);
    --ai-bg: linear-gradient(135deg, #1a1a25 0%, #171720 100%);
    --glow: rgba(200,240,90,0.15);
  }

  .nlp-app {
    font-family: 'Syne', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0;
    position: relative;
    overflow: hidden;
  }

  .nlp-app::before {
    content: '';
    position: fixed;
    top: -40%;
    left: -20%;
    width: 60%;
    height: 80%;
    background: radial-gradient(ellipse, rgba(200,240,90,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .nlp-app::after {
    content: '';
    position: fixed;
    bottom: -30%;
    right: -10%;
    width: 50%;
    height: 70%;
    background: radial-gradient(ellipse, rgba(90,240,200,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .header {
    width: 100%;
    max-width: 860px;
    padding: 28px 32px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    z-index: 1;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .logo-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
  }

  .logo-text {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text);
  }

  .logo-text span {
    color: var(--accent);
  }

  .badge {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 20px;
    border: 1px solid var(--border);
    color: var(--text-muted);
    letter-spacing: 0.05em;
  }

  .chat-container {
    width: 100%;
    max-width: 860px;
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 20px 32px 0;
    position: relative;
    z-index: 1;
  }

  .messages-area {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    min-height: 0;
    max-height: calc(100vh - 280px);
    scrollbar-width: thin;
    scrollbar-color: var(--surface2) transparent;
  }

  .messages-area::-webkit-scrollbar { width: 4px; }
  .messages-area::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 4px; }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 16px;
    min-height: 340px;
    animation: fadeUp 0.6s ease both;
  }

  .empty-icon {
    width: 64px;
    height: 64px;
    border-radius: 18px;
    background: var(--surface);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
  }

  .empty-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.3px;
  }

  .empty-sub {
    font-size: 14px;
    color: var(--text-muted);
    font-family: 'DM Mono', monospace;
    font-weight: 300;
  }

  .chips {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 8px;
  }

  .chip {
    padding: 8px 14px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface);
    font-size: 13px;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'DM Mono', monospace;
    font-weight: 300;
  }

  .chip:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(200,240,90,0.05);
  }

  .message {
    display: flex;
    gap: 12px;
    animation: fadeUp 0.3s ease both;
  }

  .message.user { flex-direction: row-reverse; }

  .avatar {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 700;
  }

  .avatar.user-av {
    background: linear-gradient(135deg, #2a3560, #3a4580);
    border: 1px solid rgba(90,130,255,0.3);
    color: #8aabff;
  }

  .avatar.ai-av {
    background: linear-gradient(135deg, #1e2830, #2a3820);
    border: 1px solid rgba(200,240,90,0.2);
    color: var(--accent);
    font-size: 16px;
  }

  .bubble-wrap { flex: 1; min-width: 0; max-width: 78%; }
  .message.user .bubble-wrap { display: flex; flex-direction: column; align-items: flex-end; }

  .bubble {
    padding: 14px 16px;
    border-radius: 14px;
    font-size: 14.5px;
    line-height: 1.6;
    border: 1px solid var(--border);
    position: relative;
    word-break: break-word;
  }

  .bubble.user-bubble {
    background: var(--user-bg);
    border-color: rgba(90,130,255,0.2);
    border-radius: 14px 4px 14px 14px;
  }

  .bubble.ai-bubble {
    background: var(--ai-bg);
    border-radius: 4px 14px 14px 14px;
  }

  .bubble-label {
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    font-weight: 400;
    color: var(--text-dim);
    margin-bottom: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }

  .answer-text {
    font-size: 15px;
    line-height: 1.65;
    color: var(--text);
  }

  .answer-label {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(200,240,90,0.1);
    border: 1px solid rgba(200,240,90,0.2);
    border-radius: 4px;
    padding: 2px 8px;
    margin-bottom: 8px;
  }

  .confidence-bar {
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .conf-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
  }

  .conf-track {
    flex: 1;
    height: 4px;
    background: var(--surface2);
    border-radius: 4px;
    overflow: hidden;
  }

  .conf-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent2), var(--accent));
    border-radius: 4px;
    transition: width 1s ease;
  }

  .conf-value {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--accent);
    min-width: 36px;
    text-align: right;
  }

  .no-answer {
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: var(--text-muted);
    font-style: italic;
  }

  .details-toggle {
    margin-top: 8px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-dim);
    cursor: pointer;
    border: none;
    background: none;
    padding: 4px 0;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: color 0.2s;
  }

  .details-toggle:hover { color: var(--text-muted); }

  .details-panel {
    margin-top: 6px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    overflow: hidden;
  }

  .details-panel pre {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--text-muted);
    white-space: pre-wrap;
    word-break: break-all;
    line-height: 1.6;
    max-height: 320px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--surface2) transparent;
  }

  .input-section {
    width: 100%;
    max-width: 860px;
    padding: 0 32px 28px;
    position: relative;
    z-index: 1;
  }

  .input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 14px 14px 12px;
    transition: border-color 0.25s, box-shadow 0.25s;
  }

  .input-card:focus-within {
    border-color: rgba(200,240,90,0.3);
    box-shadow: 0 0 0 3px rgba(200,240,90,0.05), 0 8px 32px rgba(0,0,0,0.3);
  }

  .file-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
  }

  .file-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface2);
    color: var(--text-muted);
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .file-btn:hover {
    border-color: var(--border-hover);
    color: var(--text);
  }

  .file-btn svg { flex-shrink: 0; }

  .file-name {
    flex: 1;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: var(--accent);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .file-clear {
    width: 22px;
    height: 22px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: none;
    color: var(--text-dim);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    transition: all 0.2s;
    flex-shrink: 0;
  }

  .file-clear:hover { color: var(--text); border-color: var(--border-hover); }

  .file-input-hidden { display: none; }

  .textarea-row {
    display: flex;
    gap: 10px;
    align-items: flex-end;
  }

  .chat-textarea {
    flex: 1;
    background: none;
    border: none;
    outline: none;
    color: var(--text);
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    resize: none;
    line-height: 1.55;
    min-height: 44px;
    max-height: 160px;
    padding: 4px 0;
    placeholder-color: var(--text-dim);
  }

  .chat-textarea::placeholder { color: var(--text-dim); }

  .send-btn {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    border: none;
    background: var(--accent);
    color: #0a0a0f;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    transition: all 0.2s;
    font-size: 18px;
  }

  .send-btn:hover:not(:disabled) {
    background: #d8ff6a;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(200,240,90,0.3);
  }

  .send-btn:disabled {
    background: var(--surface2);
    color: var(--text-dim);
    cursor: not-allowed;
  }

  .send-btn.loading {
    background: var(--surface2);
    color: var(--accent);
    animation: pulse 1.2s ease infinite;
  }

  .input-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
    padding: 0 2px;
  }

  .hint {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-dim);
  }

  .hint kbd {
    font-family: 'DM Mono', monospace;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 5px;
    font-size: 10px;
  }

  .typing-indicator {
    display: flex;
    gap: 12px;
    animation: fadeUp 0.3s ease both;
  }

  .typing-dots {
    display: flex;
    gap: 5px;
    align-items: center;
    padding: 14px 16px;
    background: var(--ai-bg);
    border: 1px solid var(--border);
    border-radius: 4px 14px 14px 14px;
  }

  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-dim);
    animation: dotBounce 1.2s ease infinite;
  }
  .dot:nth-child(2) { animation-delay: 0.2s; }
  .dot:nth-child(3) { animation-delay: 0.4s; }

  @keyframes dotBounce {
    0%, 60%, 100% { transform: translateY(0); background: var(--text-dim); }
    30% { transform: translateY(-5px); background: var(--accent); }
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;

function renderAssistantMessage(data) {
  if (data && typeof data.answer === 'string' && data.answer.trim().length > 0) {
    return { type: 'answer', answer: data.answer, confidence: data.confidence };
  }
  return { type: 'none' };
}

const SUGGESTIONS = [
  'What is the main topic?',
  'Summarize this text.',
  'Extract all entities.',
  'What are the key verbs?',
];

export default function ChatUi() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [openDetails, setOpenDetails] = useState({});
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const autoResize = () => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = 'auto';
    ta.style.height = Math.min(ta.scrollHeight, 160) + 'px';
  };

  const sendMessage = async () => {
    const text = input.trim();
    if ((!text && !file) || loading) return;

    const userLabel = file
      ? `${text ? text + '\n\n' : ''}📎 ${file.name}`
      : text;

    setMessages(m => [...m, { role: 'user', text: userLabel }]);
    setInput('');
    setFile(null);
    if (textareaRef.current) textareaRef.current.style.height = 'auto';
    setLoading(true);

    try {
      const features = { tokens: true, pos: true, entities: true, lemmas: true, dependencies: true, answer: true };
      let res;
      if (file) {
        const form = new FormData();
        form.append('file', file);
        if (text) form.append('question', text);
        form.append('features', JSON.stringify(features));
        res = await fetch('http://localhost:3000/api/analyze', { method: 'POST', body: form });
      } else {
        const payload = { text, question: text, features };
        res = await fetch('http://localhost:3000/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
      }
      if (!res.ok) {
        const t = await res.text();
        throw new Error(`HTTP ${res.status}: ${t}`);
      }
      const data = await res.json();
      const parsed = renderAssistantMessage(data);
      setMessages(m => [...m, { role: 'assistant', parsed, raw: data }]);
    } catch (e) {
      setMessages(m => [...m, { role: 'assistant', parsed: { type: 'error', message: e.message }, raw: null }]);
    } finally {
      setLoading(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const toggleDetails = (idx) => setOpenDetails(p => ({ ...p, [idx]: !p[idx] }));

  const confidencePct = (conf) => {
    if (typeof conf === 'number') return Math.round(conf * 100);
    if (typeof conf === 'string') return Math.round(parseFloat(conf) * 100);
    return null;
  };

  return (
    <>
      <style>{styles}</style>
      <div className="nlp-app">
        {/* Header */}
        <div className="header">
          <div className="logo">
            <div className="logo-icon">🧠</div>
            <div className="logo-text">NLP<span>Lens</span></div>
          </div>
          <div className="badge">v1.0 · analysis engine</div>
        </div>

        {/* Chat area */}
        <div className="chat-container">
          <div className="messages-area">
            {messages.length === 0 && !loading ? (
              <div className="empty-state">
                <div className="empty-icon">✦</div>
                <div className="empty-title">Analyze any text or document</div>
                <div className="empty-sub">Entities · POS · Lemmas · Dependencies · QA</div>
                <div className="chips">
                  {SUGGESTIONS.map(s => (
                    <button key={s} className="chip" onClick={() => { setInput(s); textareaRef.current?.focus(); }}>
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            ) : null}

            {messages.map((m, idx) => (
              <div key={idx} className={`message ${m.role}`}>
                <div className={`avatar ${m.role === 'user' ? 'user-av' : 'ai-av'}`}>
                  {m.role === 'user' ? 'U' : '✦'}
                </div>
                <div className="bubble-wrap">
                  <div className="bubble-label">{m.role === 'user' ? 'You' : 'Analysis'}</div>
                  <div className={`bubble ${m.role === 'user' ? 'user-bubble' : 'ai-bubble'}`}>
                    {m.role === 'user' ? (
                      <div style={{ whiteSpace: 'pre-wrap' }}>{m.text}</div>
                    ) : m.parsed?.type === 'answer' ? (
                      <>
                        <div className="answer-label">Answer</div>
                        <div className="answer-text">{m.parsed.answer}</div>
                        {m.parsed.confidence !== undefined && (() => {
                          const pct = confidencePct(m.parsed.confidence);
                          return pct !== null ? (
                            <div className="confidence-bar">
                              <span className="conf-label">confidence</span>
                              <div className="conf-track">
                                <div className="conf-fill" style={{ width: `${pct}%` }} />
                              </div>
                              <span className="conf-value">{pct}%</span>
                            </div>
                          ) : null;
                        })()}
                      </>
                    ) : m.parsed?.type === 'error' ? (
                      <div style={{ fontFamily: "'DM Mono', monospace", fontSize: 13, color: '#f05a5a' }}>
                        ⚠ {m.parsed.message}
                      </div>
                    ) : (
                      <div className="no-answer">No direct answer found. See full analysis below.</div>
                    )}
                  </div>
                  {m.raw && (
                    <>
                      <button className="details-toggle" onClick={() => toggleDetails(idx)}>
                        <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
                          <path d={openDetails[idx] ? 'M2 7l3-3 3 3' : 'M2 3l3 3 3-3'} stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                        </svg>
                        {openDetails[idx] ? 'Hide' : 'View'} raw analysis
                      </button>
                      {openDetails[idx] && (
                        <div className="details-panel">
                          <pre>{JSON.stringify(m.raw, null, 2)}</pre>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="typing-indicator">
                <div className="avatar ai-av">✦</div>
                <div>
                  <div className="bubble-label">Analysis</div>
                  <div className="typing-dots">
                    <div className="dot" /><div className="dot" /><div className="dot" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input */}
        <div className="input-section">
          <div className="input-card">
            {file && (
              <div className="file-row">
                <span style={{ fontSize: 14 }}>📎</span>
                <span className="file-name">{file.name}</span>
                <button className="file-clear" onClick={() => setFile(null)}>×</button>
              </div>
            )}
            <div className="textarea-row">
              <textarea
                ref={textareaRef}
                className="chat-textarea"
                value={input}
                onChange={e => { setInput(e.target.value); autoResize(); }}
                onKeyDown={onKeyDown}
                placeholder={file ? 'Ask a question about this file...' : 'Ask a question or paste text to analyze...'}
                rows={1}
              />
              <button
                className={`send-btn${loading ? ' loading' : ''}`}
                onClick={sendMessage}
                disabled={loading || (!input.trim() && !file)}
                title="Send"
              >
                {loading ? (
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="2" strokeDasharray="20" strokeDashoffset="0">
                      <animateTransform attributeName="transform" type="rotate" from="0 8 8" to="360 8 8" dur="0.8s" repeatCount="indefinite"/>
                    </circle>
                  </svg>
                ) : (
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M2 8h12M8 2l6 6-6 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
            </div>
          </div>
          <div className="input-footer">
            <span className="hint"><kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for new line</span>
            <button
              className="file-btn"
              onClick={() => fileInputRef.current?.click()}
            >
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <rect x="1" y="1" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.2"/>
                <path d="M4 6h4M6 4v4" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
              </svg>
              Attach PDF or TXT
            </button>
            <input
              ref={fileInputRef}
              className="file-input-hidden"
              type="file"
              accept=".pdf,.txt"
              onChange={e => setFile(e.target.files[0] || null)}
            />
          </div>
        </div>
      </div>
    </>
  );
}
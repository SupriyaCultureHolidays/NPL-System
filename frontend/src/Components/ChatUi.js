import React, { useState } from 'react';

function ChatUi() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setMessages(m => [...m, { role: 'user', text }]);
    setInput('');
    setLoading(true);
    try {
      const payload = {
        text,
        question: text,
        features: {
          tokens: true,
          pos: true,
          entities: true,
          lemmas: true,
          dependencies: true,
          answer: true
        }
      };
      const res = await fetch('http://localhost:3000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text}`);
      }
      const data = await res.json();
      const assistantMsg = data.answer
        ? `Answer: ${data.answer} (confidence ${data.confidence ?? ''})`
        : 'Analysis completed';
      setMessages(m => [...m, { role: 'assistant', text: assistantMsg, raw: data }]);
    } catch (e) {
      setMessages(m => [...m, { role: 'assistant', text: `Error: ${e.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', textAlign: 'left' }}>
      <div style={{ border: '1px solid #ddd', borderRadius: 8, padding: 16, minHeight: 300, background: '#fafafa' }}>
        {messages.map((m, idx) => (
          <div key={idx} style={{ marginBottom: 12 }}>
            <div style={{ fontWeight: 600 }}>{m.role === 'user' ? 'You' : 'Assistant'}</div>
            <div>{m.text}</div>
            {m.raw && (
              <details style={{ marginTop: 6 }}>
                <summary>Details</summary>
                <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>{JSON.stringify(m.raw, null, 2)}</pre>
              </details>
            )}
          </div>
        ))}
        {messages.length === 0 && <div style={{ color: '#666' }}>Start by typing a message below.</div>}
      </div>
      <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Ask a question or paste text..."
          rows={3}
          style={{ flex: 1, padding: 8, borderRadius: 6, border: '1px solid #ccc' }}
        />
        <button onClick={sendMessage} disabled={loading} style={{ padding: '0 16px', borderRadius: 6 }}>
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
      <FileUpload setMessages={setMessages} />
    </div>
  );
}

export default ChatUi;

function FileUpload({ setMessages }) {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);

  const onUpload = async () => {
    if (!file || loading) return;
    setMessages(m => [...m, { role: 'user', text: `Uploaded: ${file.name}${question ? ` | Q: ${question}` : ''}` }]);
    setLoading(true);
    try {
      const form = new FormData();
      form.append('file', file);
      if (question) form.append('question', question);
      form.append('features', JSON.stringify({
        tokens: true,
        pos: true,
        entities: true,
        lemmas: true,
        dependencies: true,
        answer: true
      }));
      const res = await fetch('http://localhost:3000/api/analyze', {
        method: 'POST',
        body: form
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`HTTP ${res.status}: ${text}`);
      }
      const data = await res.json();
      const assistantMsg = data.answer
        ? `Answer: ${data.answer} (confidence ${data.confidence ?? ''})`
        : 'Analysis completed';
      setMessages(m => [...m, { role: 'assistant', text: assistantMsg, raw: data }]);
    } catch (e) {
      setMessages(m => [...m, { role: 'assistant', text: `Error: ${e.message}` }]);
    } finally {
      setLoading(false);
      setFile(null);
      setQuestion('');
    }
  };

  return (
    <div style={{ marginTop: 16, borderTop: '1px solid #eee', paddingTop: 12 }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Upload PDF/TXT</div>
      <div style={{ display: 'flex', gap: 8 }}>
        <input type="file" accept=".pdf,.txt" onChange={(e) => setFile(e.target.files[0] || null)} />
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Optional question"
          style={{ flex: 1, padding: 8, borderRadius: 6, border: '1px solid #ccc' }}
        />
        <button onClick={onUpload} disabled={loading || !file} style={{ padding: '0 16px', borderRadius: 6 }}>
          {loading ? 'Uploading...' : 'Submit'}
        </button>
      </div>
    </div>
  );
}

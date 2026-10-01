import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./style.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [text, setText] = useState("");
  const [language, setLanguage] = useState("en");
  const [speed, setSpeed] = useState(1);
  const [audioUrl, setAudioUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  async function generate() {
    if (!text.trim()) return;
    setBusy(true);
    setMessage("");
    setAudioUrl("");

    try {
      const response = await fetch(API + "/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, language, speed })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Generation failed");
      setAudioUrl(data.audio_url);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="shell">
      <section className="hero">
        <div className="brand">GOSPEL <span>AI</span></div>
        <h1>Your Voice. Your Message. Your Impact.</h1>
        <p>Personal AI voice studio for creating narrated gospel messages and media.</p>
      </section>

      <section className="card">
        <label htmlFor="message">Personal Message</label>
        <textarea
          id="message"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Write your message here..."
          rows={10}
        />

        <div className="controls">
          <label>
            Language
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
              <option value="en">English</option>
              <option value="fr">Français</option>
            </select>
          </label>

          <label>
            Speed: {speed.toFixed(1)}x
            <input
              type="range"
              min="0.7"
              max="1.3"
              step="0.1"
              value={speed}
              onChange={(e) => setSpeed(Number(e.target.value))}
            />
          </label>
        </div>

        <button disabled={busy || !text.trim()} onClick={generate}>
          {busy ? "Preparing..." : "Generate My Voice"}
        </button>

        {message && <div className="notice">{message}</div>}

        {audioUrl && (
          <div className="result">
            <strong>Generated audio</strong>
            <audio controls src={audioUrl} />
            <a href={audioUrl} download>Download audio</a>
          </div>
        )}
      </section>

      <footer>GOSPEL AI · Self-hosted voice technology</footer>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
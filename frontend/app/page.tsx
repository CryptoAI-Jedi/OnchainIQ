"use client";

import { useState } from "react";

// Mirror the backend's AskResponse shape. This is the frontend's half of the
// contract; keep it in sync with the Pydantic model and both sides agree.
type AskResponse = {
  answer: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk() {
    setLoading(true);
    setError("");
    setAnswer("");
    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      if (!res.ok) {
        throw new Error(`API error: ${res.status}`);
      }
      const data: AskResponse = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 640, margin: "4rem auto", padding: "0 1rem", fontFamily: "system-ui" }}>
      <h1>OnchainIQ</h1>
      <p>Ask a question about onchain or Bitcoin-mining activity.</p>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="e.g. What were the largest miner outflows this week?"
        rows={3}
        style={{ width: "100%", padding: "0.5rem", fontSize: "1rem" }}
      />

      <button
        onClick={handleAsk}
        disabled={loading || question.trim() === ""}
        style={{ marginTop: "0.5rem", padding: "0.5rem 1rem", fontSize: "1rem" }}
      >
        {loading ? "Asking..." : "Ask"}
      </button>

      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {answer && (
        <div style={{ marginTop: "1.5rem", padding: "1rem", background: "#f4f4f5", borderRadius: 8 }}>
          {answer}
        </div>
      )}
    </main>
  );
}
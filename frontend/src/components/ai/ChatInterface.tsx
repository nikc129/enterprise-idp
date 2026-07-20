"use client";
import { useState } from "react";
import { fetchAPI } from "@/lib/api";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const result = await fetchAPI("/api/ai/provision", {
        method: "POST",
        body: JSON.stringify({ query: userMsg }),
      });
      const reply = `**Intent:** ${result.intent}\n\n**Resource Type:** ${result.resource_type}\n\n**Parameters:**\n\`\`\`json\n${JSON.stringify(result.parameters, null, 2)}\n\`\`\`\n\n**Plan:** ${result.plan}`;
      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Error: Could not process request." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px]">
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-lg">Ask me to provision infrastructure</p>
            <p className="text-sm mt-2">Try: "Create an EC2 instance for my web app"</p>
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`p-3 rounded-lg max-w-[80%] ${
            m.role === "user" ? "bg-blue-100 ml-auto" : "bg-gray-100"
          }`}>
            <pre className="whitespace-pre-wrap text-sm">{m.content}</pre>
          </div>
        ))}
        {loading && <div className="text-gray-400 text-sm">Thinking...</div>}
      </div>
      <div className="border-t p-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
          placeholder="Describe what you want to provision..."
          className="flex-1 px-4 py-2 border rounded-lg"
        />
        <button
          onClick={send}
          disabled={loading}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}

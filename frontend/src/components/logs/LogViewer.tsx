"use client";
import { useState } from "react";

export default function LogViewer({ logs, title }: { logs: string; title: string }) {
  const [filter, setFilter] = useState("");

  const filtered = filter
    ? logs.split("\n").filter((l) => l.toLowerCase().includes(filter.toLowerCase())).join("\n")
    : logs;

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold">{title}</h3>
        <input
          type="text"
          placeholder="Filter logs..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="px-3 py-1 border rounded text-sm"
        />
      </div>
      <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-auto max-h-[600px] text-sm font-mono whitespace-pre-wrap">
        {filtered || "No logs available."}
      </pre>
    </div>
  );
}

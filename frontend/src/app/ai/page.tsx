"use client";
import ChatInterface from "@/components/ai/ChatInterface";

export default function AIPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">AI Assistant</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <ChatInterface />
      </div>
    </div>
  );
}

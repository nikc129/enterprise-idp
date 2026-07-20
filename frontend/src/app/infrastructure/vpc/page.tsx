"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";

export default function CreateVPCPage() {
  const router = useRouter();
  const [form, setForm] = useState({ vpc_name: "", cidr_block: "10.0.0.0/16" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await fetchAPI("/api/infrastructure/vpc", { method: "POST", body: JSON.stringify(form) });
      router.push("/infrastructure");
    } catch (err: any) { setError(err.message); }
    setLoading(false);
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">Create VPC</h1>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">VPC Name</label>
          <input type="text" value={form.vpc_name} onChange={(e) => setForm({...form, vpc_name: e.target.value})} className="w-full px-3 py-2 border rounded" required />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">CIDR Block</label>
          <input type="text" value={form.cidr_block} onChange={(e) => setForm({...form, cidr_block: e.target.value})} className="w-full px-3 py-2 border rounded" />
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50">
          {loading ? "Creating..." : "Create VPC"}
        </button>
      </form>
    </div>
  );
}

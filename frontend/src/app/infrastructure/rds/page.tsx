"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";

export default function CreateRDSPage() {
  const router = useRouter();
  const [form, setForm] = useState({ db_name: "", instance_class: "db.t3.micro", engine: "postgres", engine_version: "16.4", allocated_storage: 20, username: "admin", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await fetchAPI("/api/infrastructure/rds", { method: "POST", body: JSON.stringify(form) });
      router.push("/infrastructure");
    } catch (err: any) { setError(err.message); }
    setLoading(false);
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">Create RDS Database</h1>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Database Name</label>
          <input type="text" value={form.db_name} onChange={(e) => setForm({...form, db_name: e.target.value})} className="w-full px-3 py-2 border rounded" required />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Instance Class</label>
          <select value={form.instance_class} onChange={(e) => setForm({...form, instance_class: e.target.value})} className="w-full px-3 py-2 border rounded">
            <option value="db.t3.micro">db.t3.micro</option>
            <option value="db.t3.small">db.t3.small</option>
            <option value="db.t3.medium">db.t3.medium</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Engine Version</label>
          <input type="text" value={form.engine_version} onChange={(e) => setForm({...form, engine_version: e.target.value})} className="w-full px-3 py-2 border rounded" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Storage (GB)</label>
          <input type="number" value={form.allocated_storage} onChange={(e) => setForm({...form, allocated_storage: parseInt(e.target.value)})} className="w-full px-3 py-2 border rounded" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Username</label>
          <input type="text" value={form.username} onChange={(e) => setForm({...form, username: e.target.value})} className="w-full px-3 py-2 border rounded" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Password</label>
          <input type="password" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} className="w-full px-3 py-2 border rounded" required />
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-orange-600 text-white rounded hover:bg-orange-700 disabled:opacity-50">
          {loading ? "Creating..." : "Create RDS Database"}
        </button>
      </form>
    </div>
  );
}

"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";

export default function CreateS3Page() {
  const router = useRouter();
  const [form, setForm] = useState({ bucket_name: "", versioning: true, encryption: true });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await fetchAPI("/api/infrastructure/s3", { method: "POST", body: JSON.stringify(form) });
      router.push("/infrastructure");
    } catch (err: any) { setError(err.message); }
    setLoading(false);
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">Create S3 Bucket</h1>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Bucket Name</label>
          <input type="text" value={form.bucket_name} onChange={(e) => setForm({...form, bucket_name: e.target.value})} className="w-full px-3 py-2 border rounded" required />
        </div>
        <div className="flex items-center gap-6">
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={form.versioning} onChange={(e) => setForm({...form, versioning: e.target.checked})} />
            <span className="text-sm">Versioning</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={form.encryption} onChange={(e) => setForm({...form, encryption: e.target.checked})} />
            <span className="text-sm">Encryption</span>
          </label>
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50">
          {loading ? "Creating..." : "Create S3 Bucket"}
        </button>
      </form>
    </div>
  );
}

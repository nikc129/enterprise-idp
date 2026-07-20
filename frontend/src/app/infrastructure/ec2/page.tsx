"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";

export default function CreateEC2Page() {
  const router = useRouter();
  const [form, setForm] = useState({ instance_name: "", instance_type: "t3.micro", subnet_id: "", key_name: "idp", ami_id: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await fetchAPI("/api/infrastructure/ec2", { method: "POST", body: JSON.stringify(form) });
      router.push("/infrastructure");
    } catch (err: any) { setError(err.message); }
    setLoading(false);
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">Create EC2 Instance</h1>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Instance Name</label>
          <input type="text" value={form.instance_name} onChange={(e) => setForm({...form, instance_name: e.target.value})} className="w-full px-3 py-2 border rounded" required />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Instance Type</label>
          <select value={form.instance_type} onChange={(e) => setForm({...form, instance_type: e.target.value})} className="w-full px-3 py-2 border rounded">
            <option value="t3.micro">t3.micro</option>
            <option value="t3.small">t3.small</option>
            <option value="t3.medium">t3.medium</option>
            <option value="t3.large">t3.large</option>
            <option value="t3.xlarge">t3.xlarge</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Subnet ID (optional)</label>
          <input type="text" value={form.subnet_id} onChange={(e) => setForm({...form, subnet_id: e.target.value})} className="w-full px-3 py-2 border rounded" placeholder="Leave empty for default" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Key Name</label>
          <input type="text" value={form.key_name} onChange={(e) => setForm({...form, key_name: e.target.value})} className="w-full px-3 py-2 border rounded" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">AMI ID (optional)</label>
          <input type="text" value={form.ami_id} onChange={(e) => setForm({...form, ami_id: e.target.value})} className="w-full px-3 py-2 border rounded" placeholder="Leave empty for default Ubuntu AMI" />
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {loading ? "Creating..." : "Create EC2 Instance"}
        </button>
      </form>
    </div>
  );
}

"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { fetchAPI } from "@/lib/api";
import { Resource, Repo, Branch } from "@/types";

export default function NewDeploymentPage() {
  const router = useRouter();
  const [ec2Instances, setEc2Instances] = useState<Resource[]>([]);
  const [repos, setRepos] = useState<Repo[]>([]);
  const [branches, setBranches] = useState<Branch[]>([]);
  const [form, setForm] = useState({ resource_id: 0, github_repo: "", github_branch: "", docker_image: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAPI("/api/infrastructure/ec2").then((d) => setEc2Instances(d.resources || [])).catch(() => {});
    fetchAPI("/api/deployment/repos/list").then((d) => setRepos(d || [])).catch(() => {});
  }, []);

  const loadBranches = async (repo: string) => {
    try {
      const data = await fetchAPI(`/api/deployment/repos/${encodeURIComponent(repo)}/branches`);
      setBranches(data || []);
    } catch { setBranches([]); }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await fetchAPI("/api/deployment/", { method: "POST", body: JSON.stringify(form) });
      router.push("/deployment");
    } catch (err: any) { setError(err.message); }
    setLoading(false);
  };

  return (
    <div className="max-w-lg">
      <h1 className="text-2xl font-bold mb-6">New Deployment</h1>
      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Target EC2 Instance</label>
          <select value={form.resource_id} onChange={(e) => setForm({...form, resource_id: parseInt(e.target.value)})} className="w-full px-3 py-2 border rounded" required>
            <option value={0}>Select instance...</option>
            {ec2Instances.map((i) => <option key={i.id} value={i.id}>{i.name} ({i.cloud_id})</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Repository</label>
          <select value={form.github_repo} onChange={(e) => { setForm({...form, github_repo: e.target.value}); loadBranches(e.target.value); }} className="w-full px-3 py-2 border rounded" required>
            <option value="">Select repository...</option>
            {repos.map((r) => <option key={r.full_name} value={r.full_name}>{r.full_name}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Branch</label>
          <select value={form.github_branch} onChange={(e) => setForm({...form, github_branch: e.target.value})} className="w-full px-3 py-2 border rounded" required>
            <option value="">Select branch...</option>
            {branches.map((b) => <option key={b.name} value={b.name}>{b.name}</option>)}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Docker Image</label>
          <input type="text" value={form.docker_image} onChange={(e) => setForm({...form, docker_image: e.target.value})} className="w-full px-3 py-2 border rounded" placeholder="e.g., ghcr.io/org/app" required />
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
          {loading ? "Deploying..." : "Start Deployment"}
        </button>
      </form>
    </div>
  );
}

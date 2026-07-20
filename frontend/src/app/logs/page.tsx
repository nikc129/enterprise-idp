"use client";
import { useState, useEffect } from "react";
import { fetchAPI } from "@/lib/api";
import LogViewer from "@/components/logs/LogViewer";
import { Resource, Deployment } from "@/types";

export default function LogsPage() {
  const [activeTab, setActiveTab] = useState<"terraform" | "deployment" | "docker">("terraform");
  const [resources, setResources] = useState<Resource[]>([]);
  const [deployments, setDeployments] = useState<Deployment[]>([]);
  const [selectedResource, setSelectedResource] = useState(0);
  const [selectedDeployment, setSelectedDeployment] = useState(0);
  const [logs, setLogs] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAPI("/api/infrastructure/").then((d) => setResources(d.resources || [])).catch(() => {});
    fetchAPI("/api/deployment/").then((d) => setDeployments(d.deployments || [])).catch(() => {});
  }, []);

  const loadTerraformLogs = async (id: number) => {
    setLoading(true);
    try {
      const d = await fetchAPI(`/api/logs/terraform/${id}`);
      setLogs(d.logs || "");
    } catch { setLogs("Error loading logs"); }
    setLoading(false);
  };

  const loadDeploymentLogs = async (id: number) => {
    setLoading(true);
    try {
      const d = await fetchAPI(`/api/logs/deployment/${id}`);
      setLogs(d.logs || "");
    } catch { setLogs("Error loading logs"); }
    setLoading(false);
  };

  const loadDockerLogs = async () => {
    setLoading(true);
    try {
      const d = await fetchAPI("/api/logs/docker/any");
      setLogs(typeof d.logs === "string" ? d.logs : JSON.stringify(d.logs, null, 2));
    } catch { setLogs("Error loading logs"); }
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Logs</h1>

      <div className="flex gap-2 mb-6">
        {(["terraform", "deployment", "docker"] as const).map((tab) => (
          <button key={tab} onClick={() => { setActiveTab(tab); setLogs(""); }}
            className={`px-4 py-2 rounded text-sm ${activeTab === tab ? "bg-blue-600 text-white" : "bg-gray-200"}`}>
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {activeTab === "terraform" && (
        <div className="bg-white rounded-lg shadow p-6">
          <select value={selectedResource} onChange={(e) => { const v = parseInt(e.target.value); setSelectedResource(v); if (v) loadTerraformLogs(v); }} className="px-3 py-2 border rounded mb-4">
            <option value={0}>Select resource...</option>
            {resources.map((r) => <option key={r.id} value={r.id}>{r.resource_type} - {r.name}</option>)}
          </select>
          {loading ? <p>Loading...</p> : <LogViewer logs={logs} title="Terraform Logs" />}
        </div>
      )}

      {activeTab === "deployment" && (
        <div className="bg-white rounded-lg shadow p-6">
          <select value={selectedDeployment} onChange={(e) => { const v = parseInt(e.target.value); setSelectedDeployment(v); if (v) loadDeploymentLogs(v); }} className="px-3 py-2 border rounded mb-4">
            <option value={0}>Select deployment...</option>
            {deployments.map((d) => <option key={d.id} value={d.id}>#{d.id} - {d.github_repo}</option>)}
          </select>
          {loading ? <p>Loading...</p> : <LogViewer logs={logs} title="Deployment Logs" />}
        </div>
      )}

      {activeTab === "docker" && (
        <div className="bg-white rounded-lg shadow p-6">
          <button onClick={loadDockerLogs} className="px-4 py-2 bg-blue-600 text-white rounded text-sm mb-4">Load Docker Logs</button>
          {loading ? <p>Loading...</p> : <LogViewer logs={logs} title="Docker Logs" />}
        </div>
      )}
    </div>
  );
}

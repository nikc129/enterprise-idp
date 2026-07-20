"use client";
import { useState, useEffect } from "react";
import { fetchAPI } from "@/lib/api";
import StatusCard from "@/components/monitoring/StatusCard";
import { Resource, ContainerInfo } from "@/types";

export default function MonitoringPage() {
  const [instances, setInstances] = useState<Resource[]>([]);
  const [containers, setContainers] = useState<ContainerInfo[]>([]);
  const [metrics, setMetrics] = useState<Record<string, any>>({});
  const [selectedInstance, setSelectedInstance] = useState("");

  useEffect(() => {
    fetchAPI("/api/infrastructure/ec2").then((d) => {
      const list = d.resources || [];
      setInstances(list);
      if (list.length > 0) setSelectedInstance(list[0].cloud_id);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedInstance) {
      fetchAPI(`/api/monitoring/${selectedInstance}/metrics`).then((d) => setMetrics(d)).catch(() => {});
    }
  }, [selectedInstance]);

  useEffect(() => {
    fetchAPI("/api/monitoring/any/containers").then((d) => setContainers(d || [])).catch(() => {});
  }, []);

  const cpuAvg = metrics.cpu?.length ? (metrics.cpu.reduce((s: number, m: any) => s + m.value, 0) / metrics.cpu.length).toFixed(1) : "-";
  const memAvg = metrics.memory?.length ? (metrics.memory.reduce((s: number, m: any) => s + m.value, 0) / metrics.memory.length).toFixed(1) : "-";

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Monitoring</h1>

      <div className="mb-6">
        <label className="text-sm font-medium mr-2">Select Instance:</label>
        <select value={selectedInstance} onChange={(e) => setSelectedInstance(e.target.value)} className="px-3 py-2 border rounded">
          {instances.map((i) => <option key={i.id} value={i.cloud_id}>{i.name} ({i.cloud_id})</option>)}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <StatusCard title="Avg CPU" value={`${cpuAvg}%`} icon="🖥️" color="blue" />
        <StatusCard title="Avg Memory" value={`${memAvg}%`} icon="💾" color="green" />
        <StatusCard title="Containers" value={containers.length} icon="🐳" color="purple" />
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Docker Containers</h2>
        {containers.length === 0 ? (
          <p className="text-gray-500">No containers found.</p>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="text-left text-sm text-gray-500 border-b">
                <th className="pb-2">Name</th>
                <th className="pb-2">Status</th>
                <th className="pb-2">Image</th>
                <th className="pb-2">Ports</th>
              </tr>
            </thead>
            <tbody>
              {containers.map((c) => (
                <tr key={c.id} className="border-b">
                  <td className="py-2 font-medium">{c.name}</td>
                  <td className="py-2">
                    <span className={`px-2 py-1 rounded text-xs ${
                      c.status === "running" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                    }`}>{c.status}</span>
                  </td>
                  <td className="py-2 text-sm font-mono">{c.image}</td>
                  <td className="py-2 text-sm">{c.ports || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

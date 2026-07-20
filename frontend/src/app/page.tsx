"use client";
import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import StatusCard from "@/components/monitoring/StatusCard";

export default function Dashboard() {
  const [resources, setResources] = useState<any[]>([]);
  const [deployments, setDeployments] = useState<any[]>([]);

  useEffect(() => {
    fetchAPI("/api/infrastructure/")
      .then((d) => setResources(d.resources || []))
      .catch(() => {});
    fetchAPI("/api/deployment/")
      .then((d) => setDeployments(d.deployments || []))
      .catch(() => {});
  }, []);

  const ec2Count = resources.filter((r) => r.resource_type === "ec2").length;
  const s3Count = resources.filter((r) => r.resource_type === "s3").length;
  const vpcCount = resources.filter((r) => r.resource_type === "vpc").length;
  const rdsCount = resources.filter((r) => r.resource_type === "rds").length;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatusCard title="EC2 Instances" value={ec2Count} icon="🖥️" color="blue" />
        <StatusCard title="S3 Buckets" value={s3Count} icon="📦" color="green" />
        <StatusCard title="VPCs" value={vpcCount} icon="🌐" color="purple" />
        <StatusCard title="RDS Databases" value={rdsCount} icon="🗄️" color="orange" />
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Recent Deployments</h2>
        {deployments.length === 0 ? (
          <p className="text-gray-500">No deployments yet.</p>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="text-left text-sm text-gray-500">
                <th className="pb-2">Repository</th>
                <th className="pb-2">Branch</th>
                <th className="pb-2">Status</th>
                <th className="pb-2">Created</th>
              </tr>
            </thead>
            <tbody>
              {deployments.slice(0, 5).map((d) => (
                <tr key={d.id} className="border-t">
                  <td className="py-2">{d.github_repo}</td>
                  <td className="py-2">{d.github_branch}</td>
                  <td className="py-2">
                    <span className={`px-2 py-1 rounded text-xs ${
                      d.status === "running" ? "bg-green-100 text-green-800" :
                      d.status === "failed" ? "bg-red-100 text-red-800" :
                      "bg-yellow-100 text-yellow-800"
                    }`}>
                      {d.status}
                    </span>
                  </td>
                  <td className="py-2 text-gray-500">{new Date(d.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

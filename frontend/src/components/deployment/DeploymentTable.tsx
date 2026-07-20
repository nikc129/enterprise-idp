"use client";
import { Deployment } from "@/types";

export default function DeploymentTable({ deployments }: { deployments: Deployment[] }) {
  if (deployments.length === 0) {
    return <p className="text-gray-500">No deployments found.</p>;
  }

  return (
    <table className="w-full">
      <thead>
        <tr className="text-left text-sm text-gray-500 border-b">
          <th className="pb-2">ID</th>
          <th className="pb-2">Repository</th>
          <th className="pb-2">Branch</th>
          <th className="pb-2">Image</th>
          <th className="pb-2">Status</th>
          <th className="pb-2">Created</th>
        </tr>
      </thead>
      <tbody>
        {deployments.map((d) => (
          <tr key={d.id} className="border-b hover:bg-gray-50">
            <td className="py-3">{d.id}</td>
            <td className="py-3 font-medium">{d.github_repo}</td>
            <td className="py-3">
              <span className="px-2 py-1 bg-gray-100 rounded text-xs">{d.github_branch}</span>
            </td>
            <td className="py-3 text-sm font-mono text-gray-600">{d.docker_image || "-"}</td>
            <td className="py-3">
              <span className={`px-2 py-1 rounded text-xs ${
                d.status === "running" ? "bg-green-100 text-green-800" :
                d.status === "failed" ? "bg-red-100 text-red-800" :
                d.status === "building" ? "bg-blue-100 text-blue-800" :
                "bg-yellow-100 text-yellow-800"
              }`}>
                {d.status}
              </span>
            </td>
            <td className="py-3 text-sm text-gray-500">
              {new Date(d.created_at).toLocaleDateString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

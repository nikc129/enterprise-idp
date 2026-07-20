"use client";
import { Resource } from "@/types";

export default function ResourceTable({
  resources,
  onDelete,
}: {
  resources: Resource[];
  onDelete: (id: number) => void;
}) {
  if (resources.length === 0) {
    return <p className="text-gray-500">No resources found.</p>;
  }

  return (
    <table className="w-full">
      <thead>
        <tr className="text-left text-sm text-gray-500 border-b">
          <th className="pb-2">Type</th>
          <th className="pb-2">Name</th>
          <th className="pb-2">Cloud ID</th>
          <th className="pb-2">Status</th>
          <th className="pb-2">Region</th>
          <th className="pb-2">Created</th>
          <th className="pb-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        {resources.map((r) => (
          <tr key={r.id} className="border-b hover:bg-gray-50">
            <td className="py-3">
              <span className="px-2 py-1 bg-gray-100 rounded text-xs font-mono">
                {r.resource_type}
              </span>
            </td>
            <td className="py-3 font-medium">{r.name}</td>
            <td className="py-3 text-sm text-gray-600 font-mono">{r.cloud_id || "-"}</td>
            <td className="py-3">
              <span className={`px-2 py-1 rounded text-xs ${
                r.status === "active" ? "bg-green-100 text-green-800" :
                r.status === "failed" ? "bg-red-100 text-red-800" :
                r.status === "destroying" ? "bg-orange-100 text-orange-800" :
                "bg-yellow-100 text-yellow-800"
              }`}>
                {r.status}
              </span>
            </td>
            <td className="py-3 text-sm text-gray-600">{r.region}</td>
            <td className="py-3 text-sm text-gray-500">
              {new Date(r.created_at).toLocaleDateString()}
            </td>
            <td className="py-3">
              <button
                onClick={() => onDelete(r.id)}
                className="text-red-600 hover:text-red-800 text-sm"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

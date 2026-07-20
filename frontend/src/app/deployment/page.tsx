"use client";
import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import DeploymentTable from "@/components/deployment/DeploymentTable";
import { Deployment } from "@/types";

export default function DeploymentPage() {
  const [deployments, setDeployments] = useState<Deployment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAPI("/api/deployment/")
      .then((d) => setDeployments(d.deployments || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Deployments</h1>
        <a href="/deployment/new" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">+ New Deployment</a>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        {loading ? <p>Loading...</p> : <DeploymentTable deployments={deployments} />}
      </div>
    </div>
  );
}

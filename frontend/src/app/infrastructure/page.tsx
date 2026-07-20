"use client";
import { useEffect, useState } from "react";
import { fetchAPI } from "@/lib/api";
import ResourceTable from "@/components/infrastructure/ResourceTable";
import { Resource } from "@/types";

export default function InfrastructurePage() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);

  const loadResources = async () => {
    try {
      const data = await fetchAPI("/api/infrastructure/");
      setResources(data.resources || []);
    } catch {}
    setLoading(false);
  };

  useEffect(() => {
    loadResources();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to destroy this resource?")) return;
    try {
      await fetchAPI(`/api/infrastructure/${id}`, { method: "DELETE" });
      loadResources();
    } catch (e: any) {
      alert("Failed: " + e.message);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Infrastructure Resources</h1>
        <div className="space-x-2">
          <a href="/infrastructure/ec2" className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">+ EC2</a>
          <a href="/infrastructure/s3" className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700">+ S3</a>
          <a href="/infrastructure/vpc" className="px-3 py-1 bg-purple-600 text-white rounded text-sm hover:bg-purple-700">+ VPC</a>
          <a href="/infrastructure/rds" className="px-3 py-1 bg-orange-600 text-white rounded text-sm hover:bg-orange-700">+ RDS</a>
        </div>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        {loading ? <p>Loading...</p> : <ResourceTable resources={resources} onDelete={handleDelete} />}
      </div>
    </div>
  );
}

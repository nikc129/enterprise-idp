from fastapi import APIRouter

from app.schemas.monitoring import InstanceMetrics, ContainerInfo, TerraformStatus
from app.services.monitoring_service import monitoring_service
from app.services.docker_service import docker_service

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])


@router.get("/{instance_id}/metrics", response_model=InstanceMetrics)
async def get_instance_metrics(instance_id: str):
    metrics = await monitoring_service.get_all_metrics(instance_id)
    return InstanceMetrics(**metrics)


@router.get("/{instance_id}/containers", response_model=list[ContainerInfo])
async def get_containers(instance_id: str):
    containers = docker_service.get_container_status()
    return [ContainerInfo(**c) for c in containers]


@router.get("/terraform/status", response_model=TerraformStatus)
async def get_terraform_status():
    status = await monitoring_service.get_terraform_status()
    return TerraformStatus(**status)

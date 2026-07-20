from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.resource_repo import ResourceRepository
from app.repositories.deployment_repo import DeploymentRepository
from app.services.terraform_service import TerraformService
from app.services.docker_service import docker_service
from app.services.github_service import github_service

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.get("/terraform/{resource_id}")
async def get_terraform_logs(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    service = TerraformService(repo)
    logs = await service.get_terraform_logs(resource_id)
    return {"resource_id": resource_id, "logs": logs}


@router.get("/deployment/{deployment_id}")
async def get_deployment_logs(
    deployment_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = DeploymentRepository(db)
    deployment = await repo.get_by_id(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")

    logs = deployment.logs
    if deployment.github_run_id and not logs:
        logs = await github_service.get_build_logs(
            deployment.github_repo, deployment.github_run_id
        )
    return {"deployment_id": deployment_id, "logs": logs}


@router.get("/docker/{instance_id}")
async def get_docker_logs(
    instance_id: str,
    container: str = "",
    lines: int = 100,
):
    if container:
        logs = docker_service.get_container_logs(container, lines)
        return {"instance_id": instance_id, "container": container, "logs": logs}

    containers = docker_service.get_container_status()
    all_logs = {}
    for c in containers:
        all_logs[c["name"]] = docker_service.get_container_logs(c["id"], lines)
    return {"instance_id": instance_id, "logs": all_logs}

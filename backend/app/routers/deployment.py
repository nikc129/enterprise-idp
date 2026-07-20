from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.deployment_repo import DeploymentRepository
from app.repositories.resource_repo import ResourceRepository
from app.schemas.deployment import (
    DeploymentCreate,
    DeploymentResponse,
    DeploymentListResponse,
    RepoResponse,
    BranchResponse,
)
from app.services.github_service import github_service

router = APIRouter(prefix="/api/deployment", tags=["deployment"])


@router.post("/", response_model=DeploymentResponse)
async def create_deployment(
    data: DeploymentCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    resource = await repo.get_by_id(data.resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    if resource.resource_type != "ec2":
        raise HTTPException(status_code=400, detail="Deployments require an EC2 resource")

    deploy_repo = DeploymentRepository(db)
    deployment = await deploy_repo.create(
        resource_id=data.resource_id,
        github_repo=data.github_repo,
        github_branch=data.github_branch,
        docker_image=data.docker_image,
    )

    if resource.cloud_id:
        run_id = await github_service.trigger_deploy(
            repo=data.github_repo,
            branch=data.github_branch,
            instance_ip=resource.cloud_id,
            image=data.docker_image,
        )
        if run_id:
            await deploy_repo.update_status(deployment.id, "building", github_run_id=run_id)

    return DeploymentResponse.model_validate(deployment)


@router.get("/", response_model=DeploymentListResponse)
async def list_deployments(
    db: AsyncSession = Depends(get_db),
):
    repo = DeploymentRepository(db)
    deployments = await repo.list_all()
    return DeploymentListResponse(
        deployments=[DeploymentResponse.model_validate(d) for d in deployments],
        total=len(deployments),
    )


@router.get("/{deployment_id}", response_model=DeploymentResponse)
async def get_deployment(
    deployment_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = DeploymentRepository(db)
    deployment = await repo.get_by_id(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return DeploymentResponse.model_validate(deployment)


@router.get("/{deployment_id}/status")
async def get_deployment_status(
    deployment_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = DeploymentRepository(db)
    deployment = await repo.get_by_id(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")

    if deployment.github_run_id:
        status = await github_service.get_deployment_status(
            deployment.github_repo, deployment.github_run_id
        )
        if status.get("conclusion") == "success":
            await repo.update_status(deployment.id, "running")
        elif status.get("conclusion") == "failure":
            await repo.update_status(deployment.id, "failed")
        return status
    return {"status": deployment.status}


@router.get("/repos/list", response_model=list[RepoResponse])
async def list_repos():
    repos = await github_service.get_user_repos()
    return [RepoResponse(**r) for r in repos]


@router.get("/repos/{repo:path}/branches", response_model=list[BranchResponse])
async def list_branches(repo: str):
    branches = await github_service.get_repo_branches(repo)
    return [BranchResponse(**b) for b in branches]

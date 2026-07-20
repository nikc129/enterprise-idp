from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.resource_repo import ResourceRepository
from app.schemas.infrastructure import (
    EC2Create,
    S3Create,
    VPCCreate,
    RDSCreate,
    ResourceResponse,
    ResourceListResponse,
)
from app.services.terraform_service import TerraformService
from app.services.aws_service import aws_service

router = APIRouter(prefix="/api/infrastructure", tags=["infrastructure"])


@router.post("/ec2", response_model=ResourceResponse)
async def create_ec2(
    data: EC2Create,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    service = TerraformService(repo)
    try:
        resource = await service.provision_ec2(data)
        return ResourceResponse.model_validate(resource)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/s3", response_model=ResourceResponse)
async def create_s3(
    data: S3Create,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    service = TerraformService(repo)
    try:
        resource = await service.provision_s3(data)
        return ResourceResponse.model_validate(resource)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vpc", response_model=ResourceResponse)
async def create_vpc(
    data: VPCCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    service = TerraformService(repo)
    try:
        resource = await service.provision_vpc(data)
        return ResourceResponse.model_validate(resource)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rds", response_model=ResourceResponse)
async def create_rds(
    data: RDSCreate,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    service = TerraformService(repo)
    try:
        resource = await service.provision_rds(data)
        return ResourceResponse.model_validate(resource)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=ResourceListResponse)
async def list_resources(
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    resources = await repo.list_all()
    return ResourceListResponse(
        resources=[ResourceResponse.model_validate(r) for r in resources],
        total=len(resources),
    )


@router.get("/{resource_type}", response_model=ResourceListResponse)
async def list_resources_by_type(
    resource_type: str,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    resources = await repo.list_by_type(resource_type)
    return ResourceListResponse(
        resources=[ResourceResponse.model_validate(r) for r in resources],
        total=len(resources),
    )


@router.get("/{resource_id}/detail", response_model=ResourceResponse)
async def get_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    resource = await repo.get_by_id(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return ResourceResponse.model_validate(resource)


@router.delete("/{resource_id}")
async def destroy_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    service = TerraformService(repo)
    try:
        await service.destroy_resource(resource_id)
        return {"message": "Resource destroyed"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{resource_id}/status")
async def get_resource_status(
    resource_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    resource = await repo.get_by_id(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource.resource_type == "ec2" and resource.cloud_id:
        status = await aws_service.get_instance_status(resource.cloud_id)
        return status
    return {"resource_id": resource_id, "status": resource.status}

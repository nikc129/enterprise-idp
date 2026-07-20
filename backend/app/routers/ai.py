from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.resource_repo import ResourceRepository
from app.schemas.ai import (
    AIProvisionRequest,
    AIProvisionResponse,
    AIOptimizeResponse,
    AITroubleshootRequest,
    AITroubleshootResponse,
)
from app.services.ai_service import ai_service
from app.services.monitoring_service import monitoring_service

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/provision", response_model=AIProvisionResponse)
async def ai_provision(data: AIProvisionRequest):
    result = await ai_service.natural_language_provision(data.query)
    return AIProvisionResponse(**result)


@router.get("/optimize", response_model=AIOptimizeResponse)
async def ai_optimize(db: AsyncSession = Depends(get_db)):
    repo = ResourceRepository(db)
    resources = await repo.list_all()
    resource_dicts = [
        {"id": r.id, "type": r.resource_type, "name": r.name, "status": r.status}
        for r in resources
    ]
    result = await ai_service.cost_optimization_advisor(resource_dicts)
    return AIOptimizeResponse(**result)


@router.post("/troubleshoot", response_model=AITroubleshootResponse)
async def ai_troubleshoot(
    data: AITroubleshootRequest,
    db: AsyncSession = Depends(get_db),
):
    repo = ResourceRepository(db)
    resource = await repo.get_by_id(data.resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    resource_info = {
        "id": resource.id,
        "type": resource.resource_type,
        "name": resource.name,
        "status": resource.status,
        "cloud_id": resource.cloud_id,
        "config": resource.config_json,
    }
    result = await ai_service.troubleshoot(resource_info)
    return AITroubleshootResponse(resource_id=data.resource_id, **result)

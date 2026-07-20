from pydantic import BaseModel


class AIProvisionRequest(BaseModel):
    query: str


class AIProvisionResponse(BaseModel):
    intent: str
    resource_type: str
    parameters: dict
    plan: str
    confirmed: bool = False


class AIOptimizeResponse(BaseModel):
    recommendations: list[dict]
    total_estimated_savings: str


class AITroubleshootRequest(BaseModel):
    resource_id: int


class AITroubleshootResponse(BaseModel):
    resource_id: int
    diagnosis: str
    root_cause: str
    suggested_fixes: list[str]

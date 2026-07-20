from pydantic import BaseModel


class CPUMetric(BaseModel):
    timestamp: str
    value: float


class MemoryMetric(BaseModel):
    timestamp: str
    value: float


class DiskMetric(BaseModel):
    timestamp: str
    value: float


class InstanceMetrics(BaseModel):
    instance_id: str
    cpu: list[CPUMetric]
    memory: list[MemoryMetric]
    disk: list[DiskMetric]


class ContainerInfo(BaseModel):
    id: str
    name: str
    status: str
    image: str
    created: str
    ports: str


class TerraformStatus(BaseModel):
    running: bool
    active_workspaces: list[str]
    last_execution: str

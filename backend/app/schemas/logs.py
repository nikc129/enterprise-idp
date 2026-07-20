from pydantic import BaseModel


class TerraformLogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
    resource: str = ""


class DeploymentLogEntry(BaseModel):
    timestamp: str
    step: str
    message: str
    status: str


class DockerLogEntry(BaseModel):
    timestamp: str
    stream: str
    log: str

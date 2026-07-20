from datetime import datetime

from pydantic import BaseModel


class DeploymentCreate(BaseModel):
    resource_id: int
    github_repo: str
    github_branch: str = "main"
    docker_image: str = ""


class DeploymentResponse(BaseModel):
    id: int
    resource_id: int
    github_repo: str
    github_branch: str
    docker_image: str
    status: str
    github_run_id: str
    logs: str
    deployed_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DeploymentListResponse(BaseModel):
    deployments: list[DeploymentResponse]
    total: int


class RepoResponse(BaseModel):
    full_name: str
    name: str
    default_branch: str
    html_url: str


class BranchResponse(BaseModel):
    name: str
    commit_sha: str

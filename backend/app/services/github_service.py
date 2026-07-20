import logging

from app.integrations.github_client import github_client
from app.core.config import settings

logger = logging.getLogger(__name__)


class GitHubService:
    def __init__(self):
        self.client = github_client

    async def get_user_repos(self) -> list[dict]:
        try:
            repos = await self.client.list_repositories()
            return [
                {
                    "full_name": r.get("full_name", ""),
                    "name": r.get("name", ""),
                    "default_branch": r.get("default_branch", "main"),
                    "html_url": r.get("html_url", ""),
                }
                for r in repos
            ]
        except Exception as e:
            logger.error(f"Failed to list repos: {e}")
            return []

    async def get_repo_branches(self, repo: str) -> list[dict]:
        try:
            if "/" in repo:
                owner, repo_name = repo.split("/", 1)
            else:
                owner = settings.GITHUB_ORG or ""
                repo_name = repo
                if not owner:
                    repos = await self.client.list_repositories()
                    for r in repos:
                        if r.get("name") == repo:
                            owner = r.get("owner", {}).get("login", "")
                            break

            branches = await self.client.list_branches(owner, repo_name)
            return [
                {
                    "name": b.get("name", ""),
                    "commit_sha": b.get("commit", {}).get("sha", ""),
                }
                for b in branches
            ]
        except Exception as e:
            logger.error(f"Failed to list branches for {repo}: {e}")
            return []

    async def trigger_build(self, repo: str, branch: str, image_name: str) -> str:
        try:
            if "/" in repo:
                owner, repo_name = repo.split("/", 1)
            else:
                owner = settings.GITHUB_ORG or ""
                repo_name = repo

            tag = branch.replace("/", "-")
            success = await self.client.trigger_workflow(
                owner=owner,
                repo=repo_name,
                workflow_id="docker-build.yml",
                ref=branch,
                inputs={"image_name": image_name, "tag": tag},
            )
            if success:
                runs = await self.client.list_workflow_runs(owner, repo_name)
                if runs:
                    return str(runs[0].get("id", ""))
            return ""
        except Exception as e:
            logger.error(f"Failed to trigger build: {e}")
            return ""

    async def trigger_deploy(self, repo: str, branch: str, instance_ip: str, image: str) -> str:
        try:
            if "/" in repo:
                owner, repo_name = repo.split("/", 1)
            else:
                owner = settings.GITHUB_ORG or ""
                repo_name = repo

            tag = branch.replace("/", "-")
            success = await self.client.trigger_workflow(
                owner=owner,
                repo=repo_name,
                workflow_id="deploy-ec2.yml",
                ref=branch,
                inputs={
                    "instance_ip": instance_ip,
                    "image_name": image,
                    "tag": tag,
                },
            )
            if success:
                runs = await self.client.list_workflow_runs(owner, repo_name)
                if runs:
                    return str(runs[0].get("id", ""))
            return ""
        except Exception as e:
            logger.error(f"Failed to trigger deploy: {e}")
            return ""

    async def get_deployment_status(self, repo: str, run_id: str) -> dict:
        try:
            if "/" in repo:
                owner, repo_name = repo.split("/", 1)
            else:
                owner = settings.GITHUB_ORG or ""
                repo_name = repo

            run = await self.client.get_workflow_run(owner, repo_name, int(run_id))
            return {
                "status": run.get("status", "unknown"),
                "conclusion": run.get("conclusion", ""),
                "html_url": run.get("html_url", ""),
            }
        except Exception as e:
            logger.error(f"Failed to get deployment status: {e}")
            return {"status": "unknown", "conclusion": "", "html_url": ""}

    async def get_build_logs(self, repo: str, run_id: str) -> str:
        try:
            if "/" in repo:
                owner, repo_name = repo.split("/", 1)
            else:
                owner = settings.GITHUB_ORG or ""
                repo_name = repo
            return await self.client.get_workflow_run_logs(owner, repo_name, int(run_id))
        except Exception as e:
            return f"Error fetching logs: {e}"


github_service = GitHubService()

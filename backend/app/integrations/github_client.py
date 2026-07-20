import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"


class GitHubClient:
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

        self.client = httpx.AsyncClient(
            base_url=GITHUB_API_BASE,
            headers=self.headers,
            timeout=30.0,
        )

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> dict | list:
        try:
            response = await self.client.request(
                method,
                endpoint,
                **kwargs,
            )

            response.raise_for_status()

            if response.content:
                return response.json()

            return {}

        except httpx.HTTPStatusError as e:
            logger.error(
                "GitHub API Error %s: %s",
                e.response.status_code,
                e.response.text,
            )
            raise

        except Exception as e:
            logger.exception("GitHub request failed")
            raise

    # ==========================================================
    # Repositories
    # ==========================================================

    async def list_repositories(self):
        if settings.GITHUB_ORG:
            return await self._request(
                "GET",
                f"/orgs/{settings.GITHUB_ORG}/repos",
                params={
                    "per_page": 100,
                    "sort": "updated",
                },
            )

        return await self._request(
            "GET",
            "/user/repos",
            params={
                "per_page": 100,
                "sort": "updated",
            },
        )

    async def get_repository(
        self,
        owner: str,
        repo: str,
    ):
        return await self._request(
            "GET",
            f"/repos/{owner}/{repo}",
        )

    # ==========================================================
    # Branches
    # ==========================================================

    async def list_branches(
        self,
        owner: str,
        repo: str,
    ):
        return await self._request(
            "GET",
            f"/repos/{owner}/{repo}/branches",
        )

    # ==========================================================
    # Commits
    # ==========================================================

    async def latest_commit(
        self,
        owner: str,
        repo: str,
        branch: str = "main",
    ):
        commits = await self._request(
            "GET",
            f"/repos/{owner}/{repo}/commits",
            params={"sha": branch, "per_page": 1},
        )

        return commits[0] if commits else {}

    # ==========================================================
    # Workflows
    # ==========================================================

    async def list_workflows(
        self,
        owner: str,
        repo: str,
    ):
        result = await self._request(
            "GET",
            f"/repos/{owner}/{repo}/actions/workflows",
        )

        return result.get("workflows", [])

    async def trigger_workflow(
        self,
        owner: str,
        repo: str,
        workflow_id: str,
        ref: str,
        inputs: dict | None = None,
    ) -> bool:

        payload = {"ref": ref}

        if inputs:
            payload["inputs"] = inputs

        response = await self.client.post(
            f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            json=payload,
        )

        return response.status_code == 204

    async def list_workflow_runs(
        self,
        owner: str,
        repo: str,
    ):
        result = await self._request(
            "GET",
            f"/repos/{owner}/{repo}/actions/runs",
            params={"per_page": 50},
        )

        return result.get("workflow_runs", [])

    async def get_workflow_run(
        self,
        owner: str,
        repo: str,
        run_id: int,
    ):
        return await self._request(
            "GET",
            f"/repos/{owner}/{repo}/actions/runs/{run_id}",
        )

    async def rerun_workflow(
        self,
        owner: str,
        repo: str,
        run_id: int,
    ) -> bool:

        response = await self.client.post(
            f"/repos/{owner}/{repo}/actions/runs/{run_id}/rerun"
        )

        return response.status_code == 201

    async def cancel_workflow(
        self,
        owner: str,
        repo: str,
        run_id: int,
    ) -> bool:

        response = await self.client.post(
            f"/repos/{owner}/{repo}/actions/runs/{run_id}/cancel"
        )

        return response.status_code == 202

    async def get_workflow_logs(
        self,
        owner: str,
        repo: str,
        run_id: int,
    ) -> str:

        response = await self.client.get(
            f"/repos/{owner}/{repo}/actions/runs/{run_id}/logs"
        )

        return response.text

    async def close(self):
        await self.client.aclose()


github_client = GitHubClient()
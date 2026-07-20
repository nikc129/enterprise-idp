from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deployment import Deployment


class DeploymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    async def create(
        self,
        resource_id: int,
        github_repo: str,
        github_branch: str,
        docker_image: str,
        deployed_by: int | None = None,
    ) -> Deployment:

        deployment = Deployment(
            resource_id=resource_id,
            github_repo=github_repo,
            github_branch=github_branch,
            docker_image=docker_image,
            status="pending",
            deployed_by=deployed_by,
        )

        self.db.add(deployment)

        await self.db.commit()
        await self.db.refresh(deployment)

        return deployment

    # ==========================================================
    # Read
    # ==========================================================

    async def get_by_id(
        self,
        deployment_id: int,
    ) -> Deployment | None:

        result = await self.db.execute(
            select(Deployment).where(
                Deployment.id == deployment_id
            )
        )

        return result.scalar_one_or_none()

    async def list_all(self) -> list[Deployment]:

        result = await self.db.execute(
            select(Deployment).order_by(
                Deployment.created_at.desc()
            )
        )

        return list(result.scalars().all())

    async def list_by_status(
        self,
        status: str,
    ) -> list[Deployment]:

        result = await self.db.execute(
            select(Deployment)
            .where(Deployment.status == status)
            .order_by(Deployment.created_at.desc())
        )

        return list(result.scalars().all())

    async def list_by_resource(
        self,
        resource_id: int,
    ) -> list[Deployment]:

        result = await self.db.execute(
            select(Deployment)
            .where(
                Deployment.resource_id == resource_id
            )
            .order_by(Deployment.created_at.desc())
        )

        return list(result.scalars().all())

    async def list_by_user(
        self,
        user_id: int,
    ) -> list[Deployment]:

        result = await self.db.execute(
            select(Deployment)
            .where(
                Deployment.deployed_by == user_id
            )
            .order_by(Deployment.created_at.desc())
        )

        return list(result.scalars().all())

    async def get_by_github_run(
        self,
        github_run_id: str,
    ) -> Deployment | None:

        result = await self.db.execute(
            select(Deployment).where(
                Deployment.github_run_id == github_run_id
            )
        )

        return result.scalar_one_or_none()

    async def latest(self) -> Deployment | None:

        result = await self.db.execute(
            select(Deployment)
            .order_by(Deployment.created_at.desc())
            .limit(1)
        )

        return result.scalar_one_or_none()

    # ==========================================================
    # Update
    # ==========================================================

    async def update_status(
        self,
        deployment_id: int,
        status: str,
        github_run_id: str | None = None,
        logs: str | None = None,
    ) -> Deployment | None:

        deployment = await self.get_by_id(deployment_id)

        if not deployment:
            return None

        deployment.status = status

        if github_run_id is not None:
            deployment.github_run_id = github_run_id

        if logs is not None:
            deployment.logs = logs

        deployment.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(deployment)

        return deployment

    async def update_logs(
        self,
        deployment_id: int,
        logs: str,
    ) -> Deployment | None:

        deployment = await self.get_by_id(deployment_id)

        if not deployment:
            return None

        deployment.logs = logs
        deployment.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(deployment)

        return deployment

    # ==========================================================
    # Delete
    # ==========================================================

    async def delete(
        self,
        deployment_id: int,
    ) -> bool:

        deployment = await self.get_by_id(deployment_id)

        if deployment is None:
            return False

        await self.db.delete(deployment)

        await self.db.commit()

        return True
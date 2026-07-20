import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource import Resource


class ResourceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    async def create(
        self,
        resource_type: str,
        name: str,
        cloud_id: str,
        status: str,
        terraform_workspace: str,
        config: dict,
        created_by: int | None = None,
        region: str = "ap-south-1",
    ) -> Resource:

        resource = Resource(
            resource_type=resource_type,
            name=name,
            cloud_id=cloud_id,
            region=region,
            status=status,
            terraform_workspace=terraform_workspace,
            config_json=json.dumps(config),
            created_by=created_by,
        )

        self.db.add(resource)

        await self.db.commit()
        await self.db.refresh(resource)

        return resource

    # ==========================================================
    # Read
    # ==========================================================

    async def get_by_id(
        self,
        resource_id: int,
    ) -> Resource | None:

        result = await self.db.execute(
            select(Resource).where(
                Resource.id == resource_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_name(
        self,
        name: str,
    ) -> Resource | None:

        result = await self.db.execute(
            select(Resource).where(
                Resource.name == name
            )
        )

        return result.scalar_one_or_none()

    async def get_by_cloud_id(
        self,
        cloud_id: str,
    ) -> Resource | None:

        result = await self.db.execute(
            select(Resource).where(
                Resource.cloud_id == cloud_id
            )
        )

        return result.scalar_one_or_none()

    async def list_all(self) -> list[Resource]:

        result = await self.db.execute(
            select(Resource).order_by(
                Resource.created_at.desc()
            )
        )

        return list(result.scalars().all())

    async def list_by_type(
        self,
        resource_type: str,
    ) -> list[Resource]:

        result = await self.db.execute(
            select(Resource)
            .where(
                Resource.resource_type == resource_type
            )
            .order_by(Resource.created_at.desc())
        )

        return list(result.scalars().all())

    async def list_by_status(
        self,
        status: str,
    ) -> list[Resource]:

        result = await self.db.execute(
            select(Resource)
            .where(Resource.status == status)
            .order_by(Resource.created_at.desc())
        )

        return list(result.scalars().all())

    async def list_by_region(
        self,
        region: str,
    ) -> list[Resource]:

        result = await self.db.execute(
            select(Resource)
            .where(Resource.region == region)
            .order_by(Resource.created_at.desc())
        )

        return list(result.scalars().all())

    async def list_by_workspace(
        self,
        workspace: str,
    ) -> list[Resource]:

        result = await self.db.execute(
            select(Resource)
            .where(
                Resource.terraform_workspace == workspace
            )
            .order_by(Resource.created_at.desc())
        )

        return list(result.scalars().all())

    async def list_by_creator(
        self,
        user_id: int,
    ) -> list[Resource]:

        result = await self.db.execute(
            select(Resource)
            .where(
                Resource.created_by == user_id
            )
            .order_by(Resource.created_at.desc())
        )

        return list(result.scalars().all())

    # ==========================================================
    # Update
    # ==========================================================

    async def update_status(
        self,
        resource_id: int,
        status: str,
        cloud_id: str | None = None,
    ) -> Resource | None:

        resource = await self.get_by_id(resource_id)

        if resource is None:
            return None

        resource.status = status

        if cloud_id is not None:
            resource.cloud_id = cloud_id

        resource.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(resource)

        return resource

    async def update_configuration(
        self,
        resource_id: int,
        config: dict,
    ) -> Resource | None:

        resource = await self.get_by_id(resource_id)

        if resource is None:
            return None

        resource.config_json = json.dumps(config)
        resource.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(resource)

        return resource

    # ==========================================================
    # Delete
    # ==========================================================

    async def delete(
        self,
        resource_id: int,
    ) -> bool:

        resource = await self.get_by_id(resource_id)

        if resource is None:
            return False

        await self.db.delete(resource)

        await self.db.commit()

        return True
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

hash_password = lambda p: p
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    async def create(
        self,
        username: str,
        email: str,
        password: str,
        role: str = "developer",
    ) -> User:

        user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role=role,
        )

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    # ==========================================================
    # Read
    # ==========================================================

    async def get_by_id(
        self,
        user_id: int,
    ) -> User | None:

        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:

        result = await self.db.execute(
            select(User).where(User.username == username)
        )

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        result = await self.db.execute(
            select(User).where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def list_all(self) -> list[User]:

        result = await self.db.execute(
            select(User).order_by(User.username)
        )

        return list(result.scalars().all())

    async def list_by_role(
        self,
        role: str,
    ) -> list[User]:

        result = await self.db.execute(
            select(User)
            .where(User.role == role)
            .order_by(User.username)
        )

        return list(result.scalars().all())

    # ==========================================================
    # Update
    # ==========================================================

    async def update_role(
        self,
        user_id: int,
        role: str,
    ) -> User | None:

        user = await self.get_by_id(user_id)

        if user is None:
            return None

        user.role = role

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update_password(
        self,
        user_id: int,
        password: str,
    ) -> User | None:

        user = await self.get_by_id(user_id)

        if user is None:
            return None

        user.hashed_password = hash_password(password)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update_profile(
        self,
        user_id: int,
        username: str,
        email: str,
    ) -> User | None:

        user = await self.get_by_id(user_id)

        if user is None:
            return None

        user.username = username
        user.email = email

        await self.db.commit()
        await self.db.refresh(user)

        return user

    # ==========================================================
    # Delete
    # ==========================================================

    async def delete(
        self,
        user_id: int,
    ) -> bool:

        user = await self.get_by_id(user_id)

        if user is None:
            return False

        await self.db.delete(user)

        await self.db.commit()

        return True
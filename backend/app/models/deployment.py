from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Deployment(Base):
    __tablename__ = "deployments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False)
    github_repo: Mapped[str] = mapped_column(String(255), nullable=False)
    github_branch: Mapped[str] = mapped_column(String(100), nullable=False, default="main")
    docker_image: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    github_run_id: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    logs: Mapped[str] = mapped_column(Text, nullable=False, default="")
    deployed_by: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

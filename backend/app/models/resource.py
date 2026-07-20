from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    resource_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    cloud_id: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    region: Mapped[str] = mapped_column(String(20), nullable=False, default="ap-south-1")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="provisioning")
    terraform_workspace: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    config_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_by: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

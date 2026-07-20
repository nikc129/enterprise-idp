"""initial schema

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="developer"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "resources",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resource_type", sa.String(20), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("cloud_id", sa.String(255), nullable=False, server_default=""),
        sa.Column("region", sa.String(20), nullable=False, server_default="ap-south-1"),
        sa.Column("status", sa.String(20), nullable=False, server_default="provisioning"),
        sa.Column("terraform_workspace", sa.String(255), nullable=False, server_default=""),
        sa.Column("config_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resources_resource_type", "resources", ["resource_type"])

    op.create_table(
        "deployments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.Column("github_repo", sa.String(255), nullable=False),
        sa.Column("github_branch", sa.String(100), nullable=False, server_default="main"),
        sa.Column("docker_image", sa.String(255), nullable=False, server_default=""),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("github_run_id", sa.String(50), nullable=False, server_default=""),
        sa.Column("logs", sa.Text(), nullable=False, server_default=""),
        sa.Column("deployed_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["resource_id"], ["resources.id"]),
        sa.ForeignKeyConstraint(["deployed_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("resource_type", sa.String(20), nullable=False, server_default=""),
        sa.Column("resource_id", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("details", sa.Text(), nullable=False, server_default=""),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("deployments")
    op.drop_table("resources")
    op.drop_table("users")

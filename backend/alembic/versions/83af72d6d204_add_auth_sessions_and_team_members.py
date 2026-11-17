"""Add revocable auth sessions and team memberships.

Revision ID: 83af72d6d204
Revises: 0f92a8c147bd
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "83af72d6d204"
down_revision: Union[str, None] = "0f92a8c147bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "must_change_password",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("csrf_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.Integer(), nullable=False),
        sa.Column("revoked_at", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_auth_sessions_id"), "auth_sessions", ["id"], unique=False)
    op.create_index(
        op.f("ix_auth_sessions_user_id"), "auth_sessions", ["user_id"], unique=False
    )
    op.create_index(
        op.f("ix_auth_sessions_token_hash"),
        "auth_sessions",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        op.f("ix_auth_sessions_expires_at"),
        "auth_sessions",
        ["expires_at"],
        unique=False,
    )
    op.create_table(
        "team_memberships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("member_role", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("team_id", "user_id", name="uq_team_membership"),
    )
    op.create_index(
        op.f("ix_team_memberships_id"), "team_memberships", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_team_memberships_team_id"),
        "team_memberships",
        ["team_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_team_memberships_user_id"),
        "team_memberships",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_team_memberships_user_id"), table_name="team_memberships")
    op.drop_index(op.f("ix_team_memberships_team_id"), table_name="team_memberships")
    op.drop_index(op.f("ix_team_memberships_id"), table_name="team_memberships")
    op.drop_table("team_memberships")
    op.drop_index(op.f("ix_auth_sessions_expires_at"), table_name="auth_sessions")
    op.drop_index(op.f("ix_auth_sessions_token_hash"), table_name="auth_sessions")
    op.drop_index(op.f("ix_auth_sessions_user_id"), table_name="auth_sessions")
    op.drop_index(op.f("ix_auth_sessions_id"), table_name="auth_sessions")
    op.drop_table("auth_sessions")
    op.drop_column("users", "must_change_password")

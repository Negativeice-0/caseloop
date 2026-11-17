"""Add human-reviewed intake submissions.

Revision ID: 0f92a8c147bd
Revises: 85daa8c7a156
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0f92a8c147bd"
down_revision: Union[str, None] = "85daa8c7a156"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "intake_submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_channel", sa.String(), nullable=False),
        sa.Column("source_message_id", sa.String(), nullable=True),
        sa.Column("source_text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("response_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["response_id"], ["responses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_intake_submissions_id"), "intake_submissions", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_intake_submissions_source_message_id"),
        "intake_submissions",
        ["source_message_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_intake_submissions_source_message_id"),
        table_name="intake_submissions",
    )
    op.drop_index(op.f("ix_intake_submissions_id"), table_name="intake_submissions")
    op.drop_table("intake_submissions")

"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-02-28
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "aigis_policies",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("stage", sa.String(length=32), nullable=False),
        sa.Column("action", sa.String(length=32), nullable=False),
        sa.Column("match_json", sa.Text, nullable=False),
        sa.Column("risk", sa.String(length=32), nullable=True),
        sa.Column("enabled", sa.Boolean, default=True),
    )

    op.create_table(
        "aigis_tool_policies",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(length=64), nullable=False, unique=True),
        sa.Column("allowed_envs", sa.Text, nullable=True),
        sa.Column("allowlist", sa.Text, nullable=True),
        sa.Column("timeout_seconds", sa.Integer, nullable=False, default=5),
        sa.Column("max_bytes", sa.Integer, nullable=True),
    )


def downgrade():
    op.drop_table("aigis_tool_policies")
    op.drop_table("aigis_policies")

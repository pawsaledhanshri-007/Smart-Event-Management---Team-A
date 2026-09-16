"""add advanced authentication and security fields

Revision ID: 9f3a2c1e6b7d
Revises: 7c7bf3ebec9d
Create Date: 2026-09-17
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "9f3a2c1e6b7d"
down_revision: Union[str, Sequence[str], None] = "7c7bf3ebec9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_email_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "users",
        sa.Column("email_verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("password_reset_version", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "users",
        sa.Column("totp_secret", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("is_2fa_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    # Preserve existing accounts during upgrade. New registrations are still
    # created as unverified by the application until they verify their email.
    op.execute(
        "UPDATE users SET is_email_verified = TRUE, email_verified_at = now() "
        "WHERE is_email_verified = FALSE"
    )

    op.create_table(
        "auth_sessions",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column("refresh_jti_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_auth_sessions_user_id", table_name="auth_sessions")
    op.drop_table("auth_sessions")
    op.drop_column("users", "is_2fa_enabled")
    op.drop_column("users", "totp_secret")
    op.drop_column("users", "password_reset_version")
    op.drop_column("users", "email_verified_at")
    op.drop_column("users", "is_email_verified")

import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
    Index,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ToolCall(Base):
    __tablename__ = "tool_calls"

    __table_args__ = (
        CheckConstraint(
            "latency_ms IS NULL OR latency_ms >= 0",
            name="ck_tool_calls_latency_nonneg"
        ),

        Index(
            "ix_tool_calls_tool_name",
            "tool_name"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("agent_runs.id",ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    tool_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    tool_input: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    tool_output: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    run = relationship(
        "AgentRun",
        back_populates="tool_calls"
    )
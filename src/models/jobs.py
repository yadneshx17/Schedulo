import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db import Base
from src.states import JobStatus, RetryStrategy


class Jobs(Base):
    """
    Job model for scheduling and tracking background tasks.

    Attributes:
        payload: JSON payload containing task parameters
        scheduled_fields: JSON fields for scheduling configuration
        recurring: Whether the job is recurring
        interval: Interval in seconds for recurring jobs
    """

    __tablename__ = "jobs"

    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    owner_id = Column(String, nullable=False, index=True)
    task_type = Column(String, nullable=False, index=True)
    payload = Column(Text, nullable=False)
    scheduled_fields = Column(
        Text, nullable=False
    )  # Extra data + config + rules needed to decide when and how a job should be scheduled, beyond fixed columns.

    # Scheduling fields
    recurring = Column(Boolean, default=False, nullable=False)
    interval = Column(Integer, nullable=True)  # in seconds
    next_run_at = Column(DateTime(timezone=True), nullable=True, index=True)

    # Status
    status = Column(
        Enum(JobStatus, name="job_status_enum"),
        nullable=False,
        index=True,
        default=JobStatus.PENDING,
    )

    # Retry fields
    max_retries = Column(Integer, default=3, nullable=False)
    retry_backoff_seconds = Column(Integer, default=300, nullable=False)
    retry_strategy = Column(
        Enum(RetryStrategy, name="retry_strategy_enum"),
        nullable=False,
        default=RetryStrategy.FIXED,
    )

    # Locking fields - prevent race condition
    locked_by = Column(String, nullable=True)
    locked_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    status_updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    job_runs = relationship(
        "Jobs_Run", back_populates="job", cascade="all, delete-orphan"
    )

    # Indexes for performance
    __table_args__ = (
        Index("idx_jobs_status_next_run", "status", "next_run_at"),
        Index("idx_jobs_owner_status", "owner_id", "status"),
        Index("idx_jobs_task_type_status", "task_type", "status"),
        Index("idx_jobs_locked_by_locked_at", "locked_by", "locked_at"),
        Index("idx_jobs_recurring_next_run", "recurring", "next_run_at"),
    )

    def __repr__(self) -> str:
        return f"<Jobs(id={self.id}, task_type={self.task_type}, status={self.status}), created_at={self.created_at}>"

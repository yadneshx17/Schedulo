import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.db import Base
from src.states import JobRunStatus


class Job_Runs(Base):
    """
    Attributes:
        attempt: Attempt number of task execution
    """

    __tablename__ = "job_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(
        UUID, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    attempt = Column(Integer, nullable=False)
    status = Column(Enum(JobRunStatus, name="job_run_status_enum"), nullable=False)
    worker_id = Column(String, nullable=False)
    error = Column(Text, nullable=True)

    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # relationship
    job = relationship("Jobs", back_populates="job_runs")

    __table_args__ = (Index("idx_job_runs_job_id_started_at", "job_id", "started_at"),)

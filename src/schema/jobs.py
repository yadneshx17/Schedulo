from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.states import JobStatus, RetryStrategy, JobRunStatus


class CreateJob(BaseModel):
    """Schema for creating a new job."""
    owner_id: str = Field(..., description="ID of the job owner")
    task_type: str = Field(..., description="Type of task to execute")
    payload: str = Field(..., description="JSON payload containing task parameters")
    scheduled_fields: str = Field(..., description="JSON fields for scheduling configuration")
    recurring: bool = Field(default=False, description="Whether the job is recurring")
    interval: Optional[int] = Field(None, description="Interval in seconds for recurring jobs")
    next_run_at: Optional[datetime] = Field(None, description="Next scheduled run time")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    retry_backoff_seconds: int = Field(default=300, description="Backoff time between retries in seconds")
    retry_strategy: RetryStrategy = Field(default=RetryStrategy.FIXED, description="Retry strategy")


class UpdateJob(BaseModel):
    """Schema for updating an existing job."""
    task_type: Optional[str] = Field(None, description="Type of task to execute")
    payload: Optional[str] = Field(None, description="JSON payload containing task parameters")
    scheduled_fields: Optional[str] = Field(None, description="JSON fields for scheduling configuration")
    recurring: Optional[bool] = Field(None, description="Whether the job is recurring")
    interval: Optional[int] = Field(None, description="Interval in seconds for recurring jobs")
    next_run_at: Optional[datetime] = Field(None, description="Next scheduled run time")
    max_retries: Optional[int] = Field(None, description="Maximum number of retries")
    retry_backoff_seconds: Optional[int] = Field(None, description="Backoff time between retries in seconds")
    retry_strategy: Optional[RetryStrategy] = Field(None, description="Retry strategy")


class JobResponse(BaseModel):
    """Schema for job response."""
    id: UUID = Field(..., description="Unique job identifier")
    owner_id: str = Field(..., description="ID of the job owner")
    task_type: str = Field(..., description="Type of task to execute")
    payload: str = Field(..., description="JSON payload containing task parameters")
    scheduled_fields: str = Field(..., description="JSON fields for scheduling configuration")
    recurring: bool = Field(..., description="Whether the job is recurring")
    interval: Optional[int] = Field(None, description="Interval in seconds for recurring jobs")
    next_run_at: Optional[datetime] = Field(None, description="Next scheduled run time")
    status: JobStatus = Field(..., description="Current job status")
    max_retries: int = Field(..., description="Maximum number of retries")
    retry_backoff_seconds: int = Field(..., description="Backoff time between retries in seconds")
    retry_strategy: RetryStrategy = Field(..., description="Retry strategy")
    locked_by: Optional[str] = Field(None, description="Worker ID that has locked the job")
    locked_at: Optional[datetime] = Field(None, description="When the job was locked")
    created_at: datetime = Field(..., description="When the job was created")
    updated_at: datetime = Field(..., description="When the job was last updated")
    status_updated_at: datetime = Field(..., description="When the status was last updated")

    class Config:
        from_attributes = True


class JobRunResponse(BaseModel):
    """Schema for job run response."""
    id: UUID = Field(..., description="Unique run identifier")
    job_id: UUID = Field(..., description="Parent job ID")
    attempt: int = Field(..., description="Attempt number")
    status: JobRunStatus = Field(..., description="Run status")
    worker_id: str = Field(..., description="Worker ID that executed the run")
    error: Optional[str] = Field(None, description="Error message if failed")
    started_at: Optional[datetime] = Field(None, description="When the run started")
    finished_at: Optional[datetime] = Field(None, description="When the run finished")
    created_at: datetime = Field(..., description="When the run was created")

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    """Schema for job list response."""
    jobs: list[JobResponse] = Field(..., description="List of jobs")
    total: int = Field(..., description="Total number of jobs")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of jobs per page")


class JobRunListResponse(BaseModel):
    """Schema for job run list response."""
    runs: list[JobRunResponse] = Field(..., description="List of job runs")
    total: int = Field(..., description="Total number of runs")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of runs per page")


class JobPauseRequest(BaseModel):
    """Schema for pausing a job."""
    reason: Optional[str] = Field(None, description="Reason for pausing the job")


class JobResumeRequest(BaseModel):
    """Schema for resuming a job."""
    reason: Optional[str] = Field(None, description="Reason for resuming the job")


class JobDeleteRequest(BaseModel):
    """Schema for deleting a job."""
    force: bool = Field(default=False, description="Force delete even if job is running")
    
    
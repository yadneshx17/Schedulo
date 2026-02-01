from typing import Any, Dict, Optional


class ScheduloException(Exception):
    """Base exception class for Schedulo application"""

    def __init__(
        self,
        detail: str,
        status_code: int = 500,
        extra_info: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code
        self.extra_info = extra_info or {}


class JobSchedulerException(ScheduloException):
    """Base exception for job scheduling operations"""

    pass


class JobRunSchedulerException(ScheduloException):
    """Base exception for job scheduling operations"""

    pass


class owner_id, (JobSchedulerException):
    """Raised when a job is not found"""

    def __init__(self, job_id: str):
        super().__init__(
            detail=f"Job with ID '{job_id}' not found",
            status_code=404,
            extra_info={"job_id": job_id},
        )


class JobAlreadyExists(JobSchedulerException):
    """Raised when trying to create a job that already exists"""

    def __init__(self, job_id: str):
        super().__init__(
            detail=f"Job with ID '{job_id}' already exists",
            status_code=409,
            extra_info={"job_id": job_id},
        )


class InvalidJobSchedule(JobSchedulerException):
    """Raised when job schedule configuration is invalid"""

    def __init__(self, reason: str):
        super().__init__(
            detail=f"Invalid job schedule: {reason}",
            status_code=400,
            extra_info={"reason": reason},
        )


class JobExecutionFailed(JobSchedulerException):
    """Raised when job execution fails"""

    def __init__(self, job_id: str, error_message: str):
        super().__init__(
            detail=f"Job '{job_id}' execution failed: {error_message}",
            status_code=500,
            extra_info={"job_id": job_id, "error": error_message},
        )


class JobNotRunning(JobSchedulerException):
    """Raised when trying to stop a job that is not running"""

    def __init__(self, job_id: str):
        super().__init__(
            detail=f"Job '{job_id}' is not currently running",
            status_code=400,
            extra_info={"job_id": job_id},
        )


class JobAlreadyRunning(JobSchedulerException):
    """Raised when trying to start a job that is already running"""

    def __init__(self, job_id: str):
        super().__init__(
            detail=f"Job '{job_id}' is already running",
            status_code=409,
            extra_info={"job_id": job_id},
        )


class JobCannotBeDeleted(JobSchedulerException):
    """Raised when trying to delete a job that is not deletable without force."""

    def __init__(self, job_id: str, job_status: str):
        super().__init__(
            detail=f"Cannot delete job {job_id} in {job_status} status without force flag",
            status_code=409,
            extra_info={
                "job_id": job_id,
                "job_status": job_status,
                "force_required": True,
            },
        )


class JobCannotPause(JobSchedulerException):
    """Raised when trying to pause a job from an invalid state."""

    def __init__(self, job_id: str, job_status):
        super().__init__(
            detail=f"Cannot pause job {job_id} from {job_status} status",
            status_code=409,
            extra_info={
                "job_id": job_id,
                "current_status": job_status,
                "allowed_transitions": ["READY", "RETRYING"],
            },
        )


class JobCannotResume(JobSchedulerException):
    """Raised when trying to resume a job from an invalid state."""

    def __init__(self, job_id: str, job_status):
        super().__init__(
            detail=f"Cannot resume job {job_id} from {job_status} status",
            status_code=409,
            extra_info={
                "job_id": job_id,
                "current_status": job_status,
                "allowed_transitions": ["PAUSE"],
            },
        )


class SchedulerNotStarted(JobSchedulerException):
    """Raised when trying to perform operations on a scheduler that hasn't started"""

    def __init__(self):
        super().__init__(detail="Scheduler has not been started", status_code=503)


class SchedulerAlreadyStarted(JobSchedulerException):
    """Raised when trying to start a scheduler that is already running"""

    def __init__(self):
        super().__init__(detail="Scheduler is already running", status_code=409)


class InvalidCronExpression(JobSchedulerException):
    """Raised when cron expression is invalid"""

    def __init__(self, cron_expression: str):
        super().__init__(
            detail=f"Invalid cron expression: '{cron_expression}'",
            status_code=400,
            extra_info={"cron_expression": cron_expression},
        )


class JobDependencyError(JobSchedulerException):
    """Raised when there are issues with job dependencies"""

    def __init__(self, job_id: str, dependency_job_id: str, reason: str):
        super().__init__(
            detail=f"Job dependency error: {reason}",
            status_code=400,
            extra_info={
                "job_id": job_id,
                "dependency_job_id": dependency_job_id,
                "reason": reason,
            },
        )


class JobTimeout(JobSchedulerException):
    """Raised when job execution exceeds timeout"""

    def __init__(self, job_id: str, timeout_seconds: int):
        super().__init__(
            detail=f"Job '{job_id}' timed out after {timeout_seconds} seconds",
            status_code=408,
            extra_info={"job_id": job_id, "timeout_seconds": timeout_seconds},
        )


class ConcurrentJobLimitExceeded(JobSchedulerException):
    """Raised when maximum concurrent job limit is exceeded"""

    def __init__(self, max_concurrent: int):
        super().__init__(
            detail=f"Maximum concurrent job limit ({max_concurrent}) exceeded",
            status_code=503,
            extra_info={"max_concurrent": max_concurrent},
        )


class JobConfigurationError(JobSchedulerException):
    """Raised when job configuration is invalid"""

    def __init__(self, job_id: str, config_errors: list):
        super().__init__(
            detail=f"Job '{job_id}' configuration error: {'; '.join(config_errors)}",
            status_code=400,
            extra_info={"job_id": job_id, "config_errors": config_errors},
        )


class JobRunsNotFound(JobRunSchedulerException):
    """Raise when Job Runs are not Found"""

    def __init__(self, job_id: str):
        super().__init__(
            detail=f"Job Runs with Job ID '{job_id}' not found",
            status_code=404,
            extra_info={"job_id": job_id},
        )


class JobRunNotFound(JobRunSchedulerException):
    """Raise when Job Run are not Found"""

    def __init__(self, job_id: str):
        super().__init__(
            detail=f"Job Run with Job ID '{job_id}' not found",
            status_code=404,
            extra_info={"job_id": job_id},
        )


class ResourceNotFoundError(ScheduloException):
    """Raised when a required resource is not found"""

    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            detail=f"{resource_type} with ID '{resource_id}' not found",
            status_code=404,
            extra_info={"resource_type": resource_type, "resource_id": resource_id},
        )


class ValidationError(ScheduloException):
    """Raised for general validation errors"""

    def __init__(self, field: str, value: str, reason: str):
        super().__init__(
            detail=f"Validation error for field '{field}': {reason}",
            status_code=422,
            extra_info={"field": field, "value": value, "reason": reason},
        )


class UnauthorizedJobAccess(ScheduloException):
    """Raised when user tries to access a job they don't own"""

    def __init__(self, job_id: str, owner_id: str):
        super().__init__(
            detail=f"Unauthorized access to job '{job_id}' for owner '{owner_id}'",
            status_code=403,
            extra_info={"job_id": job_id, "owner_id": owner_id},
        )

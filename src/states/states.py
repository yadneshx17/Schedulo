from enum import Enum


class JobStatus(Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    DEAD = "DEAD"


class RetryStrategy(Enum):
    FIXED = "fixed"
    EXPONENTIAL = "exponential"

class JobRunStatus(Enum):
    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"

ALLOWED_TRANSITIONS = {
    JobStatus.CREATED: {JobStatus.PENDING},
    JobStatus.PENDING: {JobStatus.SCHEDULED},
    JobStatus.SCHEDULED: {JobStatus.READY},
    JobStatus.READY: {JobStatus.RUNNING},
    JobStatus.RUNNING: {JobStatus.SUCCESS, JobStatus.FAILED},
    JobStatus.FAILED: {JobStatus.RETRYING, JobStatus.DEAD},
    JobStatus.RETRYING: {JobStatus.DEAD},
}


def can_transition(from_status: JobStatus, to_status: JobStatus) -> bool:
    return to_status in ALLOWED_TRANSITIONS.get(from_status, set())


if can_transition(JobStatus.CREATED, JobStatus.RUNNING):
    print("Validation Working")
else:
    print("Validation Failed")

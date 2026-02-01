from typing import List

from sqlalchemy import select

from src.core.Exceptions import (
    JobCannotBeDeleted,
    JobCannotPause,
    JobCannotResume,
    JobNotFound,
    JobRunNotFound,
    JobRunsNotFound,
    UnauthorizedJobAccess,
)
from src.models import Job_Runs, Jobs
from src.states.states import JobStatus, can_transition

# CHECKS
# 1. Owner
# job.owner_id == request.owner_id


async def _get_job_or_raise(job_id, owner_id, db):
    """Get job by ID and validate ownership"""
    job = await get_job_by_id(job_id, db)
    if not job:
        raise JobNotFound(str(job_id))
    if job.owner_id != owner_id:
        raise UnauthorizedJobAccess(str(job_id), owner_id)
    return job


async def get_job_by_id(job_id, db):
    """Get a single job by ID"""
    return (
        await db.execute(select(Jobs).where(Jobs.id == job_id))
    ).scalar_one_or_none()


async def get_jobs_by_ids(job_ids: List, db) -> List[Jobs]:
    """Get multiple jobs by list of IDs"""
    if not job_ids:
        return []
    result = await db.execute(select(Jobs).where(Jobs.id.in_(job_ids)))
    return result.scalars().all()


async def get_all_jobs(owner_id, db) -> List[Jobs]:
    """Get Whole job list"""
    result = await db.execute(select(Jobs))  #  never throws None -> []
    return result.scalars().all()


async def get_job_runs_by_job_id(job_id, db) -> List[Job_Runs]:
    return (
        (await db.execute(select(Job_Runs).where(Job_Runs.job_id == job_id)))
        .scalars()
        .all()
    )


async def get_job_run_by_id(job_id, run_id, db) -> List[Job_Runs]:
    return (
        await db.execute(
            select(Job_Runs).where(Job_Runs.job_id == job_id, Job_Runs.id == run_id)
        )
    ).scalar_one_or_none()


# async def _get_job_or_raise(job_id, owner_id, db):
#     job = await get_job_by_id(job_id, db)
#     if not job:
#         # raise JobNotFound(job_id)
#         return {"message": f"job: {job_id} does not found"}
#     # if job.owner_id != owner_id:
#     #     raise UnauthorizedJobAccess(job_id, owner_id)
#     return job


async def create_job(data, x_owner_id, db):
    job = Jobs(
        owner_id=x_owner_id,
        task_type=data.task_type,
        payload=data.payload,
        scheduled_fields=data.scheduled_fields,
        recurring=data.recurring,
        interval=data.interval,
        max_retries=data.max_retries,
        retry_backoff_seconds=data.retry_backoff_seconds,
        retry_strategy=data.retry_strategy,
        status=JobStatus.CREATED,
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_job(job_id, owner_id, db):
    return await _get_job_or_raise(job_id, owner_id, db)


async def list_jobs(owner_id, db):
    """List jobs filtered by owner_id"""
    jobs = await get_all_jobs(owner_id, db)
    return {"jobs": jobs, "total": len(jobs), "page": 1, "size": len(jobs)}


async def delete_job(force, job_id, owner_id, db):
    job = await _get_job_or_raise(job_id, owner_id, db)

    if not force and job.status in [
        JobStatus.RUNNING,
        JobStatus.READY,
        JobStatus.RETRYING,
    ]:
        raise JobCannotBeDeleted(job_id, job.status.value)

    await db.delete(job)
    await db.commit()
    return {"message": f"Job {job_id} deleted successfully"}


async def update_job(data, job_id, owner_id, db):
    job = await _get_job_or_raise(job_id, owner_id, db)

    # Update only provided fields
    if data.task_type is not None:
        job.task_type = data.task_type
    if data.payload is not None:
        job.payload = data.payload
    if data.scheduled_fields is not None:
        job.scheduled_fields = data.scheduled_fields
    if data.recurring is not None:
        job.recurring = data.recurring
    if data.interval is not None:
        job.interval = data.interval

    # Only allow schedule config changes
    # Recompute next_run_at via a function
    if data.next_run_at is not None:
        job.next_run_at = data.next_run_at
    if data.max_retries is not None:
        job.max_retries = data.max_retries
    if data.retry_backoff_seconds is not None:
        job.retry_backoff_seconds = data.retry_backoff_seconds
    if data.retry_strategy is not None:
        job.retry_strategy = data.retry_strategy

    await db.commit()
    await db.refresh(job)
    return job


# Actions
async def pause_job(job_id, owner_id, db):
    job = await _get_job_or_raise(job_id, owner_id, db)

    if not can_transition(job.status, JobStatus.PAUSE):
        raise JobCannotPause(str(job_id), job.status.value)

    job.status = JobStatus.PAUSE
    await db.commit()
    await db.refresh(job)
    return job


async def resume_job(job_id, owner_id, db):
    job = await _get_job_or_raise(job_id, owner_id, db)

    if job.status != JobStatus.PAUSE:
        raise JobCannotResume(str(job_id), job.status.value)
        # need to recalculate the next_run_at
    job.status = JobStatus.SCHEDULED
    await db.commit()
    await db.refresh(job)
    return job


# Job History
async def job_runs(job_id, db):
    # Verify job ownership before returning runs
    runs = await get_job_runs_by_id(job_id, db)

    return {"runs": runs, "total": len(runs), "page": 1, "size": len(runs)}


async def job_run(job_id, run_id, db):
    # Verify job ownership before returning run
    run = await get_job_run_by_id(job_id, run_id, db)
    if not run:
        raise ValueError(f"Job run {run_id} for job {job_id} not found")

    return run

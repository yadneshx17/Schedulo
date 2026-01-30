from sqlalchemy import select

from src.models import Job_Runs, Jobs
from src.states.states import JobStatus, can_transition


async def create_job(data, db):
    job = Jobs(
        owner_id=data.owner_id,
        task_type=data.task_type,
        payload=data.payload,
        scheduled_fields=data.scheduled_fields,
        recurring=data.recurring,
        interval=data.interval,
        next_run_at=data.next_run_at,
        max_retries=data.max_retries,
        retry_backoff_seconds=data.retry_backoff_seconds,
        retry_strategy=data.retry_strategy,
        status=JobStatus.CREATED,
    )

    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_job(job_id, db):
    stmt = select(Jobs).where(Jobs.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()

    if not job:
        raise ValueError(f"Job {job_id} not found")

    return job


async def list_jobs(db):
    results = await db.execute(select(Jobs))
    if not results:
        raise ValueError("Jobs not found")

    jobs = results.scalars().all()
    return {"jobs": jobs, "total": len(jobs), "page": 1, "size": len(jobs)}


async def delete_job(force, job_id, db):
    stmt = select(Jobs).where(Jobs.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()

    if not job:
        return {"message": f"job: {job_id} does not found"}

    if not force and job.status in [JobStatus.RUNNING]:
        raise ValueError(
            f"Cannot delete job {job_id} in {job.status.value} status without force flag"
        )

    await db.delete(job)
    await db.commit()
    return {"message": f"Job {job_id} deleted successfully"}


async def update_job(data, job_id, db):
    stmt = select(Jobs).where(Jobs.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()

    if not job:
        raise ValueError(f"Job {job_id} not found")

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
async def pause_job(reason, job_id, db):
    stmt = select(Jobs).where(Jobs.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()

    if not job:
        raise ValueError(f"Job {job_id} not found")

    if not can_transition(job.status, JobStatus.PENDING):
        raise ValueError(f"Cannot pause job {job_id} from {job.status.value} status")

    job.status = JobStatus.PENDING
    await db.commit()
    await db.refresh(job)
    return job


async def resume_job(reason, job_id, db):
    stmt = select(Jobs).where(Jobs.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()

    if not job:
        raise ValueError(f"Job {job_id} not found")

    if job.status != JobStatus.PENDING:
        raise ValueError(f"Cannot resume job {job_id} from {job.status.value} status")

    job.status = JobStatus.SCHEDULED
    await db.commit()
    await db.refresh(job)
    return job


# Job History
async def job_runs(job_id, db):
    stmt = select(Job_Runs).where(Job_Runs.job_id == job_id)
    result = await db.execute(stmt)
    runs = result.scalars().all()
    
    return {
        "runs": runs,
        "total": len(runs),
        "page": 1,
        "size": len(runs)
    }


async def job_run(job_id, run_id, db):
    stmt = select(Job_Runs).where(Job_Runs.job_id == job_id, Job_Runs.id == run_id)
    result = await db.execute(stmt)
    run = result.scalar_one_or_none()
    
    if not run:
        raise ValueError(f"Job run {run_id} for job {job_id} not found")
    
    return run

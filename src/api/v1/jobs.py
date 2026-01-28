import uuid

from fastapi import APIRouter

from src.services import (
    create_job,
    delete_job,
    get_job,
    list_jobs,
    pause_job,
    resume_job,
    update_job,
    
    job_run,
    list_job_runs
)

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])


@router.post("/")
async def handle_create_job():
    return create_job()


@router.get("/{job_id}")
async def handle_get_job(job_id: uuid.UUID):
    return get_job(job_id)


@router.delete("/{job_id}")
async def handle_delete_job(job_id: uuid.UUID):
    return delete_job(job_id)


@router.get("/")
async def handle_list_jobs(job_id: uuid.UUID):
    return list_jobs()


@router.post("/{job_id}")
async def handle_update_jobs(job_id: uuid.UUID):
    return update_job(job_id)


@router.post("/{job_id}/pause")
async def handle_pause_jobs(job_id: uuid.UUID):
    return pause_job(job_id)


@router.post("/{job_id}/resume")
async def handle_resume_jobs(job_id: uuid.UUID):
    return resume_job(job_id)


@router.get("/{job_id}/runs")
async def handle_job_runs(job_id: uuid.UUID):
    return job_run(job_id)

@router.get("/{job_id}/runs/{run_id}")
async def handle_job_run(job_id: uuid.UUID, run_id: uuid.UUID):
    return list_job_runs(job_id, run_id)

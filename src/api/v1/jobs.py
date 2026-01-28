import uuid

from fastapi import APIRouter

from src.schema import (
    CreateJob,
    JobDeleteRequest,
    JobListResponse,
    JobPauseRequest,
    JobResponse,
    JobResumeRequest,
    JobRunListResponse,
    JobRunResponse,
    UpdateJob,
)
from src.services import (
    create_job,
    delete_job,
    get_job,
    job_run,
    list_job_runs,
    list_jobs,
    pause_job,
    resume_job,
    update_job,
)

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])


@router.post("/", response_model=JobResponse)
async def handle_create_job(data: CreateJob):
    return create_job(data)


@router.get("/{job_id}", response_model=JobResponse)
async def handle_get_job(job_id: uuid.UUID):
    return get_job(job_id)


@router.get("/", response_model=JobListResponse)
async def handle_list_jobs(job_id: uuid.UUID):
    return list_jobs(job_id)


@router.delete("/{job_id}")
async def handle_delete_job(force: JobDeleteRequest, job_id: uuid.UUID):
    return delete_job(force, job_id)


@router.post("/{job_id}", response_model=JobResponse)
async def handle_update_jobs(data: UpdateJob, job_id: uuid.UUID):
    return update_job(job_id)


@router.post("/{job_id}/pause")
async def handle_pause_jobs(reason: JobPauseRequest, job_id: uuid.UUID):
    return pause_job(reason, job_id)


@router.post("/{job_id}/resume")
async def handle_resume_jobs(reason: JobResumeRequest, job_id: uuid.UUID):
    return resume_job(reason, job_id)


@router.get("/{job_id}/runs", response_model=JobRunResponse)
async def handle_job_runs(job_id: uuid.UUID):
    return job_run(job_id)


@router.get("/{job_id}/runs/{run_id}", response_model=JobRunListResponse)
async def handle_job_run(job_id: uuid.UUID, run_id: uuid.UUID):
    return list_job_runs(job_id, run_id)

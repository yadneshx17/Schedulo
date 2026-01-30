import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import getSession
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
    job_runs,
    job_run,
    list_jobs,
    pause_job,
    resume_job,
    update_job,
)

router = APIRouter()


@router.post("/", response_model=JobResponse)
async def handle_create_job(data: CreateJob, session: AsyncSession = Depends(getSession)):
    return await create_job(data, session)


@router.get("/{job_id}", response_model=JobResponse)
async def handle_get_job(job_id: uuid.UUID,  session: AsyncSession = Depends(getSession)):
    return await get_job(job_id, session)


@router.get("/", response_model=JobListResponse)
async def handle_list_jobs(session: AsyncSession = Depends(getSession)):
    return await list_jobs(session)


@router.delete("/{job_id}")
async def handle_delete_job(force: JobDeleteRequest, job_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    return await delete_job(force, job_id, session)


@router.patch("/{job_id}", response_model=JobResponse)
async def handle_update_jobs(data: UpdateJob, job_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    return await update_job(data, job_id, session)


@router.post("/{job_id}/pause")
async def handle_pause_jobs(reason: JobPauseRequest, job_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    return await pause_job(reason, job_id, session)


@router.post("/{job_id}/resume")
async def handle_resume_jobs(reason: JobResumeRequest, job_id: uuid.UUID,  session: AsyncSession = Depends(getSession)):
    return await resume_job(reason, job_id, session)


@router.get("/{job_id}/runs", response_model=JobRunListResponse)
async def handle_job_runs(job_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    return await job_runs(job_id, session)


@router.get("/{job_id}/runs/{run_id}", response_model=JobRunResponse)
async def handle_job_run(job_id: uuid.UUID, run_id: uuid.UUID, session: AsyncSession = Depends(getSession)):
    return await job_run(job_id, run_id, session)

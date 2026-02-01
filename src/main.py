import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.v1 import job
from src.core.Exceptions import ScheduloException
from src.db import Base, engine
from src.db.database import getSession
from src.models import job_runs, jobs
# from src.scheduler import scheduler_loop

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# async def start_background_tasks(app):
#     app.state.scheduler_task = asyncio.create_task(scheduler_loop(app.state.db))


# async def stop_background_tasks(app):
#     tasks = [
#         app.state.scheduler_task,
#     ]

#     for task in tasks:
#         task.cancel()
#         try:
#             await task
#         except asyncio.CancelledError:
#             pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Scheduler...")

    # app.state.db = getSession()
    # await start_background_tasks(app)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Shutting Scheduler...")
    # await stop_background_tasks(app)
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(job.router, prefix="/v1/jobs", tags=["jobs"])

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ScheduloException)
async def scheduler_exception_handler(request, exc: ScheduloException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "detail": exc.detail,
            "extra_info": exc.extra_info,
        },
    )


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True,
#         log_level="info",
#     )

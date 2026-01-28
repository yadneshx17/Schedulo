import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import Base, engine
from src.models import jobs, job_runs 

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Scheduler...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    logger.info("Shutting Scheduler...")
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=000,
#         reload=True,
#         log_level="info",
#     )

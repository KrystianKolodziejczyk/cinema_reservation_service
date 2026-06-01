from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.auth.presentation.routers.v1.auth_router import router as auth_router
from app.modules.healthcheck.healthcheck import router as healthcheck_router
from app.modules.shared.database_conn.database_client import create_tables

# ==================


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/api")
app.include_router(healthcheck_router, prefix="/api")

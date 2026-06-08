from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.auth.presentation.routers.v1.auth_router import router as auth_router
from app.modules.cinema.presentation.routers.v1.halls_router import (
    router as hall_router,
)
from app.modules.cinema.presentation.routers.v1.movies_router import (
    router as movie_router,
)
from app.modules.cinema.presentation.routers.v1.screenings_router import (
    router as screening_router,
)
from app.modules.healthcheck.healthcheck import router as healthcheck_router
from app.modules.shared.database_conn.database_client import create_tables

# ==================


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

API = "/api"

app.include_router(auth_router, prefix=API)
app.include_router(healthcheck_router, prefix=API)
app.include_router(movie_router, prefix=API)
app.include_router(hall_router, prefix=API)
app.include_router(screening_router, prefix=API)

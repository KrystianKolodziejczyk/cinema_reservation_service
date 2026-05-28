from fastapi import FastAPI

from app.modules.auth.presentation.routers.v1.auth_router import router as auth_router
from app.modules.healthcheck.healthcheck import router as healthcheck_router

# ==================

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(healthcheck_router, prefix="/api")

if __name__ == "__main__":
    app()

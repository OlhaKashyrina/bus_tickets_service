from fastapi import FastAPI
from app.api.v1.healthcheck import router as health_router

app = FastAPI()

app.include_router(health_router, prefix="/api/v1")
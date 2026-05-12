from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.core.logger import setup_logger
from app.routes.valuate import router as valuate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    logger.info("Starting PropVision AI backend...")

    yield

    logger.info("Shutting down PropVision AI backend...")


setup_logger()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """

    logger.info("Health check endpoint called")

    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }


# =========================
# ROOT
# =========================

@app.get("/")
async def root():
    """
    Root endpoint.
    """

    return {
        "message": "Welcome to PropVision AI"
    }
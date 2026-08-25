"""
FastAPI application entry point.
"""

from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered real estate lead qualification system via WhatsApp",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.ENV,
    }
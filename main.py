"""SpotForge — Main application entrypoint."""

import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.models.schemas import HealthResponse
from app.routes.spots import router as spots_router
from app.routes.voices import router as voices_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("spotforge")

settings = get_settings()

app = FastAPI(
    title="🎙️ SpotForge API",
    description=(
        "AI-Powered 30-Second Audio Ad Generator for Local Businesses & Freelancers. "
        "Built with Google Gemma open-weight models and ElevenLabs voice synthesis for Hacktoberfest 2026."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration for modern web integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure audio and static folders exist
audio_dir = settings.get_audio_dir()
static_dir = Path("static")
static_dir.mkdir(parents=True, exist_ok=True)

# Mount static asset routes
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Register API Routers
app.include_router(spots_router)
app.include_router(voices_router)


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Service health status and underlying model topology."""
    return HealthResponse(
        status="ok",
        version="1.0.0",
        open_weight_model=settings.gemma_model_id,
        voice_engine="ElevenLabs",
        environment=settings.environment,
    )


@app.get("/", tags=["Frontend"])
async def serve_index():
    """Serve single-page frontend application."""
    index_file = Path("static/index.html")
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "app": "SpotForge",
        "description": "AI-Powered Audio Ad Generator",
        "docs": "/docs",
        "health": "/api/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=(settings.environment == "development"),
    )

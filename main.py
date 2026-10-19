"""SpotForge — Main application entrypoint."""

import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.models.schemas import HealthResponse, MusicTrackItem, MusicTracksResponse
from app.routes.spots import router as spots_router
from app.routes.voices import router as voices_router
from app.services.audio_mixer import get_available_music_tracks, is_ffmpeg_available

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
        "Built with Google Gemma open-weight models, ElevenLabs voice synthesis, and FFmpeg audio mixing for Hacktoberfest 2026."
    ),
    version="2.0.0",
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

# Ensure audio, music, and static folders exist
audio_dir = settings.get_audio_dir()
music_dir = settings.get_music_dir()
static_dir = Path("static")
static_dir.mkdir(parents=True, exist_ok=True)

# Mount static asset routes
app.mount("/audio", StaticFiles(directory=str(audio_dir)), name="audio")
app.mount("/music", StaticFiles(directory=str(music_dir)), name="music")
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Register API Routers
app.include_router(spots_router)
app.include_router(voices_router)


@app.get("/api/music", response_model=MusicTracksResponse, tags=["Music"])
async def list_music_tracks() -> MusicTracksResponse:
    """Catalog of royalty-free CC0 background music tracks."""
    tracks = [
        MusicTrackItem(
            id=t["id"],
            name=t["name"],
            description=t["description"],
            filename=t.get("filename"),
        )
        for t in get_available_music_tracks()
    ]
    return MusicTracksResponse(tracks=tracks)


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Service health status and underlying model topology."""
    return HealthResponse(
        status="ok",
        version="2.0.0",
        open_weight_model=settings.gemma_model_id,
        llm_backend=settings.llm_backend,
        voice_engine="ElevenLabs",
        elevenlabs_model=settings.elevenlabs_model,
        ffmpeg_available=is_ffmpeg_available(),
        environment=settings.environment,
    )


@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    """Serve favicon.ico to prevent 404s on browser requests."""
    ico_path = Path("static/favicon.ico")
    if ico_path.exists():
        return FileResponse(ico_path, media_type="image/x-icon")
    return FileResponse(Path("static/favicon.png"), media_type="image/png")


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

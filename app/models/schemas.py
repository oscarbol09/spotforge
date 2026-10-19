"""Pydantic request and response schemas for SpotForge API (v2)."""

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class SpotGenerateRequest(BaseModel):
    """Payload to generate a new commercial audio advertisement."""

    business_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name of the business or brand",
        examples=["Don Mario's Pizzeria"],
    )
    business_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Commercial category or niche",
        examples=["Artisanal Italian Restaurant"],
    )
    offer: str = Field(
        ...,
        min_length=3,
        max_length=250,
        description="Core promotion or compelling offer",
        examples=["2-for-1 on large family pizzas every Tuesday with free delivery"],
    )
    call_to_action: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description="Clear call to action for the listener",
        examples=["Call 555-0199 or order via WhatsApp today"],
    )
    tone: str = Field(
        default="energético",
        description="Commercial tone (energético, cálido, profesional, divertido, urgente)",
        examples=["energético"],
    )
    language: str = Field(
        default="en",
        description="Language code: 'en' for English, 'es' for Spanish",
        examples=["en"],
    )
    duration_seconds: int = Field(
        default=30,
        ge=10,
        le=90,
        description="Target duration of the ad spot in seconds (10 to 90)",
        examples=[30],
    )
    voice_id: str | None = Field(
        default=None,
        description="Optional ElevenLabs voice ID. If omitted, default voice is used.",
    )
    custom_script: str | None = Field(
        default=None,
        max_length=1500,
        description="Optional manual script to synthesize without Gemma regeneration.",
    )
    music: bool = Field(
        default=True,
        description="If True, mixes the voiceover with background music bed using FFmpeg.",
    )
    music_track: str | None = Field(
        default="upbeat_commercial",
        description="Music track ID ('upbeat_commercial', 'chill_acoustic', 'urban_energy', 'none').",
    )


class SpotGenerateResponse(BaseModel):
    """Result payload of a successfully generated audio ad spot (v2)."""

    id: str
    script: str
    audio_url: str
    duration_seconds: float = Field(
        description="Actual measured physical duration of the final MP3 file."
    )
    target_duration_seconds: int = Field(
        description="Target duration requested by the user."
    )
    word_count: int
    characters_used: int = Field(
        description="Characters consumed in ElevenLabs for this spot."
    )
    model_used: str
    voice_used: str
    music_used: str | None = None
    warnings: list[str] = Field(
        default_factory=list,
        description="Non-blocking warnings generated during audio processing.",
    )
    file_size_bytes: int
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class VoiceItem(BaseModel):
    """Details of a single available ElevenLabs voice."""

    voice_id: str
    name: str
    category: str = "commercial"
    description: str = ""
    preview_url: str = ""
    labels: dict[str, str] = Field(default_factory=dict)


class VoicesResponse(BaseModel):
    """List of available voices response."""

    voices: list[VoiceItem]


class MusicTrackItem(BaseModel):
    """Catalog entry for a royalty-free background music bed."""

    id: str
    name: str
    description: str
    filename: str | None = None


class MusicTracksResponse(BaseModel):
    """List of available music beds."""

    tracks: list[MusicTrackItem]


class HealthResponse(BaseModel):
    """Health status and configuration overview."""

    status: str
    version: str
    open_weight_model: str
    llm_backend: str
    voice_engine: str
    elevenlabs_model: str
    ffmpeg_available: bool
    environment: str

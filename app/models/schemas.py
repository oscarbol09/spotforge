"""Pydantic request and response schemas for SpotForge API (v2)."""

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class SpotGenerateRequest(BaseModel):
    """Payload to generate a new audio advertisement."""

    business_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del negocio o marca",
        examples=["Pizzería Don Mario"],
    )
    business_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Categoría o giro comercial",
        examples=["restaurante"],
    )
    offer: str = Field(
        ...,
        min_length=3,
        max_length=250,
        description="Oferta principal o promoción atractiva",
        examples=["2x1 en pizzas familiares todos los martes"],
    )
    call_to_action: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description="Llamada a la acción clara para el cliente",
        examples=["Llama al 555-1234 o pide por WhatsApp"],
    )
    tone: str = Field(
        default="energético",
        description="Tono comunicacional (energético, cálido, profesional, divertido, urgente)",
        examples=["energético"],
    )
    language: str = Field(
        default="es",
        description="Código de idioma: 'es' para español, 'en' para inglés",
        examples=["es"],
    )
    duration_seconds: int = Field(
        default=30,
        ge=10,
        le=90,
        description="Duración objetivo del spot en segundos (10 a 90)",
        examples=[30],
    )
    voice_id: str | None = Field(
        default=None,
        description="ID opcional de la voz de ElevenLabs. Si no se indica, usa la voz predeterminada.",
    )
    custom_script: str | None = Field(
        default=None,
        description="Guión manual opcional para sintetizar sin regenerar con Gemma.",
    )
    music: bool = Field(
        default=True,
        description="Si es True, mezcla la voz con una cama musical de fondo usando FFmpeg.",
    )
    music_track: str | None = Field(
        default="upbeat_commercial",
        description="ID de la pista musical ('upbeat_commercial', 'chill_acoustic', 'urban_energy', 'none').",
    )


class SpotGenerateResponse(BaseModel):
    """Result payload of a successfully generated audio ad spot (v2)."""

    id: str
    script: str
    audio_url: str
    duration_seconds: float = Field(
        description="Duración real medida del archivo MP3 final."
    )
    target_duration_seconds: int = Field(
        description="Duración objetivo solicitada por el usuario."
    )
    word_count: int
    characters_used: int = Field(
        description="Caracteres consumidos en ElevenLabs para este spot."
    )
    model_used: str
    voice_used: str
    music_used: str | None = None
    warnings: list[str] = Field(
        default_factory=list,
        description="Avisos no bloqueantes generados durante el procesamiento.",
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

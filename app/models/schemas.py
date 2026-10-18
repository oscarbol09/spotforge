"""Pydantic request and response schemas for SpotForge API."""

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


class SpotGenerateResponse(BaseModel):
    """Result payload of a successfully generated audio ad spot."""

    id: str
    script: str
    audio_url: str
    duration_seconds: float
    word_count: int
    model_used: str
    voice_used: str
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


class HealthResponse(BaseModel):
    """Health status and configuration overview."""

    status: str
    version: str
    open_weight_model: str
    voice_engine: str
    environment: str

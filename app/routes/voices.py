"""Route handlers for voice catalog management."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import VoiceItem, VoicesResponse
from app.services.voice_synth import VoiceSynthService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/voices", tags=["Voices"])

_voice_synth_service: VoiceSynthService | None = None


def get_voice_synth_service() -> VoiceSynthService:
    """Dependency provider for VoiceSynthService."""
    global _voice_synth_service
    if _voice_synth_service is None:
        _voice_synth_service = VoiceSynthService()
    return _voice_synth_service


@router.get("", response_model=VoicesResponse)
async def list_available_voices(
    service: VoiceSynthService = Depends(get_voice_synth_service),
) -> VoicesResponse:
    """Retrieve catalog of high-conversion commercial voices."""
    try:
        raw_voices = service.list_voices()
        voice_items = [
            VoiceItem(
                voice_id=v.voice_id,
                name=v.name,
                category=v.category,
                description=v.description,
                preview_url=v.preview_url,
                labels=v.labels,
            )
            for v in raw_voices
        ]
        return VoicesResponse(voices=voice_items)
    except Exception as exc:
        logger.error("Failed to list voices: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudieron cargar las voces de ElevenLabs: {exc}",
        ) from exc

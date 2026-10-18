"""Route handlers for audio ad spot generation."""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import SpotGenerateRequest, SpotGenerateResponse
from app.prompts.ad_copywriter import calculate_estimated_duration
from app.services.copywriter import CopywriterService, clean_script
from app.services.voice_synth import VoiceSynthService, VoiceSynthesisError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/generate", tags=["Spots"])

_copywriter_service: CopywriterService | None = None
_voice_synth_service: VoiceSynthService | None = None


def get_copywriter_service() -> CopywriterService:
    """Dependency provider for CopywriterService."""
    global _copywriter_service
    if _copywriter_service is None:
        _copywriter_service = CopywriterService()
    return _copywriter_service


def get_voice_synth_service() -> VoiceSynthService:
    """Dependency provider for VoiceSynthService."""
    global _voice_synth_service
    if _voice_synth_service is None:
        _voice_synth_service = VoiceSynthService()
    return _voice_synth_service


@router.post("", response_model=SpotGenerateResponse)
async def generate_audio_spot(
    request: SpotGenerateRequest,
    copywriter: CopywriterService = Depends(get_copywriter_service),
    voice_synth: VoiceSynthService = Depends(get_voice_synth_service),
) -> SpotGenerateResponse:
    """Generate a broadcast-ready audio ad using Gemma 4 copywriting and ElevenLabs voice synthesis."""
    spot_id = f"spot_{uuid.uuid4().hex[:10]}"
    model_used = "custom_script"

    # Step 1: Copywriting (Gemma 4 or manual custom script)
    if request.custom_script and request.custom_script.strip():
        logger.info("Using user-provided custom script for spot %s", spot_id)
        script_text = clean_script(request.custom_script)
        words = [w for w in script_text.split() if w.strip()]
        word_count = len(words)
        duration_est = calculate_estimated_duration(script_text, request.language)
    else:
        try:
            logger.info("Generating copy with Gemma for %s (%s)", request.business_name, spot_id)
            script_result = copywriter.generate_script(
                business_name=request.business_name,
                business_type=request.business_type,
                offer=request.offer,
                call_to_action=request.call_to_action,
                tone=request.tone,
                language=request.language,
                duration_seconds=request.duration_seconds,
            )
            script_text = script_result.script
            word_count = script_result.word_count
            duration_est = script_result.estimated_duration_seconds
            model_used = script_result.model
        except Exception as exc:
            logger.error("Gemma script generation failed: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Fallo en la generación de guión con modelo Gemma: {exc}",
            ) from exc

    # Step 2: Voice Synthesis (ElevenLabs)
    try:
        output_filename = f"{spot_id}.mp3"
        logger.info("Synthesizing voice with ElevenLabs for spot %s", spot_id)
        audio_result = voice_synth.synthesize_speech(
            text=script_text,
            voice_id=request.voice_id,
            output_filename=output_filename,
        )
    except VoiceSynthesisError as exc:
        logger.error("ElevenLabs synthesis error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Fallo en síntesis de audio con ElevenLabs: {exc}",
        ) from exc
    except Exception as exc:
        logger.error("Unexpected synthesis error: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al procesar el audio: {exc}",
        ) from exc

    return SpotGenerateResponse(
        id=spot_id,
        script=script_text,
        audio_url=audio_result.relative_url,
        duration_seconds=duration_est,
        word_count=word_count,
        model_used=model_used,
        voice_used=audio_result.voice_id,
        file_size_bytes=audio_result.file_size_bytes,
    )

"""Route handlers for audio ad spot generation with real duration control and music mixing (v2)."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.models.schemas import SpotGenerateRequest, SpotGenerateResponse
from app.services.audio_mixer import mix_voice_and_music
from app.services.copywriter import CopywriterService, clean_script
from app.services.storage import (
    cleanup_old_audio,
    generate_secure_spot_id,
    measure_mp3_duration,
)
from app.services.text_normalizer import normalize_for_tts
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
    settings: Settings = Depends(get_settings),
) -> SpotGenerateResponse:
    """Generate a commercial ad spot using Gemma open-weights, text normalizer, ElevenLabs, and FFmpeg."""
    spot_id = generate_secure_spot_id()
    warnings: list[str] = []
    audio_dir = settings.get_audio_dir()

    # R8: Periodic TTL cleanup of expired audio files
    try:
        cleanup_old_audio(audio_dir, ttl_hours=settings.audio_ttl_hours)
    except Exception as exc:
        logger.warning("Error during TTL audio cleanup: %s", exc)

    # Step 1: Copywriting (Gemma or manual custom script)
    model_used = "custom_script"
    raw_script_text = ""

    if request.custom_script and request.custom_script.strip():
        logger.info("Using user-provided custom script for spot %s", spot_id)
        raw_script_text = clean_script(request.custom_script)
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
            raw_script_text = script_result.script
            model_used = script_result.model
        except Exception as exc:
            logger.error("Gemma script generation failed: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Fallo en la generación de guión con modelo Gemma: {exc}",
            ) from exc

    # Step 2: R3 Deterministic Normalization for TTS
    tts_spoken_text = normalize_for_tts(raw_script_text, language=request.language)
    words = [w for w in raw_script_text.split() if w.strip()]
    word_count = len(words)

    # Step 3: Voice Synthesis with ElevenLabs
    voice_filename = f"voice_{spot_id}.mp3"
    try:
        logger.info("Synthesizing voice with ElevenLabs for spot %s", spot_id)
        audio_result = voice_synth.synthesize_speech(
            text=tts_spoken_text,
            voice_id=request.voice_id,
            output_filename=voice_filename,
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

    voice_path = audio_result.file_path
    measured_duration = measure_mp3_duration(voice_path)

    # Step 4: R4 Duration Control with Real MP3 Length
    # If duration exceeds target + 3s, retry ONCE with reduced word target
    if measured_duration > (request.duration_seconds + 3.0) and not request.custom_script:
        logger.info(
            "Measured duration (%.1fs) exceeds target (%ds + 3s). Attempting 1 adaptive retry...",
            measured_duration,
            request.duration_seconds,
        )
        try:
            # Proportional reduction
            reduction_ratio = request.duration_seconds / measured_duration
            reduced_word_target = max(15, int(word_count * reduction_ratio))

            retry_result = copywriter.generate_script(
                business_name=request.business_name,
                business_type=request.business_type,
                offer=request.offer,
                call_to_action=request.call_to_action,
                tone=request.tone,
                language=request.language,
                duration_seconds=request.duration_seconds,
                target_words_override=reduced_word_target,
            )
            raw_script_text = retry_result.script
            tts_spoken_text = normalize_for_tts(raw_script_text, language=request.language)
            words = [w for w in raw_script_text.split() if w.strip()]
            word_count = len(words)

            # Re-synthesize
            audio_result = voice_synth.synthesize_speech(
                text=tts_spoken_text,
                voice_id=request.voice_id,
                output_filename=voice_filename,
            )
            voice_path = audio_result.file_path
            measured_duration = measure_mp3_duration(voice_path)

            if measured_duration > (request.duration_seconds + 3.0):
                warnings.append(
                    f"El audio dura {measured_duration}s tras reintento, superando el objetivo de {request.duration_seconds}s."
                )
        except Exception as retry_err:
            logger.warning("Adaptive duration retry failed: %s. Keeping first audio take.", retry_err)
            warnings.append("No se pudo completar el reintento de ajuste de duración.")

    # Step 5: Audio Mixing (FFmpeg background music bed)
    final_audio_path = voice_path
    final_filename = voice_path.name
    music_used = None

    if request.music and request.music_track and request.music_track != "none" and settings.enable_music_mixing:
        mixed_filename = f"{spot_id}.mp3"
        mixed_target_path = audio_dir / mixed_filename
        mixed_path, mix_warnings = mix_voice_and_music(
            voice_path=voice_path,
            music_track_id=request.music_track,
            output_path=mixed_target_path,
            music_dir=settings.get_music_dir(),
        )
        warnings.extend(mix_warnings)
        if mixed_path.exists() and mixed_path != voice_path:
            final_audio_path = mixed_path
            final_filename = mixed_filename
            music_used = request.music_track
            # Remove intermediate raw voice file
            try:
                voice_path.unlink(missing_ok=True)
            except OSError:
                pass

    final_duration = measure_mp3_duration(final_audio_path)
    file_size = final_audio_path.stat().st_size if final_audio_path.exists() else audio_result.file_size_bytes

    return SpotGenerateResponse(
        id=spot_id,
        script=raw_script_text,
        audio_url=f"/audio/{final_filename}",
        duration_seconds=final_duration,
        target_duration_seconds=request.duration_seconds,
        word_count=word_count,
        characters_used=audio_result.characters_used,
        model_used=model_used,
        voice_used=audio_result.voice_name or audio_result.voice_id,
        music_used=music_used,
        warnings=warnings,
        file_size_bytes=file_size,
    )

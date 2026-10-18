"""Voice synthesis service powered by ElevenLabs text-to-speech API."""

import logging
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)


class VoiceSynthesisError(Exception):
    """Raised when ElevenLabs voice synthesis fails."""
    pass


@dataclass
class VoiceInfo:
    """Metadata representing an available voice."""

    voice_id: str
    name: str
    category: str = "commercial"
    description: str = ""
    preview_url: str = ""
    labels: dict[str, str] = field(default_factory=dict)


@dataclass
class AudioFileResult:
    """Details of synthesized audio file stored on disk."""

    file_path: Path
    filename: str
    relative_url: str
    voice_id: str
    file_size_bytes: int


# Curated commercial voices with proven high conversion for radio and digital ads
CURATED_COMMERCIAL_VOICES = [
    VoiceInfo(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        name="Rachel — Comercial & Confidente",
        category="professional",
        description="Voz femenina profesional, clara, confiada y persuasiva. Ideal para marcas premium y servicios.",
        labels={"gender": "female", "accent": "american", "style": "commercial"},
    ),
    VoiceInfo(
        voice_id="pNInz6obpgDQGcFmaJgB",
        name="Adam — Corporativo & Cálido",
        category="professional",
        description="Voz masculina profunda, cálida y autorizada. Perfecta para cuñas radiales y anuncios institucionales.",
        labels={"gender": "male", "accent": "american", "style": "narration"},
    ),
    VoiceInfo(
        voice_id="ErXwobaYiN019PkySvjV",
        name="Antoni — Enérgico & Comercial",
        category="commercial",
        description="Voz masculina dinámica, rápida y llamativa. Excelente para promociones, ofertas flash y comida rápida.",
        labels={"gender": "male", "accent": "american", "style": "promo"},
    ),
    VoiceInfo(
        voice_id="EXAVITQu4vr4xnSDxMaL",
        name="Bella — Fresca & Cercana",
        category="commercial",
        description="Voz femenina juvenil, fresca y amigable. Ideal para cafeterías, boutiques y redes sociales.",
        labels={"gender": "female", "accent": "american", "style": "casual"},
    ),
    VoiceInfo(
        voice_id="TxGEqnHWrfWFTfGW9XjX",
        name="Josh — Amigable & Conversacional",
        category="conversational",
        description="Voz masculina joven y natural. Perfecta para testimoniales y recomendaciones directas.",
        labels={"gender": "male", "accent": "american", "style": "conversational"},
    ),
]


class VoiceSynthService:
    """Service to synthesize commercial audio using ElevenLabs API."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

        if not self.settings.elevenlabs_api_key:
            raise ValueError(
                "ELEVENLABS_API_KEY no está configurada. "
                "Obtén tu API key en https://elevenlabs.io/ e indícala en el archivo .env"
            )

        self._client = ElevenLabs(api_key=self.settings.elevenlabs_api_key)

    def list_voices(self) -> list[VoiceInfo]:
        """List available voices, merging ElevenLabs API catalog with curated presets."""
        try:
            response = self._client.voices.get_all()
            api_voices = []
            for v in response.voices:
                api_voices.append(
                    VoiceInfo(
                        voice_id=v.voice_id,
                        name=v.name,
                        category=getattr(v, "category", "general"),
                        preview_url=getattr(v, "preview_url", "") or "",
                        labels=getattr(v, "labels", {}) or {},
                    )
                )
            if api_voices:
                return api_voices
        except Exception as exc:
            logger.warning("Could not fetch remote voices from ElevenLabs: %s. Using curated list.", exc)

        return CURATED_COMMERCIAL_VOICES

    def synthesize_speech(
        self,
        text: str,
        voice_id: str | None = None,
        output_filename: str | None = None,
        stability: float = 0.45,
        similarity_boost: float = 0.75,
        model_id: str = "eleven_multilingual_v2",
    ) -> AudioFileResult:
        """Synthesize text into a broadcast-ready MP3 file.

        Args:
            text: Ad copy text to be spoken.
            voice_id: ElevenLabs voice ID (falls back to default).
            output_filename: Optional filename (generates random UUID if omitted).
            stability: Voice stability (lower = more emotional/commercial dynamism).
            similarity_boost: Voice clarity and speaker match boost.
            model_id: Model to use (eleven_multilingual_v2 recommended for highest quality).

        Returns:
            AudioFileResult with file path, url, and size.

        Raises:
            ValueError: If input text is empty.
            VoiceSynthesisError: If ElevenLabs API returns an error.
        """
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("El texto para síntesis no puede estar vacío.")

        target_voice = voice_id or self.settings.default_voice_id

        if not output_filename:
            output_filename = f"spot_{uuid.uuid4().hex[:12]}.mp3"

        out_dir = self.settings.get_audio_dir()
        target_path = out_dir / output_filename

        try:
            logger.info("Synthesizing speech with voice %s (model: %s)", target_voice, model_id)
            audio_stream = self._client.text_to_speech.convert(
                voice_id=target_voice,
                text=clean_text,
                model_id=model_id,
                output_format="mp3_44100_128",
                voice_settings=VoiceSettings(
                    stability=stability,
                    similarity_boost=similarity_boost,
                    style=0.0,
                    use_speaker_boost=True,
                ),
            )

            total_bytes = 0
            with open(target_path, "wb") as f:
                for chunk in audio_stream:
                    if chunk:
                        f.write(chunk)
                        total_bytes += len(chunk)

            logger.info("Audio saved to %s (%d bytes)", target_path, total_bytes)

            relative_url = f"/audio/{output_filename}"

            return AudioFileResult(
                file_path=target_path,
                filename=output_filename,
                relative_url=relative_url,
                voice_id=target_voice,
                file_size_bytes=total_bytes,
            )

        except Exception as exc:
            logger.error("ElevenLabs speech synthesis failed: %s", exc)
            # Remove partial or corrupt file if created
            if target_path.exists():
                try:
                    target_path.unlink()
                except OSError:
                    pass
            raise VoiceSynthesisError(f"Error en síntesis de voz con ElevenLabs: {exc}") from exc

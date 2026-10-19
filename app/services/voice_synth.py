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
    characters_used: int = 0
    voice_name: str = ""


# Curated commercial voices verified against ElevenLabs Multilingual v2 catalog
CURATED_COMMERCIAL_VOICES = [
    VoiceInfo(
        voice_id="CwhRBWXzGAHq8TQ4Fs17",
        name="Roger — Casual & Resonante",
        category="commercial",
        description="Voz masculina casual, resonante y confiable. Excelente para promociones locales y cuñas de radio.",
        labels={"gender": "male", "accent": "american", "style": "commercial"},
    ),
    VoiceInfo(
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        name="George — Cálido & Storyteller",
        category="professional",
        description="Voz masculina cálida, cautivadora y narrativa. Ideal para marcas tradicionales, restaurantes y servicios.",
        labels={"gender": "male", "accent": "british", "style": "storytelling"},
    ),
    VoiceInfo(
        voice_id="EXAVITQu4vr4xnSDxMaL",
        name="Sarah — Profesional & Confiable",
        category="professional",
        description="Voz femenina madura, clara, tranquilizadora y segura. Perfecta para servicios médicos y finanzas.",
        labels={"gender": "female", "accent": "american", "style": "narration"},
    ),
    VoiceInfo(
        voice_id="TX3LPaxmHKxFdv7VOQHJ",
        name="Liam — Enérgico & Dinámico",
        category="commercial",
        description="Voz masculina joven, enérgica y rápida. Excelente para redes sociales, ofertas flash y comida rápida.",
        labels={"gender": "male", "accent": "american", "style": "promo"},
    ),
    VoiceInfo(
        voice_id="IKne3meq5aSn9XLyUdCD",
        name="Charlie — Profundo & Seguro",
        category="commercial",
        description="Voz masculina profunda, segura y enérgica. Gran impacto para talleres mecánicos y barberías.",
        labels={"gender": "male", "accent": "australian", "style": "commercial"},
    ),
    VoiceInfo(
        voice_id="Xb7hH8MSUJpSbSDYk0k2",
        name="Alice — Clara & Cercana",
        category="conversational",
        description="Voz femenina clara, directa y atractiva. Ideal para tutoriales, cafeterías y boutiques.",
        labels={"gender": "female", "accent": "british", "style": "conversational"},
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
        model_id: str | None = None,
    ) -> AudioFileResult:
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("El texto para síntesis no puede estar vacío.")

        target_voice = voice_id or self.settings.default_voice_id
        target_model = model_id or self.settings.elevenlabs_model

        if not output_filename:
            output_filename = f"spot_{uuid.uuid4().hex[:12]}.mp3"

        out_dir = self.settings.get_audio_dir()
        target_path = out_dir / output_filename

        try:
            logger.info("Synthesizing speech with voice %s (model: %s)", target_voice, target_model)
            audio_stream = self._client.text_to_speech.convert(
                voice_id=target_voice,
                text=clean_text,
                model_id=target_model,
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

            # Attempt to resolve human-readable voice name
            voice_name = target_voice
            for v in self.list_voices():
                if v.voice_id == target_voice:
                    voice_name = v.name
                    break

            return AudioFileResult(
                file_path=target_path,
                filename=output_filename,
                relative_url=relative_url,
                voice_id=target_voice,
                file_size_bytes=total_bytes,
                characters_used=len(clean_text),
                voice_name=voice_name,
            )

        except Exception as exc:
            logger.error("ElevenLabs speech synthesis failed: %s", exc)
            if target_path.exists():
                try:
                    target_path.unlink()
                except OSError:
                    pass
            raise VoiceSynthesisError(f"Error en síntesis de voz con ElevenLabs: {exc}") from exc

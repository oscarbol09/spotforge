"""Audio mixer service using FFmpeg to blend voiceovers with background musical beds."""

import logging
import subprocess
from pathlib import Path

from app.services.storage import measure_mp3_duration

logger = logging.getLogger(__name__)

AVAILABLE_TRACKS = [
    {
        "id": "none",
        "name": "Sin música (Solo voz limpia)",
        "description": "Voz profesional aislada sin instrumentos de fondo",
        "filename": None,
    },
    {
        "id": "upbeat_commercial",
        "name": "⚡ Upbeat Commercial",
        "description": "Acordes brillantes y alegres (110 BPM), ideal para comercio, comida y ofertas",
        "filename": "upbeat_commercial.mp3",
    },
    {
        "id": "chill_acoustic",
        "name": "☕ Chill Acoustic",
        "description": "Piano y acordes cálidos relajantes (75 BPM), ideal para cafeterías, spas y boutiques",
        "filename": "chill_acoustic.mp3",
    },
    {
        "id": "urban_energy",
        "name": "🔥 Urban Energy",
        "description": "Pulso rítmico moderno y dinámico (120 BPM), ideal para deportes, barberías y tecnología",
        "filename": "urban_energy.mp3",
    },
]


def is_ffmpeg_available() -> bool:
    """Verify if FFmpeg binary is installed and executable in PATH."""
    try:
        res = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return res.returncode == 0
    except Exception:
        return False


def get_available_music_tracks() -> list[dict]:
    """Retrieve catalog of background music tracks."""
    return AVAILABLE_TRACKS


def mix_voice_and_music(
    voice_path: Path,
    music_track_id: str | None,
    output_path: Path,
    music_dir: Path | str = "static/music",
    music_volume: float = 0.15,
    fade_duration: float = 2.0,
) -> tuple[Path, list[str]]:
    """Blend voiceover audio with looped background music using FFmpeg.

    Gracefully degrades to raw voiceover if FFmpeg is unavailable or if mixing fails.

    Returns:
        tuple[Path, list[str]]: (final_audio_path, warnings_list)
    """
    warnings: list[str] = []

    # Case 1: No music requested or 'none'
    if not music_track_id or music_track_id == "none":
        return voice_path, []

    # Check track existence
    music_directory = Path(music_dir)
    track_meta = next((t for t in AVAILABLE_TRACKS if t["id"] == music_track_id), None)
    if not track_meta or not track_meta["filename"]:
        warnings.append(f"Pista musical '{music_track_id}' no reconocida. Se utilizó solo la voz.")
        return voice_path, warnings

    music_file = music_directory / track_meta["filename"]
    if not music_file.exists():
        warnings.append(f"Archivo musical '{music_file.name}' no encontrado. Se utilizó solo la voz.")
        return voice_path, warnings

    # Check FFmpeg availability
    if not is_ffmpeg_available():
        logger.warning("FFmpeg is not available in PATH. Degraded to voice only.")
        warnings.append("FFmpeg no está disponible en el servidor: se devolvió solo la voz sin música.")
        return voice_path, warnings

    voice_duration = measure_mp3_duration(voice_path)
    if voice_duration <= 0:
        voice_duration = 30.0

    fade_start = max(0.5, round(voice_duration - fade_duration, 1))

    # FFmpeg command: loop music infinitely, lower volume to 15%, mix inputs, truncate to voice length, fade out
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(voice_path),
        "-stream_loop",
        "-1",
        "-i",
        str(music_file),
        "-filter_complex",
        (
            f"[1:a]volume={music_volume:.2f}[m];"
            f"[0:a][m]amix=inputs=2:duration=first:dropout_transition=2,"
            f"afade=t=out:st={fade_start}:d={fade_duration}"
        ),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "128k",
        str(output_path),
    ]

    try:
        logger.info("Mixing voice (%s) with music (%s) via FFmpeg...", voice_path.name, music_file.name)
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=15.0,
        )
        if process.returncode != 0:
            stderr_msg = process.stderr.decode(errors="ignore")[:200]
            logger.warning("FFmpeg mixing exited with code %d: %s", process.returncode, stderr_msg)
            warnings.append(f"Fallo al procesar la mezcla de audio: {stderr_msg}. Se devolvió solo la voz.")
            return voice_path, warnings

        if output_path.exists() and output_path.stat().st_size > 1000:
            logger.info("Audio mix completed successfully: %s (%d bytes)", output_path.name, output_path.stat().st_size)
            return output_path, warnings
        else:
            warnings.append("El archivo de mezcla no se generó correctamente. Se devolvió solo la voz.")
            return voice_path, warnings

    except Exception as exc:
        logger.error("Exception during FFmpeg audio mixing: %s", exc)
        warnings.append(f"Error inesperado en mezcla con FFmpeg: {exc}. Se devolvió solo la voz.")
        return voice_path, warnings

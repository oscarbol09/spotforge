"""Storage and file lifecycle management with secure naming and TTL cleanup."""

import logging
import time
import uuid
from pathlib import Path
from mutagen.mp3 import MP3

logger = logging.getLogger(__name__)


def generate_secure_spot_id() -> str:
    """Generate a collision-resistant, cryptographically secure identifier for a spot."""
    return f"spot_{uuid.uuid4().hex[:12]}"


def measure_mp3_duration(filepath: Path | str) -> float:
    """Measure exact playback duration of an MP3 file using mutagen.

    Returns:
        Duration in seconds rounded to 1 decimal place.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    try:
        audio = MP3(str(path))
        return round(audio.info.length, 1)
    except Exception as exc:
        logger.warning("Could not measure exact MP3 length for %s: %s", path, exc)
        return 0.0


def cleanup_old_audio(audio_dir: Path | str, ttl_hours: int = 24) -> int:
    """Purge temporary generated audio files older than ttl_hours.

    Protects .gitkeep and permanent demo files (starting with 'demo_').

    Returns:
        Count of deleted files.
    """
    directory = Path(audio_dir)
    if not directory.exists() or not directory.is_dir():
        return 0

    now = time.time()
    cutoff = now - (ttl_hours * 3600)
    deleted_count = 0

    for item in directory.glob("*.mp3"):
        # Never delete permanent demo showcases or gitkeep
        if item.name.startswith("demo_") or item.name == ".gitkeep":
            continue

        try:
            stat = item.stat()
            if stat.st_mtime < cutoff:
                item.unlink(missing_ok=True)
                deleted_count += 1
                logger.info("Purged expired audio spot: %s (age > %d hours)", item.name, ttl_hours)
        except OSError as err:
            logger.warning("Failed to remove expired file %s: %s", item.name, err)

    return deleted_count

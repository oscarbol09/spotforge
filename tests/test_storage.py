"""Unit tests for storage lifecycle, ID generation, and TTL cleanup."""

import os
import time
from pathlib import Path
from app.services.storage import cleanup_old_audio, generate_secure_spot_id


def test_generate_secure_spot_id_format():
    spot_id = generate_secure_spot_id()
    assert spot_id.startswith("spot_")
    assert len(spot_id) == 17  # spot_ + 12 hex chars


def test_cleanup_old_audio_deletes_expired_and_preserves_demos(tmp_path: Path):
    audio_dir = tmp_path / "audio"
    audio_dir.mkdir()

    # 1. Old temporary audio (>25 hours old)
    old_file = audio_dir / "spot_old12345.mp3"
    old_file.write_bytes(b"dummy mp3 data")
    old_time = time.time() - (25 * 3600)
    os.utime(old_file, (old_time, old_time))

    # 2. Fresh temporary audio (1 hour old)
    fresh_file = audio_dir / "spot_fresh123.mp3"
    fresh_file.write_bytes(b"dummy mp3 data")
    fresh_time = time.time() - (1 * 3600)
    os.utime(fresh_file, (fresh_time, fresh_time))

    # 3. Permanent demo showcase (even if old)
    demo_file = audio_dir / "demo_pizzeria.mp3"
    demo_file.write_bytes(b"permanent demo data")
    os.utime(demo_file, (old_time, old_time))

    # Run cleanup with 24 hours TTL
    deleted_count = cleanup_old_audio(audio_dir, ttl_hours=24)

    assert deleted_count == 1
    assert not old_file.exists()
    assert fresh_file.exists()
    assert demo_file.exists()

"""Integration and contract tests for FastAPI REST endpoints using dependency overrides (v2)."""

import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from fastapi.testclient import TestClient

from app.services.copywriter import AdScriptResult
from app.services.voice_synth import AudioFileResult, VoiceInfo
from app.routes.spots import get_copywriter_service, get_voice_synth_service as get_spot_voice_service
from app.routes.voices import get_voice_synth_service as get_voice_catalog_service
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    """Ensure clean dependency overrides for every test."""
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "gemma" in data["open_weight_model"].lower()
    assert data["voice_engine"] == "ElevenLabs"
    assert "ffmpeg_available" in data


def test_favicon_endpoint():
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert "image" in response.headers.get("content-type", "")


def test_get_music_tracks_endpoint():
    response = client.get("/api/music")
    assert response.status_code == 200
    data = response.json()
    assert "tracks" in data
    assert len(data["tracks"]) >= 3
    track_ids = [t["id"] for t in data["tracks"]]
    assert "upbeat_commercial" in track_ids
    assert "chill_acoustic" in track_ids
    assert "urban_energy" in track_ids


def test_get_voices_endpoint():
    mock_voices = [
        VoiceInfo(
            voice_id="v-1",
            name="Rachel Commercial",
            category="professional",
            description="Clear commercial tone",
            preview_url="https://audio.url/test.mp3",
            labels={"gender": "female"},
        )
    ]
    mock_service = MagicMock()
    mock_service.list_voices.return_value = mock_voices
    app.dependency_overrides[get_voice_catalog_service] = lambda: mock_service

    response = client.get("/api/voices")
    assert response.status_code == 200
    data = response.json()
    assert "voices" in data
    assert len(data["voices"]) >= 1
    assert data["voices"][0]["voice_id"] == "v-1"


def test_post_generate_spot_successful():
    fake_script_result = AdScriptResult(
        script="¿Buscas la mejor pizza? En Pizzería Don Mario disfruta dos por uno.",
        word_count=10,
        estimated_duration_seconds=4.0,
        model="gemma-4-26b-a4b-it",
    )
    fake_audio_result = AudioFileResult(
        file_path=Path("static/audio/test_spot.mp3"),
        filename="test_spot.mp3",
        relative_url="/audio/test_spot.mp3",
        voice_id="voice-123",
        voice_name="Rachel",
        file_size_bytes=45000,
        characters_used=72,
    )

    mock_copy_service = MagicMock()
    mock_copy_service.generate_script.return_value = fake_script_result
    mock_voice_service = MagicMock()
    mock_voice_service.synthesize_speech.return_value = fake_audio_result

    app.dependency_overrides[get_copywriter_service] = lambda: mock_copy_service
    app.dependency_overrides[get_spot_voice_service] = lambda: mock_voice_service

    payload = {
        "business_name": "Pizzería Don Mario",
        "business_type": "restaurante",
        "offer": "2x1 en pizzas familiares",
        "call_to_action": "Llama al 555-1234",
        "tone": "energético",
        "language": "es",
        "duration_seconds": 30,
        "music": False,
    }

    with patch("app.routes.spots.measure_mp3_duration", return_value=29.4):
        response = client.post("/api/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["script"] == fake_script_result.script
        assert data["audio_url"] == "/audio/test_spot.mp3"
        assert data["word_count"] == len(fake_script_result.script.split())
        assert data["duration_seconds"] == 29.4
        assert data["target_duration_seconds"] == 30
        assert data["characters_used"] == 72
        assert data["model_used"] == "gemma-4-26b-a4b-it"


def test_post_generate_with_custom_script_bypasses_gemma():
    fake_audio_result = AudioFileResult(
        file_path=Path("static/audio/custom.mp3"),
        filename="custom.mp3",
        relative_url="/audio/custom.mp3",
        voice_id="voice-custom",
        voice_name="Custom Voice",
        file_size_bytes=30000,
        characters_used=50,
    )

    mock_copy_service = MagicMock()
    mock_voice_service = MagicMock()
    mock_voice_service.synthesize_speech.return_value = fake_audio_result

    app.dependency_overrides[get_copywriter_service] = lambda: mock_copy_service
    app.dependency_overrides[get_spot_voice_service] = lambda: mock_voice_service

    payload = {
        "business_name": "Taller López",
        "business_type": "mecánica",
        "offer": "Afinación al 50%",
        "call_to_action": "Agenda hoy",
        "custom_script": "Guión editado manualmente por el usuario listo para locución.",
        "music": False,
    }
    with patch("app.routes.spots.measure_mp3_duration", return_value=15.0):
        response = client.post("/api/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["script"] == "Guión editado manualmente por el usuario listo para locución."
        mock_copy_service.generate_script.assert_not_called()


def test_post_generate_validation_error():
    payload = {
        "business_name": "A",  # too short (< 2 chars)
        "business_type": "taquería",
        "offer": "tacos",
        "call_to_action": "ven",
        "duration_seconds": 5,  # must be >= 10
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 422


def test_post_generate_handles_service_error():
    mock_copy_service = MagicMock()
    mock_copy_service.generate_script.side_effect = Exception("Gemma rate limit")
    mock_voice_service = MagicMock()

    app.dependency_overrides[get_copywriter_service] = lambda: mock_copy_service
    app.dependency_overrides[get_spot_voice_service] = lambda: mock_voice_service

    payload = {
        "business_name": "Café Aroma",
        "business_type": "cafetería",
        "offer": "Café americano gratis con tu dona",
        "call_to_action": "Pasa por el tuyo",
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 502
    assert "Gemma" in response.json()["detail"]


def test_post_generate_custom_script_length_limit():
    """Verify custom_script cannot exceed 1500 chars to protect ElevenLabs quotas."""
    payload = {
        "business_name": "Taller López",
        "business_type": "mecánica",
        "offer": "Afinación al 50%",
        "call_to_action": "Agenda hoy",
        "custom_script": "A" * 1501,
        "music": False,
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 422


def test_get_client_ip_uses_rightmost_forwarded_for():
    """Verify rightmost IP is extracted from X-Forwarded-For to prevent spoofing."""
    from app.routes.spots import get_client_ip
    from unittest.mock import MagicMock

    req = MagicMock()
    req.headers = {"x-forwarded-for": "198.51.100.1, 203.0.113.195"}
    assert get_client_ip(req) == "203.0.113.195"


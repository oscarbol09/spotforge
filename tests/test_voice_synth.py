"""Unit and integration tests for the Voice Synthesis service (ElevenLabs)."""

import pytest
from unittest.mock import MagicMock

from app.config import Settings
from app.services.voice_synth import (
    VoiceSynthService,
    AudioFileResult,
    VoiceSynthesisError,
)


def test_voice_synth_raises_on_missing_api_key():
    settings = Settings(elevenlabs_api_key="")
    with pytest.raises(ValueError, match="ELEVENLABS_API_KEY no está configurada"):
        VoiceSynthService(settings=settings)


def test_voice_synth_raises_on_empty_text(tmp_path):
    settings = Settings(
        elevenlabs_api_key="fake-key",
        audio_output_dir=str(tmp_path),
    )
    service = VoiceSynthService(settings=settings)
    with pytest.raises(ValueError, match="El texto para síntesis no puede estar vacío"):
        service.synthesize_speech(text="   ")


def test_list_voices_curated_or_api(tmp_path):
    settings = Settings(
        elevenlabs_api_key="fake-key",
        audio_output_dir=str(tmp_path),
    )
    service = VoiceSynthService(settings=settings)

    # Mock client.voices.get_all()
    mock_client = MagicMock()
    mock_voice = MagicMock()
    mock_voice.voice_id = "test-voice-123"
    mock_voice.name = "Rachel Commercial"
    mock_voice.category = "premade"
    mock_voice.preview_url = "https://preview.url/voice.mp3"
    mock_voice.labels = {"accent": "american", "gender": "female"}

    mock_client.voices.get_all.return_value = MagicMock(voices=[mock_voice])
    service._client = mock_client

    voices = service.list_voices()
    assert len(voices) >= 1
    assert any(v.voice_id == "test-voice-123" for v in voices)
    assert any(v.name == "Rachel Commercial" for v in voices)


def test_synthesize_speech_successful(tmp_path):
    settings = Settings(
        elevenlabs_api_key="fake-key",
        audio_output_dir=str(tmp_path),
        default_voice_id="voice-abc",
    )
    service = VoiceSynthService(settings=settings)

    mock_client = MagicMock()
    # Generator of fake MP3 audio chunks
    dummy_audio_bytes = [b"ID3\x04\x00\x00", b"\x00\x00\x00#TPE1", b"\x00\x00\x00SpotForge"]
    mock_client.text_to_speech.convert.return_value = dummy_audio_bytes
    service._client = mock_client

    result = service.synthesize_speech(
        text="En Pizzería Don Mario la pizza sabe mejor.",
        voice_id="voice-abc",
        output_filename="test_spot_01.mp3",
    )

    assert isinstance(result, AudioFileResult)
    assert result.filename == "test_spot_01.mp3"
    assert result.voice_id == "voice-abc"
    assert result.file_size_bytes == sum(len(c) for c in dummy_audio_bytes)
    assert result.file_path.exists()

    # Verify parameters sent to ElevenLabs convert
    mock_client.text_to_speech.convert.assert_called_once()
    call_kwargs = mock_client.text_to_speech.convert.call_args.kwargs
    assert call_kwargs["voice_id"] == "voice-abc"
    assert call_kwargs["text"] == "En Pizzería Don Mario la pizza sabe mejor."
    assert "eleven_multilingual_v2" in call_kwargs["model_id"]


def test_synthesize_speech_handles_api_failure(tmp_path):
    settings = Settings(
        elevenlabs_api_key="fake-key",
        audio_output_dir=str(tmp_path),
    )
    service = VoiceSynthService(settings=settings)

    mock_client = MagicMock()
    mock_client.text_to_speech.convert.side_effect = Exception("ElevenLabs Quota Exceeded")
    service._client = mock_client

    with pytest.raises(VoiceSynthesisError, match="Error en síntesis de voz con ElevenLabs"):
        service.synthesize_speech(text="Texto de prueba publicitaria")

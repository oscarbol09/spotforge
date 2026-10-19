"""Configuration settings using Pydantic Settings."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    gemini_api_key: str = ""
    elevenlabs_api_key: str = ""
    gemma_model_id: str = "gemma-4-26b-a4b-it"
    fallback_model_id: str = "gemma-4-31b-it"
    llm_backend: str = "gemini"  # gemini | ollama
    ollama_base_url: str = "http://localhost:11434"
    elevenlabs_model: str = "eleven_multilingual_v2"
    default_voice_id: str = "CwhRBWXzGAHq8TQ4Fs17"  # Roger
    default_language: str = "es"
    port: int = 8000
    host: str = "0.0.0.0"
    environment: str = "development"
    audio_output_dir: str = "static/audio"
    music_dir: str = "static/music"
    audio_ttl_hours: int = 24
    enable_music_mixing: bool = True
    rate_limit_enabled: bool = True
    rate_limit_max_requests: int = 5
    rate_limit_window_seconds: int = 300
    rate_limit_max_global_daily: int = 200

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def get_audio_dir(self) -> Path:
        """Ensure audio output directory exists and return Path object."""
        path = Path(self.audio_output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_music_dir(self) -> Path:
        """Ensure background music directory exists and return Path object."""
        path = Path(self.music_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


_settings_instance: Settings | None = None


def get_settings() -> Settings:
    """Singleton getter for application settings."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
        # Fall back to GEMINI_API_KEY from environment if not set
        if not _settings_instance.gemini_api_key:
            _settings_instance.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        if not _settings_instance.elevenlabs_api_key:
            _settings_instance.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY", "")
    return _settings_instance

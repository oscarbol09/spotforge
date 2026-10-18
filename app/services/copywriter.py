"""Copywriting service supporting interchangeable LLM backends (Gemini API & local Ollama)."""

import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from google import genai
import httpx

from app.config import Settings, get_settings
from app.prompts.ad_copywriter import (
    build_unified_prompt,
    calculate_estimated_duration,
)

logger = logging.getLogger(__name__)


@dataclass
class AdScriptResult:
    """Result object for generated ad copy."""

    script: str
    word_count: int
    estimated_duration_seconds: float
    model: str


def extract_text_from_response(response) -> str:
    """Extract only the final generated text, filtering out internal thinking parts."""
    texts = []
    try:
        if hasattr(response, "candidates") and response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        # Exclude internal reasoning/thought tokens
                        if not getattr(part, "thought", False) and getattr(part, "text", None):
                            texts.append(part.text)
    except Exception:
        pass

    if texts:
        return "\n".join(texts)
    return getattr(response, "text", "") or ""


def clean_script(text: str) -> str:
    """Sanitize and clean raw LLM output for natural voiceover reading.

    Removes markdown symbols, sound effect cues, production notes, and hashtags.
    """
    if not text:
        return ""

    # Remove square bracket cues: [música alegre], [efecto]
    cleaned = re.sub(r"\[.*?\]", "", text)

    # Remove parenthetical cues: (Voz en off:), (con entusiasmo:)
    cleaned = re.sub(r"\(.*?\)", "", cleaned)

    # Remove markdown headers and asterisks
    cleaned = re.sub(r"[*_#`]", "", cleaned)

    # Remove hashtags: #PideYa
    cleaned = re.sub(r"#\w+", "", cleaned)

    # Remove speaker prefixes like "Locutor:", "Narrador:"
    cleaned = re.sub(r"^(Locutor|Narrador|Voz|Voice):\s*", "", cleaned, flags=re.IGNORECASE | re.MULTILINE)

    # Normalize double quotes and apostrophes
    cleaned = cleaned.replace('"', "").replace("'", "")

    # Normalize whitespace and newlines into single spaces
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    cleaned = " ".join(lines)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


class BaseLLMBackend(ABC):
    """Abstract interface for LLM backends (Gemini API vs Ollama local)."""

    @abstractmethod
    def generate(self, prompt: str, model_id: str, fallback_model_id: str | None = None) -> tuple[str, str]:
        """Generate text from prompt.

        Returns:
            tuple[str, str]: (raw_text, actual_model_used)
        """
        pass


class GeminiBackend(BaseLLMBackend):
    """Google AI Studio / Gemini API backend for Gemma open-weight models."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY no está configurada. "
                "Obtén una clave gratuita en https://aistudio.google.com/ e indícala en el archivo .env"
            )
        self._client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, model_id: str, fallback_model_id: str | None = None) -> tuple[str, str]:
        model_to_use = model_id
        try:
            logger.info("Generating with Gemini Gemma model: %s (single-prompt)", model_to_use)
            # R1: Single message prompt without system_instruction
            response = self._client.models.generate_content(
                model=model_to_use,
                contents=prompt,
            )
            raw = extract_text_from_response(response)
            return raw, model_to_use
        except Exception as exc:
            if fallback_model_id and fallback_model_id != model_to_use:
                logger.warning(
                    "Primary model %s failed: %s. Attempting fallback to %s",
                    model_to_use,
                    exc,
                    fallback_model_id,
                )
                model_to_use = fallback_model_id
                response = self._client.models.generate_content(
                    model=model_to_use,
                    contents=prompt,
                )
                raw = extract_text_from_response(response)
                return raw, model_to_use
            raise


class OllamaBackend(BaseLLMBackend):
    """Local Ollama backend for offline local open-weight inference."""

    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt: str, model_id: str, fallback_model_id: str | None = None) -> tuple[str, str]:
        endpoint = f"{self.base_url}/api/generate"
        logger.info("Generating with local Ollama at %s using model %s", endpoint, model_id)
        try:
            with httpx.Client(timeout=60.0) as client:
                res = client.post(
                    endpoint,
                    json={
                        "model": model_id,
                        "prompt": prompt,
                        "stream": False,
                    },
                )
                if res.status_code != 200:
                    raise RuntimeError(f"Ollama error HTTP {res.status_code}: {res.text}")
                data = res.json()
                return data.get("response", ""), model_id
        except httpx.ConnectError as err:
            raise RuntimeError(
                f"No se pudo conectar al servidor local Ollama en {self.base_url}. "
                "Asegúrate de ejecutar 'ollama serve' o cambia LLM_BACKEND=gemini en el archivo .env."
            ) from err


class CopywriterService:
    """Service to generate professional audio ad scripts using Gemma models."""

    def __init__(self, settings: Settings | None = None, backend: BaseLLMBackend | None = None) -> None:
        self.settings = settings or get_settings()

        if backend is not None:
            self.backend = backend
        elif self.settings.llm_backend == "ollama":
            self.backend = OllamaBackend(base_url=self.settings.ollama_base_url)
        else:
            self.backend = GeminiBackend(api_key=self.settings.gemini_api_key)

    def generate_script(
        self,
        business_name: str,
        business_type: str,
        offer: str,
        call_to_action: str,
        tone: str = "energético",
        language: str = "es",
        duration_seconds: int = 30,
        target_words_override: int | None = None,
    ) -> AdScriptResult:
        """Generate an audio ad script with strict pacing and AIDA structure."""
        prompt = build_unified_prompt(
            business_name=business_name,
            business_type=business_type,
            offer=offer,
            call_to_action=call_to_action,
            tone=tone,
            language=language,
            duration_seconds=duration_seconds,
            target_words_override=target_words_override,
        )

        raw_text, model_used = self.backend.generate(
            prompt=prompt,
            model_id=self.settings.gemma_model_id,
            fallback_model_id=self.settings.fallback_model_id,
        )

        script = clean_script(raw_text)
        words = [w for w in script.split() if w.strip()]
        word_count = len(words)
        estimated_duration = calculate_estimated_duration(script, language)

        return AdScriptResult(
            script=script,
            word_count=word_count,
            estimated_duration_seconds=estimated_duration,
            model=model_used,
        )

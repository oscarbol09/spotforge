"""Copywriting service powered by Google Gemma open-weight models."""

import logging
import re
from dataclasses import dataclass
from google import genai
from google.genai import types

from app.config import Settings, get_settings
from app.prompts.ad_copywriter import (
    build_prompts,
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

    # Normalize double quotes and weird formatting
    cleaned = cleaned.replace('"', "").replace("'", "")

    # Normalize whitespace and newlines into single spaces
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    cleaned = " ".join(lines)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


class CopywriterService:
    """Service to generate professional audio ad scripts using Gemma models."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

        if not self.settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY no está configurada. "
                "Obtén una clave gratuita en https://aistudio.google.com/ e indícala en el archivo .env"
            )

        self._client = genai.Client(api_key=self.settings.gemini_api_key)

    def generate_script(
        self,
        business_name: str,
        business_type: str,
        offer: str,
        call_to_action: str,
        tone: str = "energético",
        language: str = "es",
        duration_seconds: int = 30,
    ) -> AdScriptResult:
        """Generate an audio ad script with strict pacing and AIDA structure.

        Attempts primary Gemma model first (e.g. gemma-3-27b-it);
        falls back to fallback model (e.g. gemma-2-9b-it) if necessary.
        """
        sys_prompt, user_prompt = build_prompts(
            business_name=business_name,
            business_type=business_type,
            offer=offer,
            call_to_action=call_to_action,
            tone=tone,
            language=language,
            duration_seconds=duration_seconds,
        )

        model_to_use = self.settings.gemma_model_id
        raw_text = ""

        try:
            logger.info("Generating ad script with primary model: %s", model_to_use)
            response = self._client.models.generate_content(
                model=model_to_use,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.7,
                ),
            )
            raw_text = extract_text_from_response(response)
        except Exception as exc:
            logger.warning(
                "Primary model %s failed: %s. Attempting fallback to %s",
                model_to_use,
                exc,
                self.settings.fallback_model_id,
            )
            model_to_use = self.settings.fallback_model_id
            response = self._client.models.generate_content(
                model=model_to_use,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=sys_prompt,
                    temperature=0.7,
                ),
            )
            raw_text = extract_text_from_response(response)

        script = clean_script(raw_text)
        words = [w for w in script.split() if w.strip()]
        word_count = len(words)
        estimated_duration = calculate_estimated_duration(script, language)

        return AdScriptResult(
            script=script,
            word_count=word_count,
            estimated_duration_seconds=estimated_duration,
            model=model_to_use,
        )

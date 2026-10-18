"""Unit and integration tests for the Copywriting service (Gemma)."""

import pytest
from unittest.mock import MagicMock

from app.config import Settings
from app.prompts.ad_copywriter import (
    calculate_target_words,
    calculate_estimated_duration,
    build_prompts,
)
from app.services.copywriter import (
    CopywriterService,
    AdScriptResult,
    clean_script,
)


# 1. Pacing & prompt tests
def test_calculate_target_words():
    # 30s in Spanish (2.5 wps) -> 75 words
    assert calculate_target_words(30, "es") == 75
    # 15s in Spanish -> 37 words
    assert calculate_target_words(15, "es") == 37
    # 30s in English (2.8 wps) -> 84 words
    assert calculate_target_words(30, "en") == 84


def test_calculate_estimated_duration():
    text = " ".join(["palabra"] * 75)
    assert calculate_estimated_duration(text, "es") == 30.0


def test_build_prompts_contains_required_fields():
    sys_prompt, user_prompt = build_prompts(
        business_name="Tacos Don Pepe",
        business_type="taquería",
        offer="3x2 en tacos al pastor",
        call_to_action="Pide por WhatsApp al 555-0199",
        tone="divertido",
        language="es",
        duration_seconds=30,
    )
    assert "AIDA" in sys_prompt
    assert "Tacos Don Pepe" in user_prompt
    assert "3x2 en tacos al pastor" in user_prompt
    assert "Pide por WhatsApp al 555-0199" in user_prompt


# 2. Sanitization tests
def test_clean_script_removes_markdown_and_cues():
    raw = (
        '**[Música alegre de fondo]**\n'
        '¿Tienes hambre? En "Tacos Don Pepe" tenemos la mejor solución.\n'
        '(Voz con energía:) Ven hoy mismo y disfruta.\n'
        '#PideYa #Tacos'
    )
    cleaned = clean_script(raw)
    assert "[Música alegre de fondo]" not in cleaned
    assert "(Voz con energía:)" not in cleaned
    assert "**" not in cleaned
    assert "#" not in cleaned
    assert "Tacos Don Pepe" in cleaned


# 3. Service initialization & error handling
def test_service_raises_on_missing_api_key():
    settings = Settings(gemini_api_key="")
    with pytest.raises(ValueError, match="GEMINI_API_KEY no está configurada"):
        CopywriterService(settings=settings)


# 4. Mocked generation tests
def test_generate_script_successful():
    settings = Settings(gemini_api_key="fake-test-key")
    service = CopywriterService(settings=settings)

    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = (
        "¿Antojo del auténtico sabor mexicano? En Tacos Don Pepe preparamos los mejores "
        "tacos al pastor de la ciudad con receta tradicional. Aprovecha nuestra promo de tres "
        "por dos en tacos al pastor todos los jueves. No te quedes con las ganas y pide "
        "directamente a nuestro WhatsApp. Tacos Don Pepe, tu mejor opción gastronómica."
    )
    mock_client.models.generate_content.return_value = mock_response
    service._client = mock_client

    result = service.generate_script(
        business_name="Tacos Don Pepe",
        business_type="taquería",
        offer="3x2 en tacos al pastor",
        call_to_action="Pide al WhatsApp",
        tone="energético",
        language="es",
        duration_seconds=30,
    )

    assert isinstance(result, AdScriptResult)
    assert "Tacos Don Pepe" in result.script
    assert result.word_count > 0
    assert result.estimated_duration_seconds > 0
    assert result.model == settings.gemma_model_id


def test_generate_script_fallback_on_primary_model_error():
    settings = Settings(
        gemini_api_key="fake-test-key",
        gemma_model_id="gemma-3-27b-it",
        fallback_model_id="gemma-2-9b-it",
    )
    service = CopywriterService(settings=settings)

    mock_client = MagicMock()
    # First call fails, second call succeeds
    mock_success_response = MagicMock()
    mock_success_response.text = "Guión generado con éxito por el modelo de respaldo."
    mock_client.models.generate_content.side_effect = [
        Exception("Model overloaded"),
        mock_success_response,
    ]
    service._client = mock_client

    result = service.generate_script(
        business_name="AutoLavado Express",
        business_type="lavado de autos",
        offer="Lavado gratis con cambio de aceite",
        call_to_action="Visítanos hoy",
    )

    assert result.model == settings.fallback_model_id
    assert "Guión generado con éxito" in result.script

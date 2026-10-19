"""Prompt definitions and utilities for generating audio ad copy using Gemma (v2)."""

# Speech pacing constants (words per second)
WORDS_PER_SECOND = {
    "es": 2.5,
    "en": 2.8,
}
DEFAULT_WPS = 2.5


def calculate_target_words(duration_seconds: int, language: str = "es") -> int:
    """Calculate maximum word count for a given duration in seconds.

    Args:
        duration_seconds: Target duration in seconds (e.g. 15, 30, 60).
        language: Language code ('es' or 'en').

    Returns:
        Target word count as an integer.
    """
    wps = WORDS_PER_SECOND.get(language.lower(), DEFAULT_WPS)
    return int(duration_seconds * wps)


def calculate_estimated_duration(text: str, language: str = "es") -> float:
    """Estimate spoken duration in seconds based on word count."""
    words = [w for w in text.split() if w.strip()]
    wps = WORDS_PER_SECOND.get(language.lower(), DEFAULT_WPS)
    return round(len(words) / wps, 1)


def get_language_name(lang_code: str) -> str:
    """Map language code to full descriptive name."""
    mapping = {
        "es": "Español (Latinoamericano comercial)",
        "en": "English (Natural commercial)",
    }
    return mapping.get(lang_code.lower(), "Español")


# SpotForge v2 unified prompt template for Gemma (single message, no system_instruction)
UNIFIED_PROMPT_TEMPLATE = """Eres un copywriter publicitario de radio profesional con 20 años de experiencia creando cuñas para negocios locales en Latinoamérica y España.

REGLAS ESTRICTAS:
1. Usa la fórmula AIDA (Atención -> Interés -> Deseo -> Acción).
2. El guión debe durar aproximadamente {duration_seconds} segundos al leerlo en voz alta.
   Referencia: ~2.5 palabras por segundo en español, ~2.8 en inglés.
   Para {duration_seconds}s -> entre {min_words} y {max_words} palabras máximo.
3. Primera frase: un gancho que detenga al oyente (pregunta retórica o dato impactante).
4. Incluye el nombre del negocio al menos 2 veces.
5. Termina con el call-to-action claro y memorable.
6. Tono: {tone}.
7. Idioma: {language_name}.
8. Sin hashtags, emojis ni formato markdown. Sin comillas dentro del texto.
9. Escribe números, precios y teléfonos con palabras, tal como se dicen naturalmente en radio:
   - Precios y ofertas: palabras completas (ejemplo: 'quince dólares', 'treinta por ciento', 'dos por uno').
   - Direcciones y cantidades: en números naturales (ejemplo: 'Avenida Central cuatrocientos cincuenta').
   - Teléfonos: en grupos rítmicos memorables (ejemplo: 'cinco cinco cinco, cero uno, nueve dos').
10. Puntuación estratégica: coma = pausa breve, punto = pausa media, puntos suspensivos = pausa dramática.

Devuelve SOLO el texto del guión, sin explicaciones ni metadatos.

DATOS DEL NEGOCIO:
Negocio: {business_name}
Tipo: {business_type}
Oferta: {offer}
Call to action: {call_to_action}
"""


def build_unified_prompt(
    business_name: str,
    business_type: str,
    offer: str,
    call_to_action: str,
    tone: str = "energético",
    language: str = "es",
    duration_seconds: int = 30,
    target_words_override: int | None = None,
) -> str:
    """Build a single unified prompt containing all instructions and context for Gemma."""
    target = target_words_override or calculate_target_words(duration_seconds, language)
    min_words = max(10, int(target * 0.85))
    max_words = int(target * 1.05)

    return UNIFIED_PROMPT_TEMPLATE.format(
        business_name=business_name,
        business_type=business_type,
        offer=offer,
        call_to_action=call_to_action,
        tone=tone,
        language_name=get_language_name(language),
        duration_seconds=duration_seconds,
        min_words=min_words,
        max_words=max_words,
    )


def build_prompts(
    business_name: str,
    business_type: str,
    offer: str,
    call_to_action: str,
    tone: str = "energético",
    language: str = "es",
    duration_seconds: int = 30,
) -> tuple[str, str]:
    """Backward-compatible tuple returning (system_prompt, user_prompt)."""
    unified = build_unified_prompt(
        business_name=business_name,
        business_type=business_type,
        offer=offer,
        call_to_action=call_to_action,
        tone=tone,
        language=language,
        duration_seconds=duration_seconds,
    )
    return "", unified

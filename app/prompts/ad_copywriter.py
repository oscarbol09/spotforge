"""Prompt definitions and utilities for generating audio ad copy using Gemma."""

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


SYSTEM_COPYWRITER_PROMPT = """Eres un redactor creativo y locutor publicitario galardonado con más de 15 años de experiencia creando cuñas de radio y audio digital (Spotify Ads, Instagram Reels, cuñas radiales) de alta conversión para pequeños negocios locales.

Tu misión es escribir el guión EXACTO que será leído por un locutor profesional.

REGLAS INFALIBLES DE REDACCIÓN:
1. ESTRUCTURA AIDA:
   - ATENCIÓN (primeros 3-5 segundos): Un gancho impactante o pregunta que detenga al oyente en seco.
   - INTERÉS: Conecta con el problema o deseo real del cliente.
   - DESEO: Presenta la oferta irresistible del negocio. Menciona el nombre del negocio exactamente 2 veces.
   - ACCIÓN: Llamada a la acción clara, directa y urgente (ej: 'Llama ya', 'Visítanos en...', 'Pide por WhatsApp').

2. CONTROL DE TIEMPO Y PALABRAS:
   - Duración objetivo: {duration_seconds} segundos.
   - LÍMITE ESTRICTO: Entre {min_words} y {max_words} palabras.
   - Si te pasas de palabras, el audio quedará cortado. Si usas muy pocas, sobrará tiempo.

3. REGLAS DE LOCUCIÓN:
   - NO incluyas acotaciones de producción como [música alegre], [efecto de sonido], (Voz en off:), ni indicaciones de tono.
   - NO uses comillas, asteriscos, títulos, ni formato Markdown.
   - NO uses emojis ni hashtags.
   - Utiliza comas y puntos estratégicos para crear pausas naturales de respiración para el locutor.
   - Escribe los números con palabras o dígitos legibles para locución.

DEVUELVE ÚNICAMENTE EL TEXTO DIRECTO DEL GUIÓN LISTO PARA SER LEÍDO."""


USER_COPYWRITER_PROMPT = """Crea el guión de cuña publicitaria con los siguientes datos:

- Nombre del Negocio: {business_name}
- Tipo de Negocio: {business_type}
- Oferta / Promoción: {offer}
- Llamada a la Acción (CTA): {call_to_action}
- Tono deseado: {tone}
- Idioma: {language_name}
- Duración objetivo: {duration_seconds} segundos (Exactamente entre {min_words} y {max_words} palabras)

Escribe el guión final:"""


def get_language_name(lang_code: str) -> str:
    """Map language code to full descriptive name."""
    mapping = {
        "es": "Español (Latinoamericano neutro / comercial)",
        "en": "English (Natural, clear, commercial)",
    }
    return mapping.get(lang_code.lower(), "Español")


def build_prompts(
    business_name: str,
    business_type: str,
    offer: str,
    call_to_action: str,
    tone: str = "energético",
    language: str = "es",
    duration_seconds: int = 30,
) -> tuple[str, str]:
    """Build system and user prompts with calculated constraints.

    Returns:
        tuple[str, str]: (system_prompt, user_prompt)
    """
    target = calculate_target_words(duration_seconds, language)
    min_words = max(10, int(target * 0.85))
    max_words = int(target * 1.05)

    sys_prompt = SYSTEM_COPYWRITER_PROMPT.format(
        duration_seconds=duration_seconds,
        min_words=min_words,
        max_words=max_words,
    )

    user_prompt = USER_COPYWRITER_PROMPT.format(
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

    return sys_prompt, user_prompt

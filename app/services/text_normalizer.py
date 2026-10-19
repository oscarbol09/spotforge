"""Text normalizer for TTS: converts digits, prices, promos, and phones to natural spoken words."""

import re
import logging
from num2words import num2words

logger = logging.getLogger(__name__)

SPANISH_DIGITS = {
    "0": "cero",
    "1": "uno",
    "2": "dos",
    "3": "tres",
    "4": "cuatro",
    "5": "cinco",
    "6": "seis",
    "7": "siete",
    "8": "ocho",
    "9": "nueve",
}

ENGLISH_DIGITS = {
    "0": "zero",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}


def normalize_phone_number(match: re.Match, language: str = "es") -> str:
    """Convert phone number digits to natural rhythmically grouped spoken words.
    
    Prevents TTS prosodic dead air from commas after every single digit.
    E.g. 555-0192 becomes 'cinco cinco cinco, cero uno, nueve dos'.
    """
    raw = match.group(0)
    digits = [c for c in raw if c.isdigit()]
    digit_map = SPANISH_DIGITS if language.startswith("es") else ENGLISH_DIGITS
    spoken_digits = [digit_map.get(d, d) for d in digits]

    n = len(spoken_digits)
    if n == 7:
        chunks = [
            " ".join(spoken_digits[0:3]),
            " ".join(spoken_digits[3:5]),
            " ".join(spoken_digits[5:7]),
        ]
    elif n == 10:
        chunks = [
            " ".join(spoken_digits[0:3]),
            " ".join(spoken_digits[3:6]),
            " ".join(spoken_digits[6:8]),
            " ".join(spoken_digits[8:10]),
        ]
    elif n >= 6:
        chunks = [" ".join(spoken_digits[0:3])]
        for i in range(3, n, 2):
            chunks.append(" ".join(spoken_digits[i : i + 2]))
    else:
        chunks = [" ".join(spoken_digits)]

    return ", ".join(chunks)


def normalize_promo_multiplier(match: re.Match, language: str = "es") -> str:
    """Normalize '2x1', '3x2' into spoken words."""
    n1 = int(match.group(1))
    n2 = int(match.group(2))
    lang = "es" if language.startswith("es") else "en"
    w1 = num2words(n1, lang=lang)
    w2 = num2words(n2, lang=lang)
    connector = "por" if lang == "es" else "for"
    return f"{w1} {connector} {w2}"


def normalize_percentage(match: re.Match, language: str = "es") -> str:
    """Normalize '50%' to 'cincuenta por ciento'."""
    val = int(match.group(1))
    lang = "es" if language.startswith("es") else "en"
    word = num2words(val, lang=lang)
    suffix = "por ciento" if lang == "es" else "percent"
    return f"{word} {suffix}"


def normalize_currency(match: re.Match, language: str = "es") -> str:
    """Normalize '$15' or '$15 dólares' to 'quince dólares' without duplication."""
    num_str = match.group(1).replace(",", "")
    lang = "es" if language.startswith("es") else "en"
    try:
        if "." in num_str:
            val = float(num_str)
            word = num2words(val, lang=lang)
        else:
            val = int(num_str)
            word = num2words(val, lang=lang)
    except Exception:
        return match.group(0)

    unit = "dólares" if lang == "es" else "dollars"
    return f"{word} {unit}"


def normalize_for_tts(text: str, language: str = "es") -> str:
    """Deterministically convert digits, symbols, promos, prices and phone numbers to words.

    Acts as the deterministic safety net for TTS so numbers are pronounced flawlessly.
    """
    if not text:
        return ""

    result = text
    lang = "es" if language.lower().startswith("es") else "en"

    # 1. Normalize promo multipliers: 2x1, 3x2, 2X1
    result = re.sub(
        r"\b(\d+)\s*[xX]\s*(\d+)\b",
        lambda m: normalize_promo_multiplier(m, lang),
        result,
    )

    # 2. Normalize percentages: 50%, 25 %
    result = re.sub(
        r"\b(\d+)\s*%",
        lambda m: normalize_percentage(m, lang),
        result,
    )

    # 3. Normalize currency: $15, $500, $ 20, $15 dólares, $15 USD (consumes redundant unit words)
    currency_pattern = r"\$\s*(\d+(?:[.,]\d+)?)(?:\s*(?:dólares|dolares|dollars|usd))?"
    result = re.sub(
        currency_pattern,
        lambda m: normalize_currency(m, lang),
        result,
        flags=re.IGNORECASE,
    )

    # 4. Normalize phone numbers: e.g. 555-0199, 555-4321, 555 1234, (555) 123-4567
    phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}|\b\d{3}[-.\s]\d{4}\b|\b\d{3}[-.\s]\d{3,4}\b"
    result = re.sub(
        phone_pattern,
        lambda m: normalize_phone_number(m, lang),
        result,
    )

    # 5. Normalize remaining standalone integers: e.g. "todos los 15 días", "año 2026"
    def replace_standalone_num(m: re.Match) -> str:
        val = int(m.group(0))
        try:
            return num2words(val, lang=lang)
        except Exception:
            return m.group(0)

    result = re.sub(r"\b\d+\b", replace_standalone_num, result)

    # Clean redundant spaces
    result = re.sub(r"\s+", " ", result).strip()

    return result

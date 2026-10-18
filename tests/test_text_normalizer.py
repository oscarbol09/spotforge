"""Unit tests for the Text Normalizer service (R3)."""

from app.services.text_normalizer import normalize_for_tts


def test_normalize_promo_multipliers_spanish():
    text = "Aprovecha la gran promo de 2x1 en pizzas y 3x2 en bebidas."
    normalized = normalize_for_tts(text, language="es")
    assert "dos por uno" in normalized
    assert "tres por dos" in normalized
    assert "2x1" not in normalized


def test_normalize_promo_multipliers_english():
    text = "Get our special 2x1 deal today!"
    normalized = normalize_for_tts(text, language="en")
    assert "two for one" in normalized
    assert "2x1" not in normalized


def test_normalize_percentages():
    text = "Obtén un 50% de descuento en tu primer servicio."
    normalized = normalize_for_tts(text, language="es")
    assert "cincuenta por ciento" in normalized
    assert "50%" not in normalized

    text_en = "Enjoy 25% off today only."
    normalized_en = normalize_for_tts(text_en, language="en")
    assert "twenty-five percent" in normalized_en
    assert "25%" not in normalized_en


def test_normalize_currency_prices():
    text = "Corte y barba por solo $15 este fin de semana."
    normalized = normalize_for_tts(text, language="es")
    assert "quince dólares" in normalized
    assert "$15" not in normalized

    text_en = "Burgers starting at $10."
    normalized_en = normalize_for_tts(text_en, language="en")
    assert "ten dollars" in normalized_en
    assert "$10" not in normalized_en


def test_normalize_phone_numbers():
    text = "Llama ya al 555-4321 o escríbenos."
    normalized = normalize_for_tts(text, language="es")
    assert "cinco, cinco, cinco, cuatro, tres, dos, uno" in normalized
    assert "555-4321" not in normalized

    text_long = "Comunícate al 555-0199 hoy mismo."
    normalized_long = normalize_for_tts(text_long, language="es")
    assert "cinco, cinco, cinco, cero, uno, nueve, nueve" in normalized_long


def test_normalize_standalone_numbers():
    text = "Abrimos en 10 minutos."
    normalized = normalize_for_tts(text, language="es")
    assert "diez minutos" in normalized
    assert "10" not in normalized

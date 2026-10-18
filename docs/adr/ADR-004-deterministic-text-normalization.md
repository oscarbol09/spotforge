# ADR-004: Capa Determinista de Normalización de Texto para TTS

## Estado
Aceptado

## Contexto
Los modelos de Text-To-Speech fallan frecuentemente al pronunciar cifras complejas, promociones comerciales (como "2x1"), porcentajes ("30%"), monedas ("$15") y números telefónicos ("555-0199"), pronunciándolos de forma antinatural o ininteligible en audio publicitario.

## Decisión
Implementar un servicio determinista de preprocesamiento fonético (`app.services.text_normalizer`) basado en expresiones regulares y `num2words` antes de enviar el guión a ElevenLabs:
1. Multiplicadores promocionales: `2x1` -> "dos por uno".
2. Monedas: `$15` -> "quince dólares".
3. Porcentajes: `30%` -> "treinta por ciento".
4. Teléfonos: `555-0192` -> "cinco, cinco, cinco, cero, uno, nueve, dos" (con pausas de respiración).
5. Números sueltos: `2026` -> "dos mil veintiséis".

## Consecuencias
- **Positivas**: 100% de inteligibilidad en las llamadas a la acción y ofertas críticas.
- **Trade-offs**: Añade un paso de normalización en milisegundos en el backend.

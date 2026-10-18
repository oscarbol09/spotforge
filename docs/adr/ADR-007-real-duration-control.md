# ADR-007: Medición de Duración Real del MP3 y Bucle Adaptativo de 1 Reintento

## Estado
Aceptado

## Contexto
Los anuncios comerciales de radio, Spotify Ads y Stories tienen límites estrictos de tiempo (15s, 30s o 60s). La heurística de estimar la duración multiplicando palabras por 0.4 segundos es aproximada y puede fallar por la velocidad natural de locución de cada voz de ElevenLabs.

## Decisión
1. **Medición binaria real**: Utilizar la biblioteca `mutagen` para extraer la duración exacta en segundos del archivo MP3 sintetizado.
2. **Bucle adaptativo de 1 reintento**: Si la duración real excede el objetivo en más de 3 segundos (`measured_duration > target + 3.0s`), el sistema recalcula proporcionalmente el número de palabras (`reduced_word_target = word_count * (target / measured)`), solicita un reintento a Gemma con esa cota estricta y re-sintetiza el audio.
3. **Límite estricto**: Máximo 1 reintento para prevenir latencias prolongadas o consumo excesivo de créditos.

## Consecuencias
- **Positivas**: Garantía de cumplimiento del tiempo pautado para campañas publicitarias.

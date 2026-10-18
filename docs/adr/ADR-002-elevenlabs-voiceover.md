# ADR-002: Locución Comercial de Alta Fidelidad con ElevenLabs

## Estado
Aceptado

## Contexto
El éxito de una cuña de radio, anuncio de Stories o TikTok depende críticamente de la entonación, modulación humana y prosodia natural de la voz. Los motores TTS locales de código abierto actuales sufren de artefactos robóticos o falta de energía comercial en español.

## Decisión
Integrar la API oficial de **ElevenLabs** utilizando el modelo `eleven_multilingual_v2` con fallback configurable vía `ELEVENLABS_MODEL`.
- Catálogo de voces comerciales curadas (Rachel, Adam, Antoni, Bella).
- Mapeo dinámico de nombres de locutores y control de estabilidad (0.45) y similarity boost (0.75).
- Métricas auditables de consumo de caracteres por spot.

## Consecuencias
- **Positivas**: Calidad de audio indistinguible de un estudio de locución comercial.
- **Trade-offs**: Requiere conectividad a Internet y una API key válida de ElevenLabs.

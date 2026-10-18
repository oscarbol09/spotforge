# ADR-002: High-Fidelity Studio Voice Synthesis with ElevenLabs

## Status
Accepted

## Context
The success of a broadcast radio spot, Instagram Story, or TikTok ad depends heavily on human-like intonation, natural prosody, and commercial energy. Current local open-source TTS models still exhibit robotic artifacts or lack lively commercial punch in multi-lingual commercial contexts.

## Decision
Integrate the official **ElevenLabs** API utilizing the `eleven_multilingual_v2` model with configurable fallback via `ELEVENLABS_MODEL`.
- Curated commercial voice talent profiles (Rachel, Adam, Antoni, Bella).
- Dynamic voice name resolution and tuned voice settings (`stability: 0.45`, `similarity_boost: 0.75`).
- Granular character usage tracking per spot to provide transparent cost telemetry.

## Consequences
- **Positive**: Studio-grade broadcast audio quality indistinguishable from professional voiceover talent.
- **Trade-offs**: Requires internet connectivity and an active ElevenLabs API key.

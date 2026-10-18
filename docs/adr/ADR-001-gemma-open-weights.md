# ADR-001: Adoption of Google Gemma 4 as Open-Weight Ad Copywriter

## Status
Accepted

## Context
SpotForge requires generating 15, 30, and 60-second commercial ad scripts structured around the persuasive AIDA framework (Attention, Interest, Desire, Action) and constrained to strict speech pacing (~2.5 words/second in Spanish, ~2.8 words/second in English). Relying on closed proprietary LLM APIs introduces ongoing per-token markups, subscription dependencies, and vendor lock-in risks for solo digital marketing freelancers building a sustainable Side Hustle.

## Decision
Adopt the **Google Gemma 4** open-weight model family (`gemma-4-26b-a4b-it` with automatic fallback to `gemma-4-31b-it`).
1. **Unified Prompt without `system_instruction`**: Structured as a single message to ensure 100% compatibility across both Google AI Studio API and local runtime backends.
2. **Thought Tokens Extraction**: Gemma 4 emits internal reasoning traces (`part.thought == True`); we implemented surgical filtering to send only clean, spoken commercial copy to the TTS engine.
3. **`BaseLLMBackend` Abstraction**: Supports seamless execution in the cloud via Google AI Studio or 100% offline local inference via Ollama (`ollama run gemma`).

## Consequences
- **Positive**: Script copywriting cost is virtually $0 per ad. Full transparency and model weight ownership. Total client data privacy when running locally via Ollama.
- **Trade-offs**: Requires input sanitization to strip bracketed production cues (`[music]`) or parentheticals before speech synthesis.

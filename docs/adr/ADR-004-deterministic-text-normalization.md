# ADR-004: Deterministic Phonetic Text Normalization Layer for TTS

## Status
Accepted

## Context
Text-to-speech engines frequently stumble over commercial terminology, promo multipliers (e.g., "2x1" or "2 for 1"), percentages ("30%"), currencies ("$15"), and telephone numbers ("555-0199"), often pronouncing them awkwardly or unintelligibly in fast-paced commercial audio.

## Decision
Implement a deterministic phonetic pre-processing service (`app.services.text_normalizer`) based on regex pattern matching and `num2words` before passing the script to ElevenLabs:
1. Promo multipliers: `2x1` ➔ "dos por uno" (ES) or "two for one" (EN).
2. Currencies: `$15` ➔ "quince dólares" (ES) or "fifteen dollars" (EN).
3. Percentages: `30%` ➔ "treinta por ciento" (ES) or "thirty percent" (EN).
4. Phone numbers: `555-0192` ➔ "cinco cinco cinco, cero uno, nueve dos" (ES) with rhythmic cadence groups to induce natural broadcast pauses and ensure listener recall.
5. Standalone integers: `2026` ➔ "dos mil veintiséis" (ES) or "two thousand and twenty-six" (EN).

## Consequences
- **Positive**: 100% clarity and precision in business offers and critical calls to action.
- **Trade-offs**: Adds a negligible sub-millisecond string transformation step in the backend pipeline.

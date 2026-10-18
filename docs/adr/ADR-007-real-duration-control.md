# ADR-007: Real MP3 Duration Measurement and Adaptive 1-Retry Pacing Loop

## Status
Accepted

## Context
Commercial ad spots for radio, Spotify Ads, and social media Stories enforce strict runtime windows (15s, 30s, or 60s). Pacing heuristics (such as multiplying words by 0.4 seconds) are approximations that often drift depending on the unique cadence and pauses of different voice talents.

## Decision
1. **Accurate Binary Measurement**: Utilize the `mutagen` audio library to measure the exact physical runtime in seconds from the rendered MP3 header.
2. **Adaptive 1-Retry Loop**: If measured audio exceeds the target duration by more than 3 seconds (`measured_duration > target + 3.0s`), the system dynamically recalculates a reduced word target:
   $$\text{reduced\_target} = \text{word\_count} \times \left(\frac{\text{target}}{\text{measured}}\right)$$
   and requests a compressed rewrite from Gemma before re-synthesizing.
3. **Hard Bounds**: Strict maximum of 1 retry to prevent excessive latency and unnecessary token/character quota consumption.

## Consequences
- **Positive**: Strict adherence to broadcast ad specifications.

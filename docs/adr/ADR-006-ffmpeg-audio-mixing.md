# ADR-006: Professional Background Musical Bed Mixing with FFmpeg

## Status
Accepted

## Context
A voiceover ad without background music sounds like an informal voice memo rather than a polished commercial. Professional radio and digital video ads invariably incorporate a musical bed that establishes brand mood, maintains listener attention, and increases ad recall.

## Decision
Integrate a multimedia audio mixing service (`app.services.audio_mixer`) powered by **FFmpeg**:
1. **Seamless Loop**: `-stream_loop -1` to cover any custom script duration smoothly.
2. **Dynamic Volume Ducking**: Lowers background music to 15% (`volume=0.15`) so the voiceover remains crisp, clear, and prominent.
3. **Voice Duration Matching**: `amix=inputs=2:duration=first` to truncate the musical bed exactly when speech finishes.
4. **Smooth Fadeout**: 2-second gentle tail fade (`afade=t=out`) for a polished broadcast transition.
5. **Graceful Degradation**: If FFmpeg is unavailable in the execution environment, SpotForge gracefully returns the clean voiceover along with an informative non-blocking warning.

## Consequences
- **Positive**: Broadcast radio-grade audio production generated within seconds.
- **Trade-offs**: Requires the `ffmpeg` binary installed on the host system or container.

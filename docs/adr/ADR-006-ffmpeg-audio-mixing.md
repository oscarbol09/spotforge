# ADR-006: Mezcla Profesional de Cama Musical de Fondo con FFmpeg

## Estado
Aceptado

## Contexto
Una cuña publicitaria con solo voz a capella suena como un mensaje de voz o dictado informal. Los anuncios profesionales de radio y redes sociales siempre cuentan con una cama musical (*music bed*) que evoca la emoción adecuada y mantiene al oyente enganchado.

## Decisión
Integrar un servicio de mezcla de audio (`app.services.audio_mixer`) apoyado en **FFmpeg**:
1. **Looping infinito del track**: `-stream_loop -1` para que cualquier duración sea cubierta sin cortes.
2. **Atenuación de volumen (*ducking*)**: La música de fondo se reduce al 15% (`volume=0.15`) para priorizar la inteligibilidad vocal.
3. **Corte a la duración de la voz**: `amix=inputs=2:duration=first`.
4. **Fundido de salida (*fade out*)**: 2 segundos de `afade=t=out` al final del audio para un remate suave y profesional.
5. **Degradación elegante**: Si FFmpeg no estuviera instalado en el entorno, el sistema devuelve la voz limpia con un warning descriptivo no bloqueante.

## Consecuencias
- **Positivas**: Acabado de producción de radio comercial en segundos.
- **Trade-offs**: Requiere el binario `ffmpeg` instalado en el sistema operativo.

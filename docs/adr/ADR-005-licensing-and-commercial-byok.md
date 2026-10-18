# ADR-005: Licenciamiento Comercial Honesto y Modelo BYOK (Bring Your Own Key)

## Estado
Aceptado

## Contexto
El plan gratuito de ElevenLabs **no concede derechos comerciales** sobre los audios generados y exige atribución pública. Afirmar falsamente que SpotForge permite generar cuñas publicitarias para revender a "$0 de costo" viola los términos de servicio de ElevenLabs y engaña a los desarrolladores y jueces del desafío Side Hustle.

## Decisión
1. **Transparencia radical de precios**: Documentar con rigor que la comercialización y reventa de spots requiere al menos el plan **Starter ($6/mes)** de ElevenLabs.
2. **Economía unitaria defendible**:
   - Plan Starter: $6 USD por 30,000 caracteres.
   - Spot típico de 30s: ~400 caracteres (~70 palabras).
   - Cuñas incluidas en el plan base: 75 spots = **$0.08 USD (~8 centavos)** por spot.
   - Cuñas adicionales: $0.30 por 1,000 caracteres = **$0.12 USD (~12 centavos)** por spot.
   - Costo Gemma 4: $0.00 (Google AI Studio Free Tier u Ollama).
   - Precio de venta recomendado al negocio local: **$5.00 – $15.00 USD**.
   - Margen bruto para el freelancer: **97.6% – 99.2%**.
3. **Arquitectura BYOK (Bring Your Own Key)**: SpotForge no revende keys de ElevenLabs; el usuario ingresa su propia API key en `.env`, siendo el único titular de los derechos comerciales que su suscripción ampare.

## Consecuencias
- **Positivas**: Integridad legal absoluta, credibilidad ante el jurado de Hacktoberfest y seguridad jurídica para los usuarios finales.

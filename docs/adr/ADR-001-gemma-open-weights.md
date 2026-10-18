# ADR-001: Adopción de Google Gemma 4 como Redactor Publicitario de Pesos Abiertos

## Estado
Aceptado

## Contexto
SpotForge requiere generar guiones publicitarios de 15, 30 y 60 segundos con estructura persuasiva AIDA (Atención, Interés, Deseo, Acción) y cadencia estricta de locución (~2.5 palabras por segundo). Utilizar modelos propietarios de caja negra implicaría costos recurrentes por token, dependencia de tarifas cerradas y riesgo de vendor lock-in para un freelance que construye su Side Hustle.

## Decisión
Adoptar la familia de modelos de pesos abiertos **Google Gemma 4** (`gemma-4-26b-a4b-it` con fallback a `gemma-4-31b-it`).
1. **Prompt unificado sin `system_instruction`**: Diseñado en un solo mensaje para total compatibilidad con la API de Google AI Studio y backends locales.
2. **Filtrado de tokens de pensamiento**: Gemma 4 incluye razonamiento explícito (`part.thought == True`); implementamos extracción quirúrgica para enviar únicamente el copy hablado a TTS.
3. **Abstracción `BaseLLMBackend`**: Soporta ejecución en la nube (Google AI Studio) o 100% offline local vía Ollama (`ollama run gemma`).

## Consecuencias
- **Positivas**: Costo de redacción prácticamente $0 por spot. Control total sobre los pesos del modelo. Privacidad garantizada para negocios locales si se ejecuta en Ollama.
- **Trade-offs**: Requiere sanitización de indicaciones entre corchetes o paréntesis antes de pasar el texto al motor de síntesis de voz.

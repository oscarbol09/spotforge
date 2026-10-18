# ADR-003: Arquitectura Backend FastAPI y Frontend SPA Minimalista

## Estado
Aceptado

## Contexto
El usuario objetivo de SpotForge (freelancers, agencias boutique y dueños de negocio) necesita una interfaz reactiva, rápida y sin fricción de instalación o dependencias complejas de Node/Webpack.

## Decisión
1. **Backend**: FastAPI con Python 3.12, tipado estricto con Pydantic v2, endpoints REST idempotentes y manejo estructurado de excepciones.
2. **Frontend**: Single Page Application (SPA) en HTML5 semántico + Tailwind CSS CDN, con animaciones de ondas de audio, reproductor nativo HTML5 y JavaScript vanilla modular.
3. **Despliegue**: Hermético en un solo contenedor o servicio web en Render vía `render.yaml`.

## Consecuencias
- **Positivas**: Cero pasos de build de frontend; latencia instantánea; interfaz moderna y responsiva.

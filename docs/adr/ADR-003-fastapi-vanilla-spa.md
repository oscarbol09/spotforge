# ADR-003: FastAPI Backend and Minimalist Vanilla SPA Frontend

## Status
Accepted

## Context
SpotForge's target users (freelancers, local agency consultants, and small business owners) need a responsive, friction-free interface without complex Node/npm build steps, heavy bundlers, or hydration overhead.

## Decision
1. **Backend**: FastAPI with Python 3.12, strict Pydantic v2 schemas, idempotent REST endpoints, and structured exception handling.
2. **Frontend**: Single Page Application (SPA) built with semantic HTML5 and modern Tailwind CSS (via CDN), featuring soundwave animations, a native HTML5 audio player, and modular vanilla JavaScript with client-side i18n support.
3. **Deployment**: Self-contained web service deployable to Render with zero configuration via `render.yaml`.

## Consequences
- **Positive**: Zero frontend build pipeline, instant page load speeds, clean separation of concerns, and low operational overhead.

# ADR-005: Commercial Licensing Integrity and BYOK (Bring Your Own Key) Architecture

## Status
Accepted

## Context
ElevenLabs' Free tier **does not grant commercial rights** over generated audio and mandates public attribution. Falsely claiming that SpotForge enables freelancers to produce commercial ads for local clients at "$0 cost" violates ElevenLabs' Terms of Service and misleads competition judges and developers.

## Decision
1. **Radical Pricing Transparency**: Clearly document that commercial resale of generated ad spots requires at least ElevenLabs' **Starter Tier ($6 USD/month)**.
2. **Defensible Unit Economics**:
   - Starter Plan: $6 USD for 30,000 characters per month.
   - Standard 30s commercial ad: ~400 characters (~70 words).
   - Spots included within the base plan: 75 spots = **$0.08 USD (~8 cents)** per spot.
   - Additional spots beyond quota: $0.30 per 1,000 characters = **$0.12 USD (~12 cents)** per spot.
   - Gemma 4 copywriting cost: $0.00 (Google AI Studio Free Tier or local Ollama).
   - Recommended resale price to local business clients: **$5.00 – $15.00 USD**.
   - Freelancer gross profit margin: **97.6% – 99.2%**.
3. **BYOK (Bring Your Own Key) Architecture**: SpotForge does not broker or resell ElevenLabs API keys. Users configure their own API key in `.env`, ensuring that all commercial rights are legitimately backed by their active ElevenLabs subscription.

## Consequences
- **Positive**: Absolute legal compliance, credibility with hackathon evaluators, and legal protection for freelancers and their clients.

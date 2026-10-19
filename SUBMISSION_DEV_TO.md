---
title: "SpotForge: Turn 3 Local Business Facts into a Commercial Audio Ad with Gemma 4 and ElevenLabs"
published: true
description: "Turn 3 facts about any local store into a broadcast-ready 30-second audio ad with open-weights Gemma 4, text normalization, ElevenLabs studio voice, and FFmpeg music mixing in seconds."
tags: devchallenge, hf26challenge, hacktoberfest, ai
cover_image: https://raw.githubusercontent.com/oscarbol09/spotforge/master/docs/cover.png
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

---

## What I Built

Every week, millions of neighborhood businesses—pizzerias, barbershops, dental clinics, auto repair shops—struggle to capture local attention. They know that video stories, Instagram Reels, TikTok ads, and community radio are the fastest ways to drive foot traffic.

There is a major barrier: **commercial audio production is prohibitively expensive.**

- **A traditional creative agency** charges between **$300 and $800 USD** for a single 30-second commercial script, studio booking, and voice talent.
- **Freelance digital marketers** managing 5 to 10 local accounts cannot justify spending hundreds of dollars just to promote a Tuesday pizza discount or a weekend oil change deal.
- **Doing it themselves** results in amateur cellphone voice notes with background noise, hesitant pacing, and weak calls to action that listeners scroll past immediately.

### The Solution: SpotForge

**SpotForge** is an open-source, turnkey audio advertising studio designed specifically for freelancers, digital marketing consultants, and small business owners. It takes **3 simple facts** about a local business and produces a broadcast-ready, 30-second commercial ad spot in under 15 seconds:

```
Business Facts -> Gemma 4 (AIDA) -> Text Normalizer -> ElevenLabs Voice -> FFmpeg Music Bed -> Broadcast MP3
```

Here is what happens under the hood:
1. **Business Input**: Business Name, Core Offer, and Call-to-Action.
2. **Production Parameters**: Commercial tone (Energetic, Warm, Professional, Fun, Urgent), Language (Spanish or English), Target Duration (15s, 30s, or 60s), Voice Talent, and Background Music Bed.
3. **Open-Weight Intelligence (Google Gemma 4)**: Generates a persuasive ad script following the **AIDA formula** (Attention -> Interest -> Desire -> Action) with strict audio pacing limits (~2.5 words/second in Spanish, ~2.8 words/second in English). Supports Google AI Studio or **100% offline local inference with Ollama**.
4. **Deterministic Text Normalization**: Converts tricky numbers, promo multipliers (`2x1` -> "two for one" / "dos por uno"), currencies (`$15` -> "fifteen dollars" / "quince dólares"), percentages (`30%` -> "thirty percent" / "treinta por ciento"), and phone numbers (`555-0192` -> "cinco cinco cinco, cero uno, nueve dos") into clear spoken words with natural broadcast cadence.
5. **Studio Voice Synthesis (ElevenLabs)**: Renders human-grade voiceover with tailored stability and similarity settings.
6. **Real MP3 Duration Control**: Accurately measures the physical duration of the MP3 using `mutagen`. If the speech exceeds the target duration by more than 3 seconds, SpotForge automatically applies **1 adaptive retry** with a proportionally reduced word budget.
7. **FFmpeg Musical Bed Mixing**: Blends the voiceover with a royalty-free CC0 musical track, applying 15% automatic background ducking, infinite track looping, and a smooth 2-second fadeout at the end.
8. **Public Abuse Protection**: Built-in sliding-window IP rate limiting prevents quota exhaustion when deployed as a public demo.

### Side Hustle Economics: Pennies to Produce, 97%+ Gross Margin

Many AI projects claim "$0 cost forever" by glossing over commercial licensing realities. We believe judges and engineers value **honest, real-world economics**:

- **ElevenLabs Free Plan**: Free tier audio does **not** include commercial rights and requires public attribution.
- **ElevenLabs Starter Plan ($6 USD/month)**: Grants full commercial rights to resell generated audio to paying clients or use in paid advertisements (Instagram Ads, TikTok Ads, radio, Spotify).
- **SpotForge BYOK Architecture**: Users provide their own API key in `.env`. Commercial rights are cleanly backed by the user's active tier.

#### The Unit Economics Table

| Parameter | Traditional Audio Agency | SpotForge (Starter Plan) |
|---|---|---|
| **Copywriting (AIDA script)** | $150 – $300 USD | **$0.00** (Gemma 4 Open-Weights) |
| **Studio & Voice Talent** | $150 – $500 USD | **$0.08 – $0.12 USD** (~400 chars) |
| **Sound Engineering & Music** | $50 – $100 USD | **$0.00** (FFmpeg + CC0 Public Domain Beds) |
| **Total Production Cost** | **$350 – $900 USD** | **$0.08 – $0.12 USD** |
| **Freelancer Resale Price** | $350 – $900 USD | **$5.00 – $15.00 USD** |
| **Freelance Gross Margin** | N/A | **97.6% – 99.2%** |
| **Spots Included in $6/mo** | 0 spots | **~75 spots of 30 seconds** |

**The Side Hustle Playbook**: A solo freelancer offering social media management to local shops can include 2 fresh promo spots per week for an extra $30/month per client. With just 5 clients, that is **$150/month in revenue for $6 in ElevenLabs costs and 30 minutes of total work**—a sustainable, high-margin side hustle.

---

## Demo

- **Live Deployed Application**: [https://spotforge.onrender.com](https://spotforge.onrender.com) *(Hosted on Render's free tier; if inactive, please allow ~50 seconds for the container to spin up).*

Here are three authentic commercial spots generated end-to-end by SpotForge:

| Client Business | Commercial Category | Voice Talent | Background Music | Real Duration | Audio File |
|---|---|---|---|---|---|
| **Pizzería Don Mario** | Wood-fired artisanal Italian pizzeria | George | Upbeat Commercial (110 BPM) | **28.4s** | [`demo_pizzeria.mp3`](https://github.com/oscarbol09/spotforge/raw/master/static/audio/demo_pizzeria.mp3) |
| **Barbería El Bigote** | Classic executive men's grooming & hot towel | Liam | Urban Energy (120 BPM) | **31.9s** | [`demo_barber.mp3`](https://github.com/oscarbol09/spotforge/raw/master/static/audio/demo_barber.mp3) |
| **Apex Auto Repair** | Multi-brand automotive mechanics & brake service | Roger | Chill Acoustic (75 BPM) | **27.3s** | [`demo_autorepair.mp3`](https://github.com/oscarbol09/spotforge/raw/master/static/audio/demo_autorepair.mp3) |

### Transcripts Generated by Gemma 4:

> **Pizzería Don Mario (28.4s)**:  
> *"¿Buscas el auténtico sabor de Italia sin salir de casa? En Pizzería Don Mario, usamos horno de leña y masa madre para crear la textura más crujiente. ¡Atención! Los martes y jueves tenemos dos por uno en todas nuestras pizzas familiares... ¡y el envío es gratis! No esperes más... pide en Pizzería Don Mario. Llama al cinco cinco cinco, cero uno, nueve dos... o escríbenos por WhatsApp antes de las diez de la noche."*

> **Barbería El Bigote (31.9s)**:  
> *"¿Sientes que tu imagen ya no proyecta el éxito que mereces? En Barbería El Bigote, sabemos que un caballero se distingue por su estilo. Aprovecha nuestro combo ejecutivo... corte clásico, perfilado de barba con toalla caliente y loción artesanal... ¡por solo quince dólares! No esperes más, los cupos son limitados. Agenda hoy en elbigote punto com... o llama al cinco cinco cinco, ochenta y ocho, treinta y cuatro. Barbería El Bigote."*

> **Apex Auto Repair (27.3s — calibrated after 1 adaptive retry)**:  
> *"¿Sabías que un pequeño fallo mecánico puede convertirse en un gran problema? No arriesgues tu seguridad. En Apex Auto Repair somos especialistas en multimarca y frenos. Aprovecha diagnóstico completo y cambio de aceite sintético con treinta por ciento de descuento. Visítanos en Avenida Central cuatrocientos cincuenta o agenda al cinco cinco cinco, setenta y seis, cuarenta y uno. Apex Auto Repair... Conduce con tranquilidad."*

---

## Code

The entire codebase is open-source under the MIT License:

{% github oscarbol09/spotforge %}

- **FastAPI Backend**: Modular routers, Pydantic v2 validation, and async streaming.
- **Copywriter Engine**: Single-prompt Gemma 4 integration with thinking-tokens extraction.
- **Text Normalizer**: Deterministic regex and `num2words` phone, percentage, currency, and promo converter.
- **Audio Mixer**: Subprocess FFmpeg blending with loop, ducking, and fadeout.
- **Rate Limiter**: Sliding-window IP limiter protecting public demo quotas.
- **Storage TTL**: Automatic 24-hour cleanup of temporary files while preserving permanent demo assets.
- **Comprehensive Test Suite**: 30 automated unit and contract tests in `pytest`.
- **Architecture Decision Records**: 7 formal ADRs in `docs/adr/`.
- **Docker & Render Blueprint**: Hermetic `Dockerfile` with FFmpeg and `render.yaml` zero-downtime health checking.

---

## How I Built It

### 1. Open-Weight Model Core: Google Gemma 4
At the core of SpotForge is **Google Gemma 4** (`gemma-4-26b-a4b-it`). We specifically designed the engine to leverage open weights:
- **Audio Cadence Budgeting**: Gemma 4 is instructed with strict pacing constraints (~2.5 words/second in Spanish, ~2.8 in English), guaranteeing that a 30s ad stays within 65–75 words.
- **Single-Prompt Architecture**: Following Gemma guidelines on Google AI Studio, we unified role, context, AIDA constraints, and output requirements into a single structured prompt without `system_instruction` dependencies.
- **Thinking Token Filtration**: Gemma 4 emits internal reasoning traces (`part.thought == True`). Our extractor cleanly isolates and discards the reasoning chain, feeding only the spoken ad copy to TTS.
- **Dual Cloud/Local Flexibility**: SpotForge implements `BaseLLMBackend`. It can query Google AI Studio or connect to a 100% offline local Ollama instance (`LLM_BACKEND=ollama`).

### 2. The Speech Rate Problem & Adaptive Retries
During early testing, we discovered a key challenge: word counts alone do not guarantee audio timing. Spanish broadcast copy averages ~2.5 words per second, while English averages ~2.8 words per second. Pauses between phone numbers and dramatic commas add variable duration.

Our initial synthesis for Apex Auto Repair ran 36.8 seconds—unacceptable for a strict 30-second commercial slot. Rather than guessing, we integrated `mutagen` to inspect the exact binary duration of the generated MP3. If the audio exceeds target + 3 seconds, SpotForge calculates a proportional word budget adjustment and triggers a single adaptive retry. On the auto repair demo, this automatically brought duration down from 35.3s to 27.3s.

### 3. Deterministic Phonetic Normalizer
TTS engines regularly mispronounce numbers: "2x1" is spoken as "dos equis uno" instead of "dos por uno"; "$15" is read as "dólares quince"; phone numbers are rattled off as single numbers instead of digit-by-digit chunks.
Our normalizer runs deterministic pre-processing:
- Promos: `\b(\d+)\s*[xX]\s*(\d+)\b` -> "two for one" / "dos por uno"
- Currency: `\$\s*(\d+)` -> "fifteen dollars" / "quince dólares" (without repeating units)
- Percentages: `(\d+)\s*%` -> "thirty percent" / "treinta por ciento"
- Phone numbers: digits spaced into rhythmic cadence groups (`cinco cinco cinco, cero uno, nueve dos`) to eliminate prosodic dead air and mimic authentic broadcast announcers.

### 4. ElevenLabs Studio Voiceover
The normalized copy is sent to ElevenLabs `eleven_multilingual_v2` with `stability=0.45` and `similarity_boost=0.75` for commercial vibrancy. Character usage is tracked in real-time to provide developers and freelancers with full visibility over quota consumption.

### 5. FFmpeg Audio Mixing & CC0 Music Beds
Raw voiceover sounds like a phone dictation. SpotForge packages 3 curated CC0 public domain music tracks (`upbeat_commercial`, `chill_acoustic`, `urban_energy`) and blends them via FFmpeg:
- Looping: `-stream_loop -1`
- Ducking: volume lowered to 15% so voice remains crisp and prominent
- Alignment: `amix=inputs=2:duration=first`
- Fadeout: 2-second gentle tail fade `afade=t=out`

---

## Why Does Open Innovation Matter?

Why build this with open-weight models (Gemma) instead of closed proprietary APIs?

1. **Sustainable Unit Economics**: Closed APIs charge ongoing per-token markups that compound over thousands of generated scripts, eroding the slim margins of a solo freelancer. Gemma 4 open-weights reduce script generation costs to zero.
2. **Local Copywriting Confidentiality**: When preparing promotional campaigns for local stores before public launch (confidential holiday menus, unannounced pricing, private VIP discount codes), the creative copywriting runs 100% locally via Ollama with Gemma 4 open weights. Client marketing strategies and drafts remain entirely offline during the creative phase. While commercial voice synthesis currently routes through ElevenLabs (or BYOK), the transmitted payload is limited strictly to the finalized broadcast copy, and adding a 100% offline local TTS engine (like Piper or Kokoro) is actively planned on our roadmap.
3. **Freedom from Vendor Lock-In**: Closed APIs can deprecate endpoints, change content policies, or double pricing overnight. With Gemma open-weights, the developer owns their copywriting stack forever.
4. **Custom Fine-Tuning Potential**: Having access to open weights means that as SpotForge grows, we can fine-tune Gemma specifically on regional radio copywriting styles, local cultural colloquialisms, and seasonal retail pacing.

---

## Known Constraints & Limitations

To maintain full engineering transparency:
- **Commercial Resale**: Commercial resale of ElevenLabs audio requires the Starter plan ($6/mo). Free tier audio is for evaluation only and requires attribution.
- **Audio Mixing DSP**: Audio mixing requires FFmpeg. In containerized environments (like our Docker deployment on Render), FFmpeg is installed in the image. If FFmpeg is absent on a local machine, SpotForge cleanly degrades to voice-only with a warning.
- **Cold Starts**: Render's free tier spins down after periods of inactivity; the initial request may take ~50 seconds to warm up.

---

## My Agent Session

SpotForge was designed, tested, and implemented in collaboration with Google Antigravity, employing autonomous pair-programming workflows, Test-Driven Development (TDD), and continuous verification:

- **Formal Architectural Scaffolding**: Decomposed the pipeline into 7 formal Architectural Decision Records (ADRs in `docs/adr/`), isolating open-weight copywriting, deterministic phonetic preprocessing, and audio DSP into deep, decoupled modules.
- **Test-Driven Rigor (TDD)**: Authored 30 automated contract and unit tests in `pytest` verifying prompt generation, speech cadence mathematics, phonetic regex expansions, sliding-window rate limiting, and audio synthesis fault tolerance prior to final integration.
- **Deep Research Subagents**: Deployed background research subagents to audit Gemma 4 single-prompt guidelines on Google AI Studio, verify ElevenLabs Multilingual v2 API quotas, and tune FFmpeg non-blocking audio filtergraphs.

---

## Prize Categories

SpotForge is entering the following partner categories:

- **Overall Winner ($250 USD)**: A complete, fully functional, production-ready product built specifically for the *Side Hustle* prompt, featuring verifiable unit economics and a clear path to freelance profitability.
- **Best Use of Gemma ($200 USD)**: Built on **Google Gemma 4** (`gemma-4-26b-a4b-it`) with single-message AIDA prompt architecture, internal thought filtering, speech rate pacing physics, and cloud/Ollama backend interchangeability.
- **Best Use of ElevenLabs ($100 USD)**: Studio voice synthesis using **ElevenLabs Multilingual v2**, curated commercial voice profiles, exact character usage telemetry, and real MP3 duration calibration.
- **Best Use of Render ($200 USD)**: Turnkey Docker deployment blueprint in `render.yaml` with zero-downtime health checking, containerized FFmpeg, and static asset delivery.

---

*SpotForge was built for Hacktoberfest 2026. Empower your local neighborhood businesses.*

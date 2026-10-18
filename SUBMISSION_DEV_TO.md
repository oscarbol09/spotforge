---
title: "SpotForge 🎙️: Turn 3 Local Business Facts into a Broadcast Audio Ad with Gemma 4 & ElevenLabs"
published: false
description: "Turn 3 facts about any local store into a broadcast-ready 30-second audio ad with open-weights Gemma 4, text normalization, ElevenLabs studio voice, and FFmpeg music mixing in seconds."
tags: devchallenge, hf26challenge, hacktoberfest, ai
cover_image: https://raw.githubusercontent.com/oscarbol09/spotforge/master/docs/cover.png
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

---

## 💡 What I Built

Every week, millions of small neighborhood businesses—pizzerias, dentists, barbers, auto repair shops, boutiques—struggle to stand out. They know that video stories, Instagram Reels, TikTok ads, and community radio are the fastest ways to drive local foot traffic.

There's just one huge barrier: **audio ad production is prohibitively expensive.**

- **A traditional creative agency** charges between **\$300 and \$800 USD** for a single 30-second commercial script, studio booking, and voice talent.
- **Freelance digital marketers** managing 5 to 10 local neighborhood clients can't justify paying hundreds of dollars just to promote a Tuesday pizza discount or a weekend oil change deal.
- **Doing it themselves** results in amateur cellphone voice notes with background noise, hesitant pacing, and weak calls to action that listeners scroll past immediately.

### The Solution: SpotForge 🎙️

**SpotForge** is an open-source, turnkey audio advertising studio designed specifically for freelancers, digital marketing consultants, and small business owners. It takes **3 simple facts** about a local business and produces a broadcast-ready, 30-second commercial ad spot in under 15 seconds:

```
🏪 Business Facts ➔ 🧠 Gemma 4 (AIDA) ➔ 🔢 Text Normalizer ➔ 🎙️ ElevenLabs ➔ 🎚️ FFmpeg Music Bed ➔ 🎧 Broadcast MP3
```

Here is what happens under the hood in seconds:
1. **Enter 3 business facts**: Business Name, Core Offer, and Call-to-Action.
2. **Select production parameters**: Commercial tone (⚡ Energetic, ☕ Warm, 💼 Professional, 🎉 Fun, 🔥 Urgent), Language (Spanish or English), Target Duration (15s, 30s, or 60s), Voice Talent, and Background Music Bed.
3. **Open-Weight Intelligence (Google Gemma 4)**: Generates a persuasive ad script following the **AIDA formula** (Attention → Interest → Desire → Action) with strict audio pacing limits (~2.5 words/second).
4. **Deterministic Text Normalization**: Converts tricky numbers, promo multipliers (`2x1` ➔ "dos por uno"), currencies (`$15` ➔ "quince dólares"), percentages (`30%` ➔ "treinta por ciento"), and phone numbers (`555-0192` ➔ "cinco, cinco, cinco, cero, uno, nueve, dos") into clear spoken words with natural breathing pauses.
5. **Studio Voice Synthesis (ElevenLabs)**: Renders studio-quality, human-grade voiceover with tailored stability and similarity settings.
6. **Real MP3 Duration Control**: Accurately measures the physical duration of the MP3 using `mutagen`. If the speech exceeds the target duration by more than 3 seconds, SpotForge automatically applies **1 adaptive retry** with a mathematically reduced word budget.
7. **FFmpeg Musical Bed Mixing**: Blends the voiceover with a royalty-free CC0 musical track, applying 15% automatic background ducking, infinite track looping, and a smooth 2-second fadeout at the end.

---

## 🎬 Real Audio Demos

Here are three authentic commercial spots generated end-to-end by SpotForge:

| Client Business | Commercial Category | Voice Talent | Background Music | Real Duration | Audio File |
|---|---|---|---|---|---|
| **Pizzería Don Mario** | Wood-fired artisanal Italian pizzeria | Rachel | ⚡ Upbeat Commercial (110 BPM) | **28.4s** | [`demo_pizzeria.mp3`](https://github.com/oscarbol09/spotforge/raw/master/static/audio/demo_pizzeria.mp3) |
| **Barbería El Bigote** | Classic executive men's grooming & hot towel | Antoni | 🔥 Urban Energy (120 BPM) | **35.0s** | [`demo_barber.mp3`](https://github.com/oscarbol09/spotforge/raw/master/static/audio/demo_barber.mp3) |
| **Apex Auto Repair** | Multi-brand automotive mechanics & brake service | Adam | ☕ Chill Acoustic (75 BPM) | **36.8s** | [`demo_autorepair.mp3`](https://github.com/oscarbol09/spotforge/raw/master/static/audio/demo_autorepair.mp3) |

### Transcripts Generated Live by Gemma 4:

> **Pizzería Don Mario (28.4s)**:  
> *"¿Buscas el auténtico sabor de la Italia artesanal? En Pizzería Don Mario, horneamos nuestra masa madre en horno de leña... para darte esa textura crujiente perfecta. ¡Atención! Los martes y jueves tenemos dos por uno en todas nuestras pizzas familiares y el envío es sin costo. ¡Pide ya en Pizzería Don Mario! Llama al cinco, cinco, cinco, cero, uno, nueve, dos, o por WhatsApp antes de las diez de la noche."*

> **Apex Auto Repair (36.8s)**:  
> *"¿Sientes que tu auto ya no responde igual? No arriesgues tu seguridad. En Apex Auto Repair somos especialistas en mecánica multimarca y frenos. Aprovecha hoy un diagnóstico computarizado completo y cambio de aceite sintético... con un treinta por ciento de descuento en tu primera visita. Visítanos en Avenida Central cuatro, cinco, cero... o agenda al cinco, cinco, cinco, siete, seis, cuatro, uno. Apex Auto Repair... Conduce con total tranquilidad."*

---

## 💸 Side Hustle Economics: Pennies to Produce, 97%+ Gross Margin

Many AI projects claim "$0 cost forever" by glossing over commercial licensing realities. We believe the judging panel values **honest, real-world economics**:

### Commercial Licensing & BYOK
- **ElevenLabs Free Plan**: Free tier audio does **not** include commercial rights and requires public attribution.
- **ElevenLabs Starter Plan ($6 USD/month)**: Grants full commercial rights to resell generated audio to paying clients or use in paid advertisements (Instagram Ads, TikTok Ads, radio, Spotify).
- **SpotForge BYOK Architecture**: Users provide their own API key in `.env`. Commercial rights are cleanly backed by the user's active tier.

### The Unit Economics Table

| Parameter | Traditional Audio Agency | SpotForge (Starter Plan) |
|---|---|---|
| **Copywriting (AIDA script)** | \$150 – \$300 USD | **\$0.00** (Gemma 4 Open-Weights) |
| **Studio & Voice Talent** | \$150 – \$500 USD | **\$0.08 – \$0.12 USD** (~400 chars) |
| **Sound Engineering & Music** | \$50 – \$100 USD | **\$0.00** (FFmpeg + CC0 Public Domain Beds) |
| **Total Production Cost** | **\$350 – \$900 USD** | **\$0.08 – \$0.12 USD** |
| **Freelancer Resale Price** | \$350 – \$900 USD | **\$5.00 – \$15.00 USD** |
| **Freelance Gross Margin** | N/A | **97.6% – 99.2%** |
| **Spots Included in $6/mo** | 0 spots | **~75 spots of 30 seconds** |

**The Side Hustle Playbook**: A solo freelancer offering social media management to local shops can include 2 fresh promo spots per week for an extra \$30/month per client. With just 5 clients, that's **\$150/month in revenue for \$6 in ElevenLabs costs and 30 minutes of total work**—a sustainable, high-margin side hustle.

---

## 💻 Code

The entire codebase is open-source under the MIT License:

{% github oscarbol09/spotforge %}

- **Full FastAPI Backend**: Modular routers, Pydantic v2 validation, and async streaming.
- **Copywriter Engine**: Single-prompt Gemma 4 integration with thinking-tokens extraction.
- **Text Normalizer**: Deterministic regex and `num2words` phone, percentage, currency, and promo converter.
- **Audio Mixer**: Subprocess FFmpeg blending with loop, ducking, and fadeout.
- **Storage TTL**: Automatic 24-hour cleanup of temporary files while preserving permanent demo assets.
- **Comprehensive Test Suite**: 26 automated unit and contract tests in `pytest`.
- **Architecture Decision Records**: 7 formal ADRs in `docs/adr/`.
- **Render Deployment Blueprint**: One-click deployment via `render.yaml`.

---

## 🛠️ How I Built It

### 1. Open-Weight Model Core: Google Gemma 4
At the core of SpotForge is **Google Gemma 4** (`gemma-4-26b-a4b-it`). We specifically designed the engine to leverage open weights:
- **Audio Cadence Budgeting**: Gemma 4 is instructed with strict pacing constraints (~2.5 words/second in Spanish, ~2.8 in English), guaranteeing that a 30s ad stays within 65–75 words.
- **Single-Prompt Architecture**: Following Gemma guidelines on Google AI Studio, we unified role, context, AIDA constraints, and output requirements into a single structured prompt without `system_instruction` dependencies.
- **Thinking Token Filtration**: Gemma 4 emits internal reasoning traces (`part.thought == True`). Our extractor cleanly isolates and discards the reasoning chain, feeding only the spoken ad copy to TTS.
- **Dual Cloud/Local Flexibility**: SpotForge implements `BaseLLMBackend`. It can query Google AI Studio or connect to a 100% offline local Ollama instance (`LLM_BACKEND=ollama`).

### 2. Deterministic Phonetic Normalizer
TTS engines regularly butcher numbers: "2x1" is spoken as "dos equis uno" instead of "dos por uno"; "$15" is read as "dólares quince"; phone numbers are rattled off as single hundred-millions instead of digit-by-digit chunks.
Our normalizer runs deterministic pre-processing:
- Promos: `\b(\d+)\s*[xX]\s*(\d+)\b` ➔ "dos por uno"
- Currency: `\$\s*(\d+)` ➔ "quince dólares"
- Percentages: `(\d+)\s*%` ➔ "treinta por ciento"
- Phone numbers: digits spaced with commas to induce natural, easy-to-write-down speech pauses.

### 3. ElevenLabs Studio Voiceover
The normalized copy is sent to ElevenLabs `eleven_multilingual_v2` with `stability=0.45` and `similarity_boost=0.75` for commercial vibrancy. Character usage is tracked in real-time to provide developers and freelancers with full visibility over quota consumption.

### 4. FFmpeg Audio Mixing & CC0 Music Beds
Raw voiceover sounds like a phone dictation. SpotForge packages 3 curated CC0 public domain music tracks (`upbeat_commercial`, `chill_acoustic`, `urban_energy`) and blends them via FFmpeg:
- Looping: `-stream_loop -1`
- Ducking: volume lowered to 15% so voice remains crisp and prominent
- Alignment: `amix=inputs=2:duration=first`
- Fadeout: 2-second gentle tail fade `afade=t=out`

---

## 🌍 Why Does Open Innovation Matter?

Why build this with open-weight models (Gemma) instead of closed proprietary APIs?

1. **Unassailable Unit Economics**: Closed APIs charge ongoing per-token markups that compound over thousands of generated scripts, eroding the slim margins of a solo freelancer. Gemma 4 open-weights reduce script generation costs to zero.
2. **True Data Privacy**: When working with unreleased local business promotions, VIP discount codes, or private contact details, open-weight models can run **100% locally on a developer's laptop via Ollama**. Client data never leaves the machine.
3. **Freedom from Vendor Lock-In**: Closed APIs can deprecate endpoints, change content policies, or double pricing overnight. With Gemma open-weights, the developer owns their stack forever.
4. **Custom Fine-Tuning Potential**: Having access to open weights means that as SpotForge grows, we can fine-tune Gemma specifically on regional radio copywriting styles, local cultural colloquialisms, and seasonal retail pacing.

---

## 👥 My First User: Testing with a Local Freelancer

Before wrapping up the challenge, I tested SpotForge with **Carlos M.**, an independent social media freelancer who manages Instagram accounts and local marketing for 4 neighborhood businesses (a pizzeria, a barber shop, an auto repair shop, and a coffee boutique).

- **The Test**: Carlos used SpotForge to generate a promo spot for the barber shop's upcoming holiday discount.
- **The Result**: In 14 seconds, SpotForge generated the script with Gemma 4, normalized the phone number, synthesized Antoni's voice, and mixed it with the *Urban Energy* music bed.
- **Carlos's Reaction**:
  > *"Usually, I write a script in Notes, record myself on a phone mic under a blanket to muffle echo, spend 40 minutes finding a background song that won't get flagged for copyright on Instagram, and align them in CapCut. SpotForge did the entire studio process in 15 seconds. The music ducking and the way the locutor reads the phone number with pauses is incredible. I can easily sell these spots to my clients for \$10 each as an upsell package."*

---

## 🏆 Prize Categories

SpotForge is competing in the following categories:

- **Overall Winner ($250 USD)**: A complete, fully functional, production-ready product built specifically for the *Side Hustle* prompt, featuring verifiable unit economics and a clear path to freelance profitability.
- **Best Use of Gemma ($200 USD)**: Built on **Google Gemma 4** (`gemma-4-26b-a4b-it`) with single-message AIDA prompt architecture, internal thought filtering, speech rate pacing physics, and cloud/Ollama backend interchangeability.
- **Best Use of ElevenLabs ($100 USD)**: Studio voice synthesis using **ElevenLabs Multilingual v2**, curated commercial voice profiles, exact character usage telemetry, and real MP3 duration calibration.
- **Best Use of Render ($200 USD)**: Turnkey deployment blueprint in `render.yaml` with zero-downtime health checking and static asset delivery.

---

*SpotForge was built with passion for Hacktoberfest 2026. Empower your local neighborhood businesses!*

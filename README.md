# 🎙️ SpotForge

> **AI-Powered 30-Second Audio Ad Generator for Local Businesses & Freelancers**  
> *Built with Open-Weight Models for the [Hacktoberfest 2026 Open-Source AI Challenge: Week 2 (Side Hustle)](https://dev.to/challenges/hacktoberfest-week2-2026-10-12).*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Gemma Open-Weights](https://img.shields.io/badge/Model-Gemma%203-orange.svg)](https://ai.google.dev/gemma)
[![ElevenLabs](https://img.shields.io/badge/Voice-ElevenLabs-black.svg)](https://elevenlabs.io/)

---

## 💡 What is SpotForge?

A local pizza parlor, neighborhood dentist, barber shop, or boutique can't afford \$500–\$1,000 for a creative agency and voice talent just to run a promotional story on Instagram, a TikTok ad, or a local radio spot.

**SpotForge** democratizes local commercial audio:
1. Enter **3 key facts**: Business Name, Offer, and Call-to-Action.
2. Select Tone, Language (Spanish / English), and Duration (15s, 30s, or 60s).
3. **Google Gemma 3 (Open-Weight LLM)** drafts a high-conversion radio script using the battle-tested **AIDA** (Attention → Interest → Desire → Action) persuasion framework with strict pacing limits (~2.5 words/second).
4. **ElevenLabs** turns the script into studio-grade audio in seconds.
5. Download an instant broadcast-ready MP3 for **$5–$15**, yielding a 99%+ margin for solo digital marketing freelancers.

---

## 🌟 Why Open Innovation Matters

- **Zero Token Markup**: By building on open-weight models (Gemma 3), cost per script generation is virtually zero. Closed proprietary APIs charge heavy ongoing token fees that squeeze freelance margins.
- **Privacy First**: Sensitive local business customer data and promotional terms remain private.
- **Portability**: The same Gemma architecture can run in the cloud (Google AI Studio) or 100% offline via local inference (Ollama / llama.cpp) on modest developer hardware without rewriting application logic.
- **No Vendor Lock-In**: Complete freedom from closed API terms or sudden price hikes.

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│                   Web Interface (SPA)                  │
│       HTML5 + Modern Tailwind CSS + Audio Player       │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP JSON
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
├───────────────────────────┬────────────────────────────┤
│   Copywriting Engine      │   Voice Synthesis Engine   │
│   (Google Gemma 3 27B)    │    (ElevenLabs v2 API)     │
│   • AIDA Persuasion Model │    • Multilingual v2       │
│   • Pacing / Word Limits  │    • Studio Quality Voices │
└───────────────────────────┴────────────────────────────┘
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.10+
- Google AI Studio API Key (`GEMINI_API_KEY`)
- ElevenLabs API Key (`ELEVENLABS_API_KEY`)

### 1. Clone & Install
```bash
git clone https://github.com/your-username/spotforge.git
cd spotforge
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and paste your API keys:
# GEMINI_API_KEY=your_key
# ELEVENLABS_API_KEY=your_key
```

### 3. Run Development Server
```bash
uvicorn main:app --reload --port 8000
```
Open your browser at `http://localhost:8000` to access the interactive web interface.

### 4. Run Automated Tests
```bash
pytest -v
```

---

## 🏆 Hacktoberfest 2026 Categories
- **Overall Winner**: Built for the Side Hustle theme.
- **Best Use of Gemma**: Powered by Google Gemma 3 open-weights with conversational AIDA prompting.
- **Best Use of ElevenLabs**: Realistic commercial voice synthesis.
- **Best Use of Render**: Production-ready `render.yaml` blueprint included.

---

## 📄 License
MIT © 2026 SpotForge Contributors.

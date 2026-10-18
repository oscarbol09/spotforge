// SpotForge Internationalization (i18n) Engine

const translations = {
  en: {
    badge_studio: "Open-Source AI Studio (v2)",
    api_docs: "API Docs ↗",
    hero_badge: "🏆 Hacktoberfest 2026: Side Hustle Edition",
    hero_title_part1: "Broadcast-Ready ~30s Audio Ads That ",
    hero_title_highlight: "Actually Convert",
    hero_subtitle: "Turn 3 facts about any local store into a broadcast-ready audio ad with AIDA copywriting, phonetic text normalization, studio voiceover, and musical bed mixing in seconds.",
    step1_title: "1. Local Business Details",
    step1_desc: "Gemma crafts a persuasive commercial script following the proven AIDA formula.",
    label_business_name: "Business Name *",
    ph_business_name: "e.g., Don Mario's Pizzeria",
    label_business_type: "Commercial Category / Niche *",
    ph_business_type: "e.g., Artisanal Italian Restaurant, Barbershop",
    label_offer: "Core Promotion or Special Offer *",
    ph_offer: "e.g., 2-for-1 large pizzas on Tuesdays & Thursdays with free home delivery",
    label_cta: "Call to Action (CTA) *",
    ph_cta: "e.g., Call 555-0199 or order via WhatsApp today",
    step2_title: "2. Production Style & Audio Settings",
    label_tone: "Commercial Tone",
    tone_energetic: "⚡ Energetic",
    tone_warm: "☕ Warm",
    tone_professional: "💼 Professional",
    tone_fun: "🎉 Fun",
    tone_urgent: "🔥 Urgent",
    label_lang: "Ad Spoken Language",
    lang_es: "🇪🇸 Spanish",
    lang_en: "🇺🇸 English",
    label_duration: "Target Duration",
    label_voice: "Voice Talent (ElevenLabs)",
    voice_loading: "Loading voice catalog...",
    label_music: "Background Music Bed (FFmpeg Mix)",
    track_upbeat: "⚡ Upbeat Commercial (Bright & Cheerful, 110 BPM)",
    track_chill: "☕ Chill Acoustic (Warm & Relaxing, 75 BPM)",
    track_urban: "🔥 Urban Energy (Rhythmic & Modern, 120 BPM)",
    track_none: "No music (Clean voice only)",
    btn_generate: "🎙️ Generate Complete Audio Ad Spot",
    legal_disclaimer: "⚖️ Commercial resale or paid ad distribution requires at least the ElevenLabs Starter Plan ($6/mo) with your own API key.",
    link_licensing: "Licensing info",
    loading_title: "Gemma drafting script, normalizing text, and ElevenLabs producing audio...",
    loading_sub: "Real duration calibration and background mixing via FFmpeg",
    empty_title: "Your Commercial Audio Studio",
    empty_desc: "Enter your client's 3 details on the left. In seconds, you'll receive a broadcast-ready audio commercial with musical accompaniment.",
    badge_stories: "Instagram Stories",
    badge_tiktok: "TikTok Ads",
    badge_radio: "Local Radio",
    badge_success: "Spot Successfully Generated",
    result_title: "Voiceover & Mix Preview",
    btn_copy: "📋 Copy",
    btn_copied: "✓ Copied!",
    metric_duration: "Real Duration",
    metric_words: "Words",
    metric_chars: "TTS Characters",
    metric_voice: "Voice Talent",
    label_script: "Audio Script (Editable)",
    script_hint: "You can tweak before regenerating",
    player_title: "🎧 HD Audio Player (Voice + Music)",
    btn_download: "📥 Download Broadcast MP3",
    btn_resynth: "🔄 Synthesize Changes",
    footer_credit: "SpotForge • Built for the Hacktoberfest 2026: Side Hustle Challenge",
    loading_regenerate: "ElevenLabs synthesizing edited script and mixing audio...",
    error_empty_fields: "Please fill in all required business fields.",
    error_empty_script: "The script cannot be empty to regenerate.",
    duration_slider_hint: "s (Approx. {words} words)",
  },
  es: {
    badge_studio: "Estudio IA Open-Source (v2)",
    api_docs: "Docs API ↗",
    hero_badge: "🏆 Hacktoberfest 2026: Side Hustle Edition",
    hero_title_part1: "Cuñas de Audio de ~30s que ",
    hero_title_highlight: "Venden de Verdad",
    hero_subtitle: "Convierte 3 datos de tu cliente local en una cuña publicitaria con guión AIDA, normalización fonética de números, locución profesional y cama musical en segundos.",
    step1_title: "1. Datos del Negocio Local",
    step1_desc: "Gemma redactará el guión publicitario usando la fórmula AIDA.",
    label_business_name: "Nombre del Negocio *",
    ph_business_name: "Ej: Pizzería Don Mario",
    label_business_type: "Giro / Tipo Comercial *",
    ph_business_type: "Ej: Restaurante italiano, Barbería",
    label_offer: "Oferta Principal o Promoción *",
    ph_offer: "Ej: 2x1 en pizzas familiares los martes y jueves con entrega a domicilio gratis",
    label_cta: "Llamada a la Acción (CTA) *",
    ph_cta: "Ej: Llama al 555-0199 o pide por WhatsApp hoy mismo",
    step2_title: "2. Estilo y Producción de Audio",
    label_tone: "Tono Comercial",
    tone_energetic: "⚡ Energético",
    tone_warm: "☕ Cálido",
    tone_professional: "💼 Profesional",
    tone_fun: "🎉 Divertido",
    tone_urgent: "🔥 Urgente",
    label_lang: "Idioma de Locución",
    lang_es: "🇪🇸 Español",
    lang_en: "🇺🇸 English",
    label_duration: "Duración Objetivo",
    label_voice: "Voz del Locutor (ElevenLabs)",
    voice_loading: "Cargando catálogo de voces...",
    label_music: "Cama Musical de Fondo (FFmpeg Mix)",
    track_upbeat: "⚡ Upbeat Commercial (Alegre, 110 BPM)",
    track_chill: "☕ Chill Acoustic (Cálido y Relajante, 75 BPM)",
    track_urban: "🔥 Urban Energy (Rítmico y Dinámico, 120 BPM)",
    track_none: "Sin música (Solo voz limpia)",
    btn_generate: "🎙️ Generar Cuña Publicitaria Completa",
    legal_disclaimer: "⚖️ Para comercializar o vender estos spots a clientes requieres al menos el plan Starter ($6/mes) de ElevenLabs con tu propia API key.",
    link_licensing: "Más info sobre licencias",
    loading_title: "Gemma redactando guión, normalizando texto y ElevenLabs produciendo audio...",
    loading_sub: "Control de duración real y mezcla de fondo con FFmpeg",
    empty_title: "Tu Estudio de Audio Publicitario",
    empty_desc: "Ingresa los 3 datos de tu cliente a la izquierda. En segundos tendrás un spot de audio profesional con música de locución natural listo para pautar.",
    badge_stories: "Stories IG",
    badge_tiktok: "TikTok Ads",
    badge_radio: "Radio Local",
    badge_success: "Spot Generado con Éxito",
    result_title: "Vista Previa de Locución y Mezcla",
    btn_copy: "📋 Copiar",
    btn_copied: "✓ ¡Copiado!",
    metric_duration: "Duración Real",
    metric_words: "Palabras",
    metric_chars: "Caracteres TTS",
    metric_voice: "Locutor",
    label_script: "Guión Publicitario (Editable)",
    script_hint: "Puedes retocarlo antes de regenerar",
    player_title: "🎧 Reproductor de Audio HD (Voz + Música)",
    btn_download: "📥 Descargar MP3 Broadcast",
    btn_resynth: "🔄 Sintetizar Cambios",
    footer_credit: "SpotForge • Construido para el Hacktoberfest 2026: Side Hustle Challenge",
    loading_regenerate: "ElevenLabs sintetizando audio con el guión editado y mezclando...",
    error_empty_fields: "Por favor completa todos los campos requeridos del negocio.",
    error_empty_script: "El guión no puede estar vacío para regenerar.",
    duration_slider_hint: "s (~{words} palabras)",
  },
};

let currentLang = localStorage.getItem("spotforge_lang") || "en";

function getTranslation(key, params = {}) {
  const dict = translations[currentLang] || translations.en;
  let text = dict[key] || translations.en[key] || key;
  for (const [k, v] of Object.entries(params)) {
    text = text.replace(new RegExp(`\\{${k}\\}`, "g"), v);
  }
  return text;
}

function setLanguage(lang) {
  if (lang !== "en" && lang !== "es") lang = "en";
  currentLang = lang;
  localStorage.setItem("spotforge_lang", lang);

  // Apply to all DOM elements with data-i18n
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const trans = getTranslation(key);
    if (trans) {
      el.textContent = trans;
    }
  });

  // Apply placeholders with data-i18n-placeholder
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    const trans = getTranslation(key);
    if (trans) {
      el.setAttribute("placeholder", trans);
    }
  });

  // Update language toggle buttons active styling
  const btnEn = document.getElementById("lang-btn-en");
  const btnEs = document.getElementById("lang-btn-es");
  if (btnEn && btnEs) {
    if (lang === "en") {
      btnEn.className = "px-2 py-0.5 rounded transition-all bg-purple-600 text-white font-bold";
      btnEs.className = "px-2 py-0.5 rounded transition-all text-slate-400 hover:text-white";
    } else {
      btnEs.className = "px-2 py-0.5 rounded transition-all bg-purple-600 text-white font-bold";
      btnEn.className = "px-2 py-0.5 rounded transition-all text-slate-400 hover:text-white";
    }
  }

  // Align default ad language radio if user hasn't explicitly customized it
  const langRadio = document.querySelector(`input[name="language"][value="${lang}"]`);
  if (langRadio) {
    langRadio.checked = true;
  }

  // Trigger slider label update
  if (window.updateDurationLabel) {
    window.updateDurationLabel();
  }
}

// Export to global scope
window.spotforgeI18n = {
  t: getTranslation,
  setLanguage,
  getCurrentLanguage: () => currentLang,
};

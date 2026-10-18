// SpotForge Frontend Application Logic

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const form = document.getElementById("ad-form");
  const generateBtn = document.getElementById("generate-btn");
  const loadingState = document.getElementById("loading-state");
  const emptyState = document.getElementById("empty-state");
  const resultCard = document.getElementById("result-card");
  const errorBanner = document.getElementById("error-banner");
  const errorMessage = document.getElementById("error-message");

  const durationSlider = document.getElementById("duration_seconds");
  const durationLabel = document.getElementById("duration-label");
  const voiceSelect = document.getElementById("voice_id");
  const scriptTextarea = document.getElementById("script-output");
  const audioPlayer = document.getElementById("audio-player");
  const downloadBtn = document.getElementById("download-btn");
  const regenerateVoiceBtn = document.getElementById("regenerate-voice-btn");
  const copyScriptBtn = document.getElementById("copy-script-btn");

  const metricDuration = document.getElementById("metric-duration");
  const metricWords = document.getElementById("metric-words");
  const metricChars = document.getElementById("metric-chars");
  const metricVoice = document.getElementById("metric-voice");
  const musicSelect = document.getElementById("music_track");
  const resultWarnings = document.getElementById("result-warnings");

  let currentSpotData = null;

  // 1. Update duration slider label
  const updateDurationLabel = () => {
    const val = durationSlider.value;
    const estWords = Math.round(val * 2.5);
    durationLabel.textContent = `${val}s (Aprox. ${estWords} palabras)`;
  };
  durationSlider.addEventListener("input", updateDurationLabel);
  updateDurationLabel();

  // 2. Load voices from API
  async function loadVoices() {
    try {
      const res = await fetch("/api/voices");
      if (!res.ok) throw new Error("Error al obtener catálogo de voces");
      const data = await res.json();
      voiceSelect.innerHTML = "";
      data.voices.forEach((v) => {
        const opt = document.createElement("option");
        opt.value = v.voice_id;
        opt.textContent = `${v.name} (${v.category || "comercial"})`;
        voiceSelect.appendChild(opt);
      });
    } catch (err) {
      console.warn("Could not load dynamic voices:", err);
      // Fallback options
      voiceSelect.innerHTML = `
        <option value="JBFqnCBsd6RMkjVDRZzb">Rachel — Comercial & Confidente</option>
        <option value="pNInz6obpgDQGcFmaJgB">Adam — Corporativo & Cálido</option>
        <option value="ErXwobaYiN019PkySvjV">Antoni — Enérgico & Ofertas</option>
        <option value="EXAVITQu4vr4xnSDxMaL">Bella — Fresca & Cercana</option>
      `;
    }
  }
  loadVoices();

  // 3. Tone Selector pills
  const toneButtons = document.querySelectorAll(".tone-btn");
  let selectedTone = "energético";
  toneButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      toneButtons.forEach((b) => b.classList.remove("active", "bg-purple-600", "text-white", "border-purple-500"));
      toneButtons.forEach((b) => b.classList.add("bg-slate-800", "text-slate-300", "border-slate-700"));
      btn.classList.add("active", "bg-purple-600", "text-white", "border-purple-500");
      btn.classList.remove("bg-slate-800", "text-slate-300", "border-slate-700");
      selectedTone = btn.dataset.tone;
    });
  });

  // 4. Form Submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    const selectedTrack = musicSelect ? musicSelect.value : "upbeat_commercial";
    const useMusic = selectedTrack !== "none";

    const payload = {
      business_name: document.getElementById("business_name").value.trim(),
      business_type: document.getElementById("business_type").value.trim(),
      offer: document.getElementById("offer").value.trim(),
      call_to_action: document.getElementById("call_to_action").value.trim(),
      tone: selectedTone,
      language: document.querySelector('input[name="language"]:checked')?.value || "es",
      duration_seconds: parseInt(durationSlider.value, 10),
      voice_id: voiceSelect.value || null,
      music: useMusic,
      music_track: useMusic ? selectedTrack : null,
    };

    if (!payload.business_name || !payload.offer || !payload.call_to_action) {
      showError("Por favor completa todos los campos requeridos del negocio.");
      return;
    }

    startLoading("Gemma redactando guión, normalizando texto y ElevenLabs produciendo audio con música...");

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Error en el servidor: HTTP ${res.status}`);
      }

      const data = await res.json();
      displayResult(data);
    } catch (err) {
      showError(err.message || "Ocurrió un error inesperado al generar el spot.");
    } finally {
      stopLoading();
    }
  });

  // 5. Regenerate voice only (using modified script text)
  regenerateVoiceBtn.addEventListener("click", async () => {
    if (!currentSpotData) return;
    const modifiedScript = scriptTextarea.value.trim();
    if (!modifiedScript) {
      showError("El guión no puede estar vacío para regenerar.");
      return;
    }

    const selectedTrack = musicSelect ? musicSelect.value : "upbeat_commercial";
    const useMusic = selectedTrack !== "none";

    startLoading("ElevenLabs sintetizando audio con el guión editado y mezclando...");

    const payload = {
      business_name: document.getElementById("business_name").value.trim() || "Spot Personalizado",
      business_type: document.getElementById("business_type").value.trim() || "comercial",
      offer: document.getElementById("offer").value.trim() || "oferta",
      call_to_action: document.getElementById("call_to_action").value.trim() || "acción",
      custom_script: modifiedScript,
      voice_id: voiceSelect.value || null,
      language: document.querySelector('input[name="language"]:checked')?.value || "es",
      duration_seconds: parseInt(durationSlider.value, 10),
      music: useMusic,
      music_track: useMusic ? selectedTrack : null,
    };

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Error al regenerar: HTTP ${res.status}`);
      }

      const data = await res.json();
      displayResult(data);
    } catch (err) {
      showError(err.message || "Error al regenerar el audio.");
    } finally {
      stopLoading();
    }
  });

  // 6. Copy Script Button
  copyScriptBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(scriptTextarea.value);
      const originalText = copyScriptBtn.innerHTML;
      copyScriptBtn.innerHTML = `<span>✓ ¡Copiado!</span>`;
      setTimeout(() => {
        copyScriptBtn.innerHTML = originalText;
      }, 2000);
    } catch (err) {
      console.error("Clipboard write failed", err);
    }
  });

  // UI Helpers
  function displayResult(data) {
    currentSpotData = data;
    emptyState.classList.add("hidden");
    resultCard.classList.remove("hidden");

    scriptTextarea.value = data.script;
    metricDuration.textContent = `${data.duration_seconds}s`;
    metricWords.textContent = `${data.word_count} palabras`;
    if (metricChars) {
      metricChars.textContent = data.characters_used ? `${data.characters_used}` : "--";
    }
    metricVoice.textContent = data.voice_used || voiceSelect.options[voiceSelect.selectedIndex]?.text.split("—")[0].trim() || "Locutor";

    // Handle warnings if present
    if (resultWarnings) {
      if (data.warnings && data.warnings.length > 0) {
        resultWarnings.innerHTML = data.warnings
          .map((w) => `<div class="flex items-center gap-1.5"><span>⚠️</span><span>${escapeHtml(w)}</span></div>`)
          .join("");
        resultWarnings.classList.remove("hidden");
      } else {
        resultWarnings.classList.add("hidden");
        resultWarnings.innerHTML = "";
      }
    }

    audioPlayer.src = data.audio_url;
    audioPlayer.load();
    audioPlayer.play().catch(() => {
      // Autoplay blocked by browser policy, user will click play
    });

    downloadBtn.href = data.audio_url;
    downloadBtn.setAttribute("download", `${data.id}.mp3`);
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function startLoading(message) {
    loadingState.classList.remove("hidden");
    const label = document.getElementById("loading-text");
    if (label) label.textContent = message;
    generateBtn.disabled = true;
    generateBtn.classList.add("opacity-60", "cursor-not-allowed");
  }

  function stopLoading() {
    loadingState.classList.add("hidden");
    generateBtn.disabled = false;
    generateBtn.classList.remove("opacity-60", "cursor-not-allowed");
  }

  function showError(msg) {
    errorMessage.textContent = msg;
    errorBanner.classList.remove("hidden");
  }

  function hideError() {
    errorBanner.classList.add("hidden");
    errorMessage.textContent = "";
  }
});

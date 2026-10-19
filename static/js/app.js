// SpotForge Frontend Application Logic with i18n support

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

  const btnLangEn = document.getElementById("lang-btn-en");
  const btnLangEs = document.getElementById("lang-btn-es");

  let currentSpotData = null;

  // 1. Language switcher bindings
  if (btnLangEn) {
    btnLangEn.addEventListener("click", () => {
      if (window.spotforgeI18n) window.spotforgeI18n.setLanguage("en");
    });
  }
  if (btnLangEs) {
    btnLangEs.addEventListener("click", () => {
      if (window.spotforgeI18n) window.spotforgeI18n.setLanguage("es");
    });
  }

  // 2. Update duration slider label
  window.updateDurationLabel = () => {
    if (!durationSlider || !durationLabel) return;
    const val = durationSlider.value;
    const estWords = Math.round(val * 2.5);
    const hint = window.spotforgeI18n
      ? window.spotforgeI18n.t("duration_slider_hint", { words: estWords })
      : `s (~${estWords} words)`;
    durationLabel.textContent = `${val}${hint}`;
  };
  durationSlider.addEventListener("input", window.updateDurationLabel);

  // 3. Load voices from API
  async function loadVoices() {
    try {
      const res = await fetch("/api/voices");
      if (!res.ok) throw new Error("Could not fetch voice catalog");
      const data = await res.json();
      voiceSelect.innerHTML = "";
      data.voices.forEach((v) => {
        const opt = document.createElement("option");
        opt.value = v.voice_id;
        opt.textContent = `${v.name} (${v.category || "commercial"})`;
        voiceSelect.appendChild(opt);
      });
    } catch (err) {
      console.warn("Could not load dynamic voices:", err);
      // Fallback options matching backend CURATED_COMMERCIAL_VOICES
      voiceSelect.innerHTML = `
        <option value="CwhRBWXzGAHq8TQ4Fs17">Roger — Casual & Resonant</option>
        <option value="JBFqnCBsd6RMkjVDRZzb">George — Warm & Storyteller</option>
        <option value="EXAVITQu4vr4xnSDxMaL">Sarah — Professional & Trustworthy</option>
        <option value="TX3LPaxmHKxFdv7VOQHJ">Liam — Energetic & Dynamic</option>
      `;
    }
  }
  loadVoices();

  // 4. Tone Selector pills
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

  // 5. Form Submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    const selectedTrack = musicSelect ? musicSelect.value : "upbeat_commercial";
    const useMusic = selectedTrack !== "none";
    const t = window.spotforgeI18n ? window.spotforgeI18n.t : (k) => k;

    const payload = {
      business_name: document.getElementById("business_name").value.trim(),
      business_type: document.getElementById("business_type").value.trim(),
      offer: document.getElementById("offer").value.trim(),
      call_to_action: document.getElementById("call_to_action").value.trim(),
      tone: selectedTone,
      language: document.querySelector('input[name="language"]:checked')?.value || "en",
      duration_seconds: parseInt(durationSlider.value, 10),
      voice_id: voiceSelect.value || null,
      music: useMusic,
      music_track: useMusic ? selectedTrack : null,
    };

    if (!payload.business_name || !payload.offer || !payload.call_to_action) {
      showError(t("error_empty_fields"));
      return;
    }

    startLoading(t("loading_title"));

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server error: HTTP ${res.status}`);
      }

      const data = await res.json();
      displayResult(data);
    } catch (err) {
      showError(err.message || "An unexpected error occurred while generating the audio spot.");
    } finally {
      stopLoading();
    }
  });

  // 6. Regenerate voice only (using modified script text)
  regenerateVoiceBtn.addEventListener("click", async () => {
    if (!currentSpotData) return;
    const modifiedScript = scriptTextarea.value.trim();
    const t = window.spotforgeI18n ? window.spotforgeI18n.t : (k) => k;

    if (!modifiedScript) {
      showError(t("error_empty_script"));
      return;
    }

    const selectedTrack = musicSelect ? musicSelect.value : "upbeat_commercial";
    const useMusic = selectedTrack !== "none";

    startLoading(t("loading_regenerate"));

    const payload = {
      business_name: document.getElementById("business_name").value.trim() || "Custom Spot",
      business_type: document.getElementById("business_type").value.trim() || "commercial",
      offer: document.getElementById("offer").value.trim() || "offer",
      call_to_action: document.getElementById("call_to_action").value.trim() || "action",
      custom_script: modifiedScript,
      voice_id: voiceSelect.value || null,
      language: document.querySelector('input[name="language"]:checked')?.value || "en",
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
        throw new Error(errorData.detail || `Error regenerating: HTTP ${res.status}`);
      }

      const data = await res.json();
      displayResult(data);
    } catch (err) {
      showError(err.message || "Error while regenerating speech audio.");
    } finally {
      stopLoading();
    }
  });

  // 7. Copy Script Button
  copyScriptBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(scriptTextarea.value);
      const originalText = copyScriptBtn.innerHTML;
      const copiedText = window.spotforgeI18n ? window.spotforgeI18n.t("btn_copied") : "✓ Copied!";
      copyScriptBtn.innerHTML = `<span>${copiedText}</span>`;
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

    const t = window.spotforgeI18n ? window.spotforgeI18n.t : (k) => k;

    scriptTextarea.value = data.script;
    metricDuration.textContent = `${data.duration_seconds}s`;
    metricWords.textContent = `${data.word_count} ${t("metric_words").toLowerCase()}`;
    if (metricChars) {
      metricChars.textContent = data.characters_used ? `${data.characters_used}` : "--";
    }
    metricVoice.textContent = data.voice_used || voiceSelect.options[voiceSelect.selectedIndex]?.text.split("—")[0].trim() || "Voice";

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

  // 8. Initialize language on page load
  if (window.spotforgeI18n) {
    window.spotforgeI18n.setLanguage(window.spotforgeI18n.getCurrentLanguage());
  } else {
    window.updateDurationLabel();
  }
});

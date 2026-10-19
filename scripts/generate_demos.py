"""Script to generate the 3 official demo spots for SpotForge."""

import sys
from pathlib import Path

# Force UTF-8 stdout if possible on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.services.copywriter import CopywriterService
from app.services.text_normalizer import normalize_for_tts
from app.services.voice_synth import VoiceSynthService
from app.services.audio_mixer import mix_voice_and_music
from app.services.storage import measure_mp3_duration

DEMO_CASES = [
    {
        "id": "demo_pizzeria",
        "business_name": "Pizzería Don Mario",
        "business_type": "Pizzería artesanal italiana con horno de leña",
        "offer": "2x1 en todas las pizzas familiares los martes y jueves, con masa madre crujiente y envío sin costo",
        "call_to_action": "Llama ahora al 555-0192 o pide por WhatsApp antes de las 10 de la noche",
        "tone": "energético",
        "language": "es",
        "duration_seconds": 30,
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",  # George
        "music_track": "upbeat_commercial",
        "output_filename": "demo_pizzeria.mp3",
    },
    {
        "id": "demo_barber",
        "business_name": "Barbería El Bigote",
        "business_type": "Barbería clásica premium y estilismo masculino",
        "offer": "Combo ejecutivo de corte clásico, perfilado de barba con toalla caliente y loción artesanal por solo $15 dólares",
        "call_to_action": "Agenda tu cita hoy en elbigote.com o marca al 555-8834. Cupos limitados",
        "tone": "urgente",
        "language": "es",
        "duration_seconds": 30,
        "voice_id": "TX3LPaxmHKxFdv7VOQHJ",  # Liam
        "music_track": "urban_energy",
        "output_filename": "demo_barber.mp3",
    },
    {
        "id": "demo_autorepair",
        "business_name": "Apex Auto Repair",
        "business_type": "Taller mecánico especializado multimarca y frenos",
        "offer": "Diagnóstico computarizado completo y cambio de aceite sintético con 30% de descuento en tu primera visita",
        "call_to_action": "Visítanos en Avenida Central 450 o agenda al 555-7641. Conduce con total tranquilidad",
        "tone": "profesional",
        "language": "es",
        "duration_seconds": 30,
        "voice_id": "CwhRBWXzGAHq8TQ4Fs17",  # Roger
        "music_track": "chill_acoustic",
        "output_filename": "demo_autorepair.mp3",
    },
]


def generate_demos():
    print("=" * 60, flush=True)
    print("[SpotForge] Generating 3 Official Demo Spots", flush=True)
    print("=" * 60, flush=True)

    copywriter = CopywriterService()
    voice_synth = VoiceSynthService()

    output_dir = Path("static/audio")
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, case in enumerate(DEMO_CASES, 1):
        print(f"\n[{idx}/3] Processing: {case['business_name']} ({case['id']})", flush=True)
        print(f"  Tone: {case['tone']} | Music: {case['music_track']} | Target: {case['duration_seconds']}s", flush=True)

        # 1. Gemma Copywriter
        print("  -> Step 1: Gemma generating AIDA ad copy...", flush=True)
        script_result = copywriter.generate_script(
            business_name=case["business_name"],
            business_type=case["business_type"],
            offer=case["offer"],
            call_to_action=case["call_to_action"],
            tone=case["tone"],
            language=case["language"],
            duration_seconds=case["duration_seconds"],
        )
        script = script_result.script
        print(f"  [Copy] Raw script ({script_result.word_count} words | Model: {script_result.model}):", flush=True)
        print(f"    {script}", flush=True)

        # 2. Text Normalizer
        print("  -> Step 2: Normalizing numbers, currency, phones to spoken Spanish...", flush=True)
        normalized_script = normalize_for_tts(script, language=case["language"])
        print("  [TTS-Ready] Normalized script for TTS:", flush=True)
        print(f"    {normalized_script}", flush=True)

        # 3. ElevenLabs TTS
        print(f"  -> Step 3: ElevenLabs synthesizing voice (voice: {case['voice_id']})...", flush=True)
        temp_voice_filename = f"temp_{case['id']}_voice.mp3"
        voice_result = voice_synth.synthesize_speech(
            text=normalized_script,
            voice_id=case["voice_id"],
            output_filename=temp_voice_filename,
        )
        voice_duration = measure_mp3_duration(voice_result.file_path)
        print(f"  [Voice] Talent: {voice_result.voice_name} | Duration: {voice_duration:.2f}s | Chars: {voice_result.characters_used}", flush=True)

        # Adaptive duration pacing retry if duration > 33.0s
        if voice_duration > case["duration_seconds"] + 3.0:
            print(f"  [Duration Check] {voice_duration:.2f}s exceeds {case['duration_seconds'] + 3.0}s target bound. Triggering adaptive retry...", flush=True)
            ratio = (case["duration_seconds"] / voice_duration) * 0.90
            new_target_words = int(script_result.word_count * ratio)
            print(f"  [Adaptive Retry] Re-budgeting target to {new_target_words} words...", flush=True)
            retry_script_res = copywriter.generate_script(
                business_name=case["business_name"],
                business_type=case["business_type"],
                offer=case["offer"],
                call_to_action=case["call_to_action"],
                tone=case["tone"],
                language=case["language"],
                duration_seconds=case["duration_seconds"],
                target_words_override=new_target_words,
            )
            script = retry_script_res.script
            normalized_script = normalize_for_tts(script, language=case["language"])
            if voice_result.file_path.exists():
                voice_result.file_path.unlink()
            voice_result = voice_synth.synthesize_speech(
                text=normalized_script,
                voice_id=case["voice_id"],
                output_filename=temp_voice_filename,
            )
            voice_duration = measure_mp3_duration(voice_result.file_path)
            print(f"  [Voice Retry] New duration: {voice_duration:.2f}s | Chars: {voice_result.characters_used}", flush=True)

        # 4. FFmpeg Audio Mixer
        final_output_path = output_dir / case["output_filename"]
        print(f"  -> Step 4: FFmpeg mixing voice with background track '{case['music_track']}'...", flush=True)
        mixed_path, warnings = mix_voice_and_music(
            voice_path=voice_result.file_path,
            music_track_id=case["music_track"],
            output_path=final_output_path,
        )
        if warnings:
            print(f"  [WARNINGS] {warnings}", flush=True)

        final_duration = measure_mp3_duration(final_output_path)
        file_size_kb = final_output_path.stat().st_size / 1024
        print(f"  [SUCCESS] Saved: {final_output_path.as_posix()}", flush=True)
        print(f"  [STATS] Real Duration: {final_duration:.2f}s | Size: {file_size_kb:.1f} KB", flush=True)

        # Clean up temporary voice file
        if voice_result.file_path.exists():
            voice_result.file_path.unlink()

    print("\n" + "=" * 60, flush=True)
    print("[SUCCESS] All 3 official demo spots generated successfully!", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    generate_demos()

"""
transcribe_audio.py — offline voice recognition / speech-to-text for X Jarvis.

Uses core/stt.py (Whisper or Vosk). Fully local after the first model download.
No Gemini / network required for the actual transcription.
"""
from __future__ import annotations

from pathlib import Path


def _resolve_path(raw: str) -> Path | None:
    """Expand ~ and make absolute; return None if empty."""
    raw = (raw or "").strip().strip('"').strip("'")
    if not raw:
        return None
    p = Path(raw).expanduser()
    if not p.is_absolute():
        # Try relative to user home and cwd
        home_try = Path.home() / p
        if home_try.is_file():
            return home_try
        cwd_try = Path.cwd() / p
        if cwd_try.is_file():
            return cwd_try
    return p


def transcribe_audio(parameters: dict, player=None, session_memory=None) -> str:
    params = parameters or {}
    path_str = (
        params.get("path")
        or params.get("file")
        or params.get("audio_path")
        or params.get("filename")
        or ""
    )
    engine = (params.get("engine") or "whisper").strip().lower()
    language = params.get("language") or None
    install_if_missing = str(params.get("install", "true")).lower() in ("1", "true", "yes")

    path = _resolve_path(path_str)
    if path is None:
        return (
            "Please give me the path to an audio file to transcribe "
            "(wav, mp3, flac, ogg, m4a, …)."
        )
    if not path.is_file():
        return f"I couldn't find the file: {path}"

    # Lazy import so the rest of the app stays light
    try:
        from core import stt as stt_mod
    except Exception as e:
        return f"Voice recognition module failed to load: {e}"

    if not stt_mod.is_engine_available(engine):
        if install_if_missing:
            if player:
                try:
                    player.write_log(f"[STT] Installing {engine}…")
                except Exception:
                    pass
            ok, msg = stt_mod.install_engine(engine)
            if not ok:
                return (
                    f"The {engine} engine is not installed and auto-install failed: {msg}. "
                    f"Run: pip install {'faster-whisper' if 'whisper' in engine else 'vosk'}"
                )
        else:
            return (
                f"The {engine} engine is not installed. "
                f"Say 'install whisper' / 'install vosk' or run: "
                f"pip install {'faster-whisper' if 'whisper' in engine else 'vosk'}"
            )

    try:
        text = stt_mod.transcribe_file(
            path,
            engine=engine,
            language=language,
        )
    except Exception as e:
        return f"Transcription failed: {e}"

    if not text:
        return f"I listened to {path.name} but heard no clear speech."

    if player:
        try:
            player.write_log(f"[STT] {path.name} → {text[:100]}")
        except Exception:
            pass

    # Keep it concise for voice; full text is returned
    if len(text) > 400:
        return f"Transcript of {path.name}:\n{text[:400]}…\n(Full text is {len(text)} characters.)"
    return f"Transcript of {path.name}:\n{text}"


# ── Tool declaration (auto-discovered) ────────────────────────────────────
TOOL = {
    "name": "transcribe_audio",
    "description": (
        "Offline speech-to-text / voice recognition. Transcribes an audio file "
        "(wav, mp3, flac, ogg, m4a…) into text using a local model (Whisper or Vosk). "
        "Use when the user asks to 'transcribe', 'what does this audio say', "
        "'convert this voice note to text', or similar. Fully offline after first model download."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "path": {
                "type": "STRING",
                "description": "Full or relative path to the audio file",
            },
            "engine": {
                "type": "STRING",
                "description": "whisper (accurate, default) or vosk (lighter, streaming)",
            },
            "language": {
                "type": "STRING",
                "description": "Language code e.g. en, ur, hi, or 'auto' (default)",
            },
            "install": {
                "type": "BOOLEAN",
                "description": "If the engine package is missing, try to pip-install it (default true)",
            },
        },
        "required": ["path"],
    },
    "handler": transcribe_audio,
}

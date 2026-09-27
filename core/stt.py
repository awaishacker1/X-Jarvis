"""
Speech-to-Text / Voice Recognition module for X Jarvis.

Two offline engines (no cloud, no API key after first model download):

  Whisper  – higher accuracy, VAD-buffered (faster-whisper)
  Vosk     – lighter, true streaming (Kaldi)

Primary real-time conversation still uses Gemini Live. This module is for:
  • offline transcription of audio files / buffers
  • local fallback when the network is down
  • the "transcribe" voice action
  • future local-only modes

Public API
----------
  is_engine_available(name) -> bool
  install_engine(name, logger=print) -> (ok, message)
  create_stt(config | engine_name) -> WhisperSTT | VoskSTT
  transcribe_file(path, engine=None, language=None) -> str
  load_audio(path, target_sr=16000) -> np.ndarray   # float32 mono

Both engines accept float32 mono @ 16 kHz.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import wave
from pathlib import Path
from typing import Callable, Optional, Union

import numpy as np

# ── Constants ──────────────────────────────────────────────────────────────
SAMPLE_RATE = 16000
_WHISPER_MODELS = ("tiny", "base", "small", "medium", "large-v3")
_DEFAULT_WHISPER = "base"
_DEFAULT_VOSK_LANG = "en-us"


# ── Availability / install helpers (same spirit as wake_word.py) ───────────

def is_engine_available(engine: str) -> bool:
    """True if the Python package for that engine can be imported."""
    engine = (engine or "").strip().lower()
    if engine in ("whisper", "faster-whisper", "faster_whisper"):
        return importlib.util.find_spec("faster_whisper") is not None
    if engine == "vosk":
        return importlib.util.find_spec("vosk") is not None
    return False


def install_engine(
    engine: str,
    logger: Callable[[str], None] = print,
) -> tuple[bool, str]:
    """
    One-shot pip install for the chosen STT engine.
    Returns (ok, human message). Never raises.
    """
    engine = (engine or "").strip().lower()
    mapping = {
        "whisper": "faster-whisper",
        "faster-whisper": "faster-whisper",
        "faster_whisper": "faster-whisper",
        "vosk": "vosk",
    }
    pkg = mapping.get(engine)
    if not pkg:
        return False, f"Unknown STT engine '{engine}'. Choose 'whisper' or 'vosk'."

    if is_engine_available(engine):
        return True, f"{pkg} is already installed."

    logger(f"[STT] Installing {pkg} (one-time)…")
    try:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg,
             "--quiet", "--disable-pip-version-check"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            err = (r.stderr or r.stdout or "").strip()[:200]
            return False, f"Failed to install {pkg}: {err}"
        return True, f"{pkg} installed successfully."
    except Exception as e:
        return False, f"Install error: {e}"


# ── Audio loading helpers ──────────────────────────────────────────────────

def load_audio(path: Union[str, Path], target_sr: int = SAMPLE_RATE) -> np.ndarray:
    """
    Load any common audio file → float32 mono @ target_sr.
    Prefers soundfile; falls back to wave for plain WAV.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")

    # Prefer soundfile (handles wav/flac/ogg/mp3 if codecs present)
    try:
        import soundfile as sf
        data, sr = sf.read(str(path), always_2d=False, dtype="float32")
        if data.ndim > 1:
            data = data.mean(axis=1)
        if sr != target_sr:
            data = _resample(data, sr, target_sr)
        return np.ascontiguousarray(data, dtype=np.float32)
    except Exception:
        pass

    # Minimal WAV fallback (stdlib only)
    if path.suffix.lower() == ".wav":
        with wave.open(str(path), "rb") as wf:
            nch = wf.getnchannels()
            sw = wf.getsampwidth()
            sr = wf.getframerate()
            nframes = wf.getnframes()
            raw = wf.readframes(nframes)
        if sw == 2:
            audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        elif sw == 4:
            audio = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483648.0
        else:
            raise ValueError(f"Unsupported WAV sample width: {sw}")
        if nch > 1:
            audio = audio.reshape(-1, nch).mean(axis=1)
        if sr != target_sr:
            audio = _resample(audio, sr, target_sr)
        return np.ascontiguousarray(audio, dtype=np.float32)

    raise RuntimeError(
        f"Cannot load '{path.name}'. Install soundfile (`pip install soundfile`) "
        "for broader format support, or provide a 16-bit PCM WAV."
    )


def _resample(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """Cheap linear resample (good enough for speech)."""
    if orig_sr == target_sr or len(audio) == 0:
        return audio
    duration = len(audio) / orig_sr
    new_len = int(duration * target_sr)
    if new_len <= 0:
        return np.zeros(0, dtype=np.float32)
    x_old = np.linspace(0.0, 1.0, num=len(audio), endpoint=False)
    x_new = np.linspace(0.0, 1.0, num=new_len, endpoint=False)
    return np.interp(x_new, x_old, audio).astype(np.float32)


def float32_to_int16_bytes(audio: np.ndarray) -> bytes:
    """Convert float32 mono [-1,1] → int16 LE PCM bytes (for Vosk)."""
    clipped = np.clip(audio, -1.0, 1.0)
    return (clipped * 32767.0).astype(np.int16).tobytes()


# ── Whisper engine ─────────────────────────────────────────────────────────

class WhisperSTT:
    """Offline batch transcription via faster-whisper."""

    def __init__(self, model_name: str = _DEFAULT_WHISPER, language: str | None = None):
        if not is_engine_available("whisper"):
            raise RuntimeError(
                "faster-whisper is not installed. "
                "Call core.stt.install_engine('whisper') or: pip install faster-whisper"
            )
        from faster_whisper import WhisperModel

        model_name = (model_name or _DEFAULT_WHISPER).strip().lower()
        if model_name not in _WHISPER_MODELS:
            model_name = _DEFAULT_WHISPER

        print(f"[STT] Loading Whisper '{model_name}'…")
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            compute = "float16" if device == "cuda" else "int8"
        except Exception:
            device, compute = "cpu", "int8"

        try:
            self._model = WhisperModel(model_name, device=device, compute_type=compute)
        except Exception as first_err:
            # Model not cached yet → clear offline flags and retry once
            e = str(first_err).lower()
            offline_kw = (
                "offline", "not found", "cache", "localentry",
                "does not exist", "outgoing", "local_files_only",
            )
            if any(k in e for k in offline_kw):
                print(f"[STT] Whisper '{model_name}' not cached — downloading (one-time)…")
                for key in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "HF_DATASETS_OFFLINE"):
                    os.environ.pop(key, None)
                try:
                    self._model = WhisperModel(model_name, device=device, compute_type=compute)
                except Exception as dl_err:
                    raise RuntimeError(
                        f"Whisper '{model_name}' download failed.\n"
                        "Internet is required the first time (~75–1500 MB depending on size).\n"
                        f"After that it runs fully offline.\nDetails: {dl_err}"
                    ) from dl_err
            else:
                raise

        self._language = None if (not language or language.strip().lower() == "auto") else language.strip().lower()
        self.engine_name = "whisper"
        self.model_name = model_name
        print(f"[STT] Whisper '{model_name}' ready ({device})")

    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribe float32 mono 16 kHz array → text."""
        if audio is None or len(audio) == 0:
            return ""
        try:
            segments, _ = self._model.transcribe(
                audio.astype(np.float32),
                language=self._language,
                beam_size=1,
                best_of=1,
                condition_on_previous_text=False,
                vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 300},
            )
            return " ".join(s.text for s in segments).strip()
        except Exception as e:
            print(f"[STT] Whisper transcription error: {e}")
            raise

    def transcribe_file(self, path: Union[str, Path]) -> str:
        audio = load_audio(path, SAMPLE_RATE)
        return self.transcribe(audio)


# ── Vosk engine ────────────────────────────────────────────────────────────

class VoskSTT:
    """Lightweight streaming / batch transcription via Vosk."""

    def __init__(self, model_path: str | None = None, language: str = _DEFAULT_VOSK_LANG):
        if not is_engine_available("vosk"):
            raise RuntimeError(
                "vosk is not installed. "
                "Call core.stt.install_engine('vosk') or: pip install vosk"
            )
        from vosk import Model, KaldiRecognizer, SetLogLevel
        SetLogLevel(-1)  # silence Vosk spam

        print("[STT] Loading Vosk model…")
        if model_path and Path(model_path).is_dir():
            model = Model(model_path)
        else:
            lang = (language or _DEFAULT_VOSK_LANG).strip().lower()
            if lang == "auto":
                lang = _DEFAULT_VOSK_LANG
            try:
                model = Model(lang=lang)
            except Exception as e:
                raise RuntimeError(
                    f"Vosk model for language '{lang}' not found.\n"
                    "Download a model from https://alphacephei.com/vosk/models "
                    "and pass model_path=, or install the small English model."
                ) from e

        self._model = model
        self._rec = KaldiRecognizer(model, SAMPLE_RATE)
        self._rec.SetWords(True)
        self.engine_name = "vosk"
        self.language = language
        print("[STT] Vosk ready.")

    def reset(self) -> None:
        """Clear recognizer state (start a new utterance)."""
        from vosk import KaldiRecognizer
        self._rec = KaldiRecognizer(self._model, SAMPLE_RATE)
        self._rec.SetWords(True)

    def process_chunk(self, audio_bytes: bytes) -> tuple[str, bool]:
        """
        Feed raw int16 LE PCM bytes @ 16 kHz.
        Returns (text, is_final).
        """
        if self._rec.AcceptWaveform(audio_bytes):
            result = json.loads(self._rec.Result())
            return result.get("text", "").strip(), True
        partial = json.loads(self._rec.PartialResult())
        return partial.get("partial", "").strip(), False

    def finish(self) -> str:
        """Flush remaining audio and return final text."""
        result = json.loads(self._rec.FinalResult())
        return result.get("text", "").strip()

    def transcribe(self, audio: np.ndarray) -> str:
        """Batch-transcribe a float32 mono 16 kHz array."""
        if audio is None or len(audio) == 0:
            return ""
        self.reset()
        pcm = float32_to_int16_bytes(audio)
        # Feed in ~0.5 s chunks for better streaming behaviour
        chunk = SAMPLE_RATE  # 1 second of int16 samples → 2 bytes each
        step = chunk * 2
        for i in range(0, len(pcm), step):
            self.process_chunk(pcm[i : i + step])
        return self.finish()

    def transcribe_file(self, path: Union[str, Path]) -> str:
        audio = load_audio(path, SAMPLE_RATE)
        return self.transcribe(audio)


# ── Factory ────────────────────────────────────────────────────────────────

def create_stt(
    config_or_engine: Union[dict, str, None] = None,
    *,
    language: str | None = None,
    model_name: str | None = None,
) -> Union[WhisperSTT, VoskSTT]:
    """
    Create an STT engine from a config dict or engine name string.

    Config keys (all optional):
      stt_engine   : "whisper" | "vosk"   (default "whisper")
      stt_model    : Whisper model size or Vosk model path
      stt_language : language code or "auto"
    """
    if isinstance(config_or_engine, dict):
        cfg = config_or_engine
        engine = (cfg.get("stt_engine") or "whisper").strip().lower()
        model = cfg.get("stt_model") or model_name
        lang = cfg.get("stt_language") or language
    elif isinstance(config_or_engine, str):
        engine = config_or_engine.strip().lower()
        model = model_name
        lang = language
    else:
        engine = "whisper"
        model = model_name
        lang = language

    if engine in ("whisper", "faster-whisper", "faster_whisper"):
        return WhisperSTT(model_name=model or _DEFAULT_WHISPER, language=lang)
    if engine == "vosk":
        return VoskSTT(model_path=model, language=lang or _DEFAULT_VOSK_LANG)
    raise ValueError(f"Unknown STT engine '{engine}'. Use 'whisper' or 'vosk'.")


def transcribe_file(
    path: Union[str, Path],
    engine: str = "whisper",
    language: str | None = None,
    model_name: str | None = None,
) -> str:
    """Convenience: load file + create engine + transcribe in one call."""
    stt = create_stt(engine, language=language, model_name=model_name)
    return stt.transcribe_file(path)

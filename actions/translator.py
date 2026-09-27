"""
translator.py — quick text translation for X Jarvis.

Reuses core/gemini.py's shared one-shot call (FAST tier: Live-first, falls
back down the REST ladder) instead of opening a fresh genai.Client the way
older actions in this codebase used to — see core/gemini.py's module
docstring for why that used to be a real, repeated bug (no timeout, no
fallback, sixteen copies of the same model name).
"""
from core import gemini


def translate_text(text: str, target_language: str) -> str:
    text = (text or "").strip()
    target_language = (target_language or "English").strip()
    if not text:
        return "Please give me the text you want translated."

    prompt = (
        f"Translate the following text into {target_language}. "
        "Return ONLY the translation — no notes, no quotation marks, "
        "no explanation.\n\n"
        f"Text:\n{text}"
    )
    result = gemini.text(prompt, tier=gemini.FAST, timeout_ms=15_000, default="")
    if not result:
        return "Sorry, I couldn't reach the translation model right now."
    return result


def translator(parameters: dict, player=None, session_memory=None) -> str:
    params = parameters or {}
    text   = params.get("text", "")
    target = params.get("target_language", "English")

    result = translate_text(text, target)

    if player:
        try:
            player.write_log(f"[Translate] -> {target}: {result[:60]}")
        except Exception:
            pass

    if session_memory:
        try:
            session_memory.set_last_search(query=f"translate to {target}", response=result)
        except Exception:
            pass

    return result


# ── Tool declaration (auto-discovered by core/action_loader.py) ──────────────
TOOL = {
    "name": "translator",
    "description": "Translates a piece of text into another language.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "text": {
                "type": "STRING",
                "description": "The text to translate",
            },
            "target_language": {
                "type": "STRING",
                "description": "Language to translate into, e.g. Urdu, English, Arabic",
            },
        },
        "required": ["text", "target_language"],
    },
    "handler": translator,
}

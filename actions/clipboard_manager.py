"""
clipboard_manager.py — clipboard history for X Jarvis.

Watches the system clipboard on a background thread (started lazily, on
first use) and keeps the last _MAX_HISTORY entries in memory so the user can
ask "what did I copy earlier?" or paste something copied a few steps back.

History is kept IN MEMORY ONLY, on purpose: the clipboard routinely carries
passwords, OTP codes and other short-lived secrets, and writing that to a
plaintext file on disk would turn a convenience feature into a standing
security liability. History is lost on restart — that trade-off is
deliberate, not an oversight.
"""
import threading
import time
from datetime import datetime

try:
    import pyperclip
    _PYPERCLIP = True
except ImportError:
    _PYPERCLIP = False

_MAX_HISTORY  = 50
_POLL_SECONDS = 1.5

_history      : list[dict] = []   # newest last: {"text":..., "time":...}
_history_lock = threading.Lock()
_last_value   = None
_watcher_thread: threading.Thread | None = None
_stop_event   = threading.Event()


def _watch_loop() -> None:
    global _last_value
    while not _stop_event.is_set():
        try:
            val = pyperclip.paste()
            if val and val != _last_value:
                _last_value = val
                with _history_lock:
                    _history.append({
                        "text": val[:1000],
                        "time": datetime.now().strftime("%H:%M:%S"),
                    })
                    if len(_history) > _MAX_HISTORY:
                        del _history[0]
        except Exception:
            pass
        _stop_event.wait(_POLL_SECONDS)


def _ensure_watcher() -> str | None:
    """Starts the background watcher if it isn't already running.
    Returns an error string if it can't start, else None."""
    global _watcher_thread
    if not _PYPERCLIP:
        return "Clipboard support isn't installed (pip install pyperclip)."
    if _watcher_thread and _watcher_thread.is_alive():
        return None
    _stop_event.clear()
    _watcher_thread = threading.Thread(
        target=_watch_loop, daemon=True, name="clipboard-watcher"
    )
    _watcher_thread.start()
    return None


def _stop_watcher() -> None:
    _stop_event.set()


def _format_entry(i: int, entry: dict) -> str:
    text = entry["text"].replace("\n", " ")
    if len(text) > 120:
        text = text[:120].rstrip() + "…"
    return f"{i}. [{entry['time']}] {text}"


def get_history(limit: int = 10) -> str:
    err = _ensure_watcher()
    if err:
        return err
    with _history_lock:
        items = list(reversed(_history))[:max(1, limit)]
    if not items:
        return "Nothing copied yet since the watcher started."
    lines = [_format_entry(i, e) for i, e in enumerate(items, 1)]
    return "Clipboard history (most recent first):\n" + "\n".join(lines)


def search_history(query: str) -> str:
    err = _ensure_watcher()
    if err:
        return err
    query = (query or "").strip().lower()
    if not query:
        return "What should I search the clipboard history for?"
    with _history_lock:
        items = list(reversed(_history))
    matches = [(i, e) for i, e in enumerate(items, 1) if query in e["text"].lower()]
    if not matches:
        return f"Nothing in clipboard history matches '{query}'."
    lines = [_format_entry(i, e) for i, e in matches[:10]]
    return f"Matches for '{query}':\n" + "\n".join(lines)


def copy_from_history(index: int) -> str:
    if not _PYPERCLIP:
        return "Clipboard support isn't installed (pip install pyperclip)."
    with _history_lock:
        items = list(reversed(_history))
    if index < 1 or index > len(items):
        return f"There's no item #{index} in the clipboard history."
    entry = items[index - 1]
    try:
        pyperclip.copy(entry["text"])
    except Exception as e:
        return f"Couldn't copy that back to the clipboard: {e}"
    return f"Copied item #{index} back to the clipboard."


def clear_history() -> str:
    with _history_lock:
        _history.clear()
    return "Clipboard history cleared."


def clipboard_manager(parameters: dict, player=None, session_memory=None) -> str:
    params = parameters or {}
    action = (params.get("action") or "history").strip().lower()

    try:
        if action == "start":
            err = _ensure_watcher()
            result = err or "Clipboard watcher is running."
        elif action == "stop":
            _stop_watcher()
            result = "Clipboard watcher stopped."
        elif action == "history":
            limit  = int(params.get("limit") or 10)
            result = get_history(limit)
        elif action == "search":
            result = search_history(params.get("query", ""))
        elif action == "copy":
            result = copy_from_history(int(params.get("index", 1)))
        elif action == "clear":
            result = clear_history()
        else:
            result = f"Unknown action '{action}'. Use start, stop, history, search, copy, or clear."
    except Exception as e:
        print(f"[Clipboard] Error: {e}")
        result = f"Clipboard manager error: {e}"

    if player:
        try:
            player.write_log(f"[Clipboard] {action}")
        except Exception:
            pass
    return result


# ── Tool declaration (auto-discovered by core/action_loader.py) ──────────────
TOOL = {
    "name": "clipboard_manager",
    "description": (
        "Tracks clipboard history so the user can recall or re-copy "
        "something they copied earlier in the session."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "start | stop | history | search | copy | clear",
            },
            "limit": {
                "type": "INTEGER",
                "description": "For 'history': how many recent entries to show (default 10)",
            },
            "query": {
                "type": "STRING",
                "description": "For 'search': text to look for in clipboard history",
            },
            "index": {
                "type": "INTEGER",
                "description": "For 'copy': which item to restore, 1 = most recent",
            },
        },
        "required": ["action"],
    },
    "handler": clipboard_manager,
}

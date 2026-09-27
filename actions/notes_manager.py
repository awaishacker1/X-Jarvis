"""
notes_manager.py — persistent quick notes for X Jarvis.

Stores notes in memory/notes.json (next to long_term.json and todos.json).
Actions: add | list | search | delete | clear
"""
import json
import sys
import threading
from datetime import datetime
from pathlib import Path


def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


_NOTES_PATH = _base_dir() / "memory" / "notes.json"
_lock = threading.Lock()
_MAX_NOTES = 200


def _load() -> list:
    if not _NOTES_PATH.exists():
        return []
    try:
        data = json.loads(_NOTES_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[Notes] Load error: {e}")
        return []


def _save(notes: list) -> None:
    _NOTES_PATH.parent.mkdir(parents=True, exist_ok=True)
    _NOTES_PATH.write_text(
        json.dumps(notes, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _next_id(notes: list) -> int:
    return max((n.get("id", 0) for n in notes), default=0) + 1


def _find(notes: list, ref: str):
    """Match by numeric id first, else by case-insensitive substring of text."""
    ref = (ref or "").strip()
    if not ref:
        return None
    if ref.isdigit():
        rid = int(ref)
        for n in notes:
            if n.get("id") == rid:
                return n
    low = ref.lower()
    for n in reversed(notes):
        if low in n.get("text", "").lower():
            return n
    return None


def add_note(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return "I need some text to save as a note."
    with _lock:
        notes = _load()
        note = {
            "id": _next_id(notes),
            "text": text,
            "created": datetime.now().isoformat(timespec="seconds"),
        }
        notes.append(note)
        # Keep only the most recent notes
        if len(notes) > _MAX_NOTES:
            notes = notes[-_MAX_NOTES:]
        _save(notes)
    return f"Note #{note['id']} saved."


def list_notes(limit: int = 10) -> str:
    with _lock:
        notes = _load()
    if not notes:
        return "You have no notes yet."
    recent = notes[-limit:]
    lines = [f"#{n['id']}: {n['text']}" for n in reversed(recent)]
    header = f"Last {len(recent)} of {len(notes)} notes:\n" if len(notes) > limit else f"{len(notes)} notes:\n"
    return header + "\n".join(lines)


def search_notes(query: str) -> str:
    query = (query or "").strip().lower()
    if not query:
        return "Give me a keyword to search notes."
    with _lock:
        notes = _load()
    matches = [n for n in notes if query in n.get("text", "").lower()]
    if not matches:
        return f"No notes match '{query}'."
    lines = [f"#{n['id']}: {n['text']}" for n in reversed(matches[-15:])]
    return f"Found {len(matches)} note(s):\n" + "\n".join(lines)


def delete_note(ref: str) -> str:
    with _lock:
        notes = _load()
        target = _find(notes, ref)
        if not target:
            return f"No note found matching '{ref}'."
        notes = [n for n in notes if n.get("id") != target["id"]]
        _save(notes)
    return f"Deleted note #{target['id']}: {target['text'][:60]}"


def clear_notes() -> str:
    with _lock:
        notes = _load()
        count = len(notes)
        _save([])
    return f"Cleared {count} note(s)."


def notes_manager(parameters: dict, player=None, session_memory=None) -> str:
    params = parameters or {}
    action = (params.get("action") or "list").strip().lower()
    text = params.get("text", "") or params.get("query", "") or params.get("note", "")

    try:
        if action == "add":
            result = add_note(text)
        elif action == "list":
            limit = int(params.get("limit", 10) or 10)
            result = list_notes(limit)
        elif action in ("search", "find"):
            result = search_notes(text)
        elif action in ("delete", "remove"):
            result = delete_note(text)
        elif action in ("clear", "clear_all"):
            result = clear_notes()
        else:
            result = (
                "Unknown notes action. Use: add, list, search, delete, or clear."
            )
    except Exception as e:
        result = f"Notes error: {e}"

    if player:
        try:
            player.write_log(f"[Notes] {action}: {result[:80]}")
        except Exception:
            pass

    return result


# ── Tool declaration (auto-discovered by core/action_loader.py) ──────────────
TOOL = {
    "name": "notes_manager",
    "description": (
        "Manages persistent quick notes: add a note, list recent notes, "
        "search notes by keyword, delete a note by id or keyword, or clear all notes."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "add | list | search | delete | clear",
            },
            "text": {
                "type": "STRING",
                "description": "Note text (for add), keyword (for search/delete), or id (for delete)",
            },
            "limit": {
                "type": "INTEGER",
                "description": "For 'list': how many recent notes to show (default 10)",
            },
        },
        "required": ["action"],
    },
    "handler": notes_manager,
}

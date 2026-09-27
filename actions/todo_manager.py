"""
todo_manager.py — a small persistent to-do list for X Jarvis.

Stores tasks in memory/todos.json (next to long_term.json), independent of
the fact-memory store in memory/memory_manager.py — this is a checklist, not
a fact the assistant "remembers about you".

Actions: add | list | complete | remove | clear_completed
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


_TODOS_PATH = _base_dir() / "memory" / "todos.json"
_lock = threading.Lock()


def _as_bool(v) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "1", "yes", "y")
    return bool(v)


def _load() -> list:
    if not _TODOS_PATH.exists():
        return []
    try:
        data = json.loads(_TODOS_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[Todo] Load error: {e}")
        return []


def _save(tasks: list) -> None:
    _TODOS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _TODOS_PATH.write_text(
        json.dumps(tasks, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _next_id(tasks: list) -> int:
    return max((t.get("id", 0) for t in tasks), default=0) + 1


def _find(tasks: list, ref: str):
    """Match a task by numeric id first, else by case-insensitive substring
    of its text — most recently added match wins, since that's usually the
    one the user means ("mark the milk one done")."""
    ref = (ref or "").strip()
    if not ref:
        return None
    if ref.isdigit():
        rid = int(ref)
        for t in tasks:
            if t.get("id") == rid:
                return t
    low = ref.lower()
    for t in reversed(tasks):
        if low in t.get("text", "").lower():
            return t
    return None


def add_task(text: str) -> str:
    text = (text or "").strip()
    if not text:
        return "I need the task text to add it."
    with _lock:
        tasks = _load()
        tid = _next_id(tasks)
        tasks.append({
            "id": tid,
            "text": text,
            "done": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        _save(tasks)
    return f"Added task #{tid}: {text}"


def list_tasks(include_done: bool = False) -> str:
    with _lock:
        tasks = _load()
    pending = [t for t in tasks if not t.get("done")]
    done    = [t for t in tasks if t.get("done")]

    if not pending and not (include_done and done):
        return "Your to-do list is empty."

    out = (
        "Pending tasks:\n" + "\n".join(f"#{t['id']} {t['text']}" for t in pending)
        if pending else "No pending tasks."
    )
    if include_done and done:
        out += "\n\nCompleted:\n" + "\n".join(f"#{t['id']} {t['text']}" for t in done)
    return out


def complete_task(ref: str) -> str:
    with _lock:
        tasks = _load()
        t = _find(tasks, ref)
        if not t:
            return f"I couldn't find a task matching '{ref}'."
        if t.get("done"):
            return f"'{t['text']}' is already marked done."
        t["done"] = True
        t["completed"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        _save(tasks)
        return f"Marked done: {t['text']}"


def remove_task(ref: str) -> str:
    with _lock:
        tasks = _load()
        t = _find(tasks, ref)
        if not t:
            return f"I couldn't find a task matching '{ref}'."
        tasks = [x for x in tasks if x is not t]
        _save(tasks)
        return f"Removed: {t['text']}"


def clear_completed() -> str:
    with _lock:
        tasks = _load()
        remaining = [t for t in tasks if not t.get("done")]
        removed = len(tasks) - len(remaining)
        _save(remaining)
    return f"Cleared {removed} completed task(s)." if removed else "No completed tasks to clear."


def todo_manager(parameters: dict, player=None, session_memory=None) -> str:
    params   = parameters or {}
    action   = (params.get("action") or "list").strip().lower()
    task_ref = params.get("task", "")

    try:
        if action == "add":
            result = add_task(task_ref)
        elif action == "list":
            result = list_tasks(include_done=_as_bool(params.get("include_done", False)))
        elif action == "complete":
            result = complete_task(task_ref)
        elif action == "remove":
            result = remove_task(task_ref)
        elif action == "clear_completed":
            result = clear_completed()
        else:
            result = f"Unknown action '{action}'. Use add, list, complete, remove, or clear_completed."
    except Exception as e:
        print(f"[Todo] Error: {e}")
        result = f"To-do list error: {e}"

    if player:
        try:
            player.write_log(f"[Todo] {action}: {result[:60]}")
        except Exception:
            pass
    return result


# ── Tool declaration (auto-discovered by core/action_loader.py) ──────────────
TOOL = {
    "name": "todo_manager",
    "description": (
        "Manages a persistent to-do list: add a task, list pending or "
        "completed tasks, mark a task done, remove a task, or clear "
        "completed tasks."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "add | list | complete | remove | clear_completed",
            },
            "task": {
                "type": "STRING",
                "description": "Task text (for add) or an id/keyword to match (for complete/remove)",
            },
            "include_done": {
                "type": "BOOLEAN",
                "description": "For 'list': also show completed tasks (default false)",
            },
        },
        "required": ["action"],
    },
    "handler": todo_manager,
}

# X Jarvis — Changelog

## 2.2.2

### Startup experience
- Professional full-width **AWAIS ASSISTANCE** ASCII banner + smaller **X JARVIS** title on every `python main.py` launch
- Animated console robot (arm motion + status line) under the banner for a powerful first impression

### Already present (confirmed)
- Shutdown / Restart / Lock screen via `computer_settings` with real UI confirmation (model cannot self-confirm)

## 2.2.1

### New: Offline Voice Recognition module
- **`core/stt.py` rewritten** into a full offline STT / voice-recognition module:
  - `WhisperSTT` (faster-whisper) — high accuracy, VAD, GPU if available
  - `VoskSTT` — lightweight true streaming
  - `create_stt()`, `transcribe_file()`, `load_audio()`, install helpers
  - Zero cost when unused (packages imported only when needed)
- **`actions/transcribe_audio.py`** — voice command: "transcribe this audio file",
  "what does this recording say", etc. Can auto-install the engine on first use.
- Documented as optional in `requirements.txt` (not pulled by a normal `setup.py`).

## 2.2.0

### New features
- **`actions/notes_manager.py`** — persistent quick notes (`memory/notes.json`):
  add / list / search / delete / clear. Notes survive restarts; max 200 kept.
- **`actions/calculator.py`** — safe math evaluator (AST-based, no arbitrary code).
  Supports arithmetic, parentheses, sqrt/sin/cos/tan/log/exp/abs/round/floor/ceil,
  and constants pi & e. Zero new dependencies.

### Repository readiness
- Renamed `readme.md` → `README.md` (GitHub standard).
- Added `LICENSE` (CC BY-NC 4.0).
- Expanded `.gitignore` to cover `memory/todos.json`, `memory/notes.json` and all
  runtime JSON under memory/ while preserving the source modules.
- Updated README with full `git clone` install flow, complete tool/command list,
  and refreshed project structure.

## 2.1.0

### Security fixes
- **`actions/desktop.py` — hardened the "task" (AI-generated code) sandbox.**
  Generated code used to run with `getattr`/`hasattr` available and the real,
  unrestricted `pathlib.Path` / `shutil` handed in — so a restricted-builtins
  `exec()` could still be escaped with a plain attribute chain like
  `().__class__.__bases__[0].__subclasses__()`, or simply call
  `Path(...).unlink()` / `.write_text()` even though the prompt said not to.
  Fixed by:
  - dropping `getattr`/`hasattr` from the sandbox's builtins,
  - rejecting any generated code that touches a dunder attribute
    (`__class__`, `__globals__`, …) or calls a reflection/name-space function
    (`getattr`, `vars`, `globals`, `eval`, …) *before* it is ever compiled,
  - replacing the raw `Path`/`shutil` objects with read-only proxies
    (`_SafePath`, `_SafeShutil`) that simply don't have `unlink`, `rename`,
    `write_text`, `chmod`, etc. as attributes.
  This is defense in depth, not a claim that arbitrary generated Python is
  now provably safe — see the comments in `_build_sandbox()`.

- **`memory/memory_manager.py` — closed a lost-update race.** `update_memory()`
  and `forget()` used to read the store and write it back as two separate
  lock acquisitions, so a second call on another thread could read a stale
  copy in between and overwrite what the first call had just saved. Both
  (and `save_session_summary()`) now do the whole read‑modify‑write under one
  lock.

### Bug fixes
- **`memory/memory_manager.py` — `search_memory()` missed underscore keys.**
  A query like `"sister_name"` failed to match a stored key of exactly that
  name, because the key is displayed/matched as `"sister name"` (underscores
  turned into spaces) but the query tokenizer left the underscore glued to
  the word. Query words are now split the same way, so a query containing an
  underscore matches the way a person would expect.
- `save_session_summary()` now runs through the same size-guard
  (`_trim_to_limit`) as every other write, instead of writing straight to
  disk and bypassing it.

### New features
- **`actions/todo_manager.py`** — a persistent to-do list (`memory/todos.json`):
  add / list / complete / remove tasks, clear completed ones. Tasks can be
  referenced by id or by a keyword from their text.
- **`actions/clipboard_manager.py`** — clipboard history: a lazily-started
  background watcher keeps the last 50 copies in memory (in-memory only,
  never written to disk, since the clipboard routinely carries passwords and
  OTP codes) so the user can list, search, or re-copy something from earlier
  in the session.
- **`actions/translator.py`** — quick text translation into any named
  language, built on the shared `core/gemini.py` one-shot call (so it gets
  the existing timeout + model-fallback ladder for free, instead of opening
  a fresh, unbounded `genai.Client` the way several older actions in this
  codebase originally did).

No new third-party dependencies: `pyperclip` (clipboard) and `google-genai`
(translation) were already required by `requirements.txt`.

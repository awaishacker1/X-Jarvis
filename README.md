<div align="center">

# ⚙️ X JARVIS

### `THE PERSONAL AI COMMAND CORE`

**AWAIS × HASEEB HACKER TEAM**  
`POWERED BY X HACKER CAPTAIN TEAM`

[![Python](https://img.shields.io/badge/Python-3.11%2B-00d9ff?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Windows-SUPPORTED-00d9ff?style=for-the-badge&logo=windows)](#-platform-support)
[![macOS](https://img.shields.io/badge/macOS-SUPPORTED-00d9ff?style=for-the-badge&logo=apple)](#-platform-support)
[![Linux](https://img.shields.io/badge/Linux-SUPPORTED-00d9ff?style=for-the-badge&logo=linux)](#-platform-support)
[![Gemini](https://img.shields.io/badge/Gemini-Live%20API-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/)

<br>

<img src="assets/x-jarvis-heavy-loop.gif" width="100%" alt="X JARVIS animated command core">

<br><br>

<a href="#-quick-start">🚀 QUICK START</a> •
<a href="#-features">⚡ FEATURES</a> •
<a href="#-commands">🎙️ COMMANDS</a> •
<a href="#-architecture">🧠 ARCHITECTURE</a> •
<a href="#-support">💬 SUPPORT</a>

</div>

---

## 🛰️ LIVE COMMAND CORE

```text
╔══════════════════════════════════════════════════════════════════════╗
║                         X  J A R V I S                              ║
║                 AWAIS × HASEEB HACKER TEAM                         ║
║                 X HACKER CAPTAIN TEAM                              ║
╠══════════════════════════════════════════════════════════════════════╣
║  ● VOICE          ONLINE        ● VISION        ONLINE              ║
║  ● MEMORY         ONLINE        ● PLUGINS       READY               ║
║  ● SYSTEM         READY         ● OFFLINE STT   READY               ║
║  ● HUD            ACTIVE        ● DASHBOARD     READY               ║
╠══════════════════════════════════════════════════════════════════════╣
║                    >>> READY FOR COMMAND <<<                        ║
╚══════════════════════════════════════════════════════════════════════╝
```

# ⚡ FEATURES

| Core | Capability | State |
|---|---|:---:|
| 🤖 **Heavy HUD** | Animated futuristic command interface | `ACTIVE` |
| 🎙️ **Live Voice** | Real-time conversational voice | `ONLINE` |
| 👁️ **Vision** | Screen + webcam awareness | `READY` |
| 🧠 **Memory** | Persistent local facts/preferences | `ONLINE` |
| ⚙️ **System Control** | Apps, volume, lock, restart, shutdown | `READY` |
| 🧩 **Plugins** | Drop-in Python skills | `READY` |
| 🎙️ **Offline STT** | Whisper / Vosk | `READY` |
| 📱 **Dashboard** | Remote control interface | `READY` |
| 🔐 **Confirmation** | Human confirmation for destructive actions | `ENABLED` |

# 🎙️ COMMANDS

### SYSTEM

```text
Open Chrome
Set volume to 50%
Lock the screen
Restart the computer
Shutdown the computer
Open system settings
```

### FILES

```text
Organize my desktop
Find the PDF on my desktop
Summarize the PDF on my desktop
```

### WEB / BROWSER

```text
Search for the latest AI news
What's the weather in Lahore?
Open youtube.com
Search YouTube for lofi music
```

### PRODUCTIVITY

```text
Add a todo: buy milk
Save a note: meeting at 3pm
Show my todos
```

### VISION / CODE / MEMORY

```text
Look at my screen
What's on my webcam?
Review this code
Write a Python function that sorts a list
Remember that my favorite editor is VS Code
```

### VOICE CONTROL

```text
Hey Jarvis
```

```text
CTRL + SPACE
```

> Restart and shutdown require explicit confirmation in the HUD.

# 🧠 ARCHITECTURE

```text
USER
 │
 ├── 🎙 VOICE / KEYBOARD
 │
 ▼
INPUT + STT
 │
 ▼
X JARVIS ROUTER
 │
 ├──── SYSTEM
 ├──── WEB
 ├──── VISION
 ├──── MEMORY
 ├──── PRODUCTIVITY
 └──── PLUGINS
 │
 ▼
ACTION ENGINE
 │
 ├── TTS
 ├── HUD
 └── RESPONSE
```

# 🚀 QUICK START

## Windows

```powershell
git clone https://github.com/YOUR_USERNAME/X-Jarvis.git
cd X-Jarvis
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python setup.py
python main.py
```

## macOS / Linux

```bash
git clone https://github.com/YOUR_USERNAME/X-Jarvis.git
cd X-Jarvis
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python setup.py
python main.py
```

## Manual dependencies

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium firefox
```

# 🔑 GEMINI SETUP

Create your API key in Google AI Studio:

https://aistudio.google.com/app/apikey

Then:

```bash
python main.py
```

Keep API keys out of Git.

# 🖥️ PLATFORM SUPPORT

```text
Windows 10 / 11    ✓
macOS              ✓
Linux              ✓
Python 3.11–3.13   ✓
GPU                Optional
Microphone         Required for voice
Internet            Required for live cloud voice
```

# 📁 PROJECT STRUCTURE

```text
X-Jarvis/
├── main.py
├── ui.py
├── setup.py
├── requirements.txt
├── README.md
├── LICENSE
├── actions/
├── core/
├── memory/
├── plugins/
├── dashboard/
├── config/
└── assets/
    ├── x-jarvis-heavy-loop.gif
    └── x-jarvis-hero.png
```

# 🔐 SECURITY

```text
✓ API keys excluded from Git
✓ Runtime memory excluded from Git
✓ Destructive actions require confirmation
✓ Review third-party plugins before installing
✓ Do not expose remote dashboards without authentication
✓ Use TLS for remote deployments
```

Recommended `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
config/api_keys.json
config/certs/
memory/long_term.json
.env
.env.*
```

# 🧪 TROUBLESHOOTING

```text
Python not found
→ Install Python and enable PATH

ModuleNotFoundError
→ Activate .venv and run:
  python -m pip install -r requirements.txt

Playwright error
→ python -m playwright install chromium firefox

No microphone
→ Check OS microphone permissions

Shutdown/restart not working
→ Open HUD and press CONFIRM
```

# 🛣️ ROADMAP

```text
[✓] Voice
[✓] Vision foundation
[✓] Memory
[✓] Plugin architecture
[✓] Desktop HUD
[✓] System actions
[✓] Offline STT

[ ] Expanded local AI
[ ] Advanced avatar rendering
[ ] More offline capabilities
[ ] Expanded mobile dashboard
[ ] More OS integrations
```

# 💬 SUPPORT

<div align="center">

<a href="https://whatsapp.com/channel/0029VbBzlMlIt5rzSeMBE922">📢 WHATSAPP CHANNEL</a>

&nbsp; • &nbsp;

<a href="https://chat.whatsapp.com/EPOI1v4hJ6b822unjnlujz">💬 WHATSAPP GROUP</a>

&nbsp; • &nbsp;

<a href="https://t.me/awaishacker1">📱 AWAIS MAYO HACKER</a>

&nbsp; • &nbsp;

<a href="https://wa.me/923295533119">📞 HASEEB HACKER</a>

</div>

# 👥 TEAM

<div align="center">

```text
╔══════════════════════════════════════════════════╗
║                                                  ║
║            AWAIS × HASEEB HACKER TEAM            ║
║                                                  ║
║            POWERED BY X HACKER                   ║
║                  CAPTAIN TEAM                    ║
║                                                  ║
║                    X JARVIS                      ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

</div>

# ⚠️ RESPONSIBLE USE

X JARVIS is intended for authorized personal automation, productivity, accessibility, development, and system administration. Do not use system, browser, file, webcam, microphone, or remote-control capabilities against systems or accounts without authorization.

# 📜 LICENSE

Personal and non-commercial use only.

CC BY-NC 4.0:

https://creativecommons.org/licenses/by-nc/4.0/

<div align="center">

# ⚙️ X JARVIS

```text
HEAR → SEE → THINK → REMEMBER → SPEAK → ACT
```

### `AWAIS × HASEEB HACKER TEAM`

**POWERED BY X HACKER CAPTAIN TEAM**

</div>

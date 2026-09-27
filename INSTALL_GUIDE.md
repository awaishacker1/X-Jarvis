# 📘 X JARVIS — Complete Beginner Installation Guide

**Development By Awais Mayo Hacker × Haseeb Hacker**  
**Powered By X Hacker Captain Team**

This guide is written for complete beginners. Even if you have never used Python or the terminal before, follow the steps carefully and you will have X Jarvis running on your computer.

---

## 📋 What You Need Before Starting

| Item | Required? | Notes |
|------|-----------|-------|
| Computer | Yes | Windows 10/11, macOS, or Linux |
| Internet | Yes (first time) | To download Python, packages, and get free Gemini API key |
| Microphone | Yes | Built-in or external USB mic |
| Speakers / Headphones | Yes | To hear the assistant reply |
| Free Gemini API Key | Yes | Takes 2 minutes from Google (see Step 3) |
| GPU / Graphics Card | **No** | Avatar is drawn in software — works on old laptops |

---

## 🪟 PART 1 — WINDOWS (Most Common)

### Step 1: Install Python 3.11, 3.12 or 3.13

1. Open your browser and go to:  
   **https://www.python.org/downloads/**
2. Click the big yellow button **Download Python 3.x.x** (any 3.11, 3.12 or 3.13 is fine).
3. Run the downloaded installer.
4. **VERY IMPORTANT:** On the first screen tick the box  
   ✅ **Add python.exe to PATH**
5. Click **Install Now**.
6. When finished, click **Close**.

**Check it worked:**
- Press `Windows key + R`
- Type `cmd` and press Enter
- In the black window type:
  ```
  python --version
  ```
- You should see something like `Python 3.12.x`. If you see an error, reinstall Python and make sure "Add to PATH" was ticked.

### Step 2: Get the X-Jarvis Code

**Recommended — Git clone (easiest for updates later):**

1. Install Git if you don't have it: https://git-scm.com/download/win
2. Open Command Prompt or PowerShell and run:
   ```
   git clone https://github.com/YOUR_USERNAME/X-Jarvis.git
   cd X-Jarvis
   ```

**Or — Download ZIP (classic way):**

1. Download the ZIP from the GitHub repo (Code → Download ZIP) and extract it.
2. Go to the extracted folder (the one that contains `main.py`, `setup.py`, `ui.py`).
3. In the address bar of File Explorer, type `cmd` and press Enter.  
   A black terminal window will open **already inside** the X-Jarvis folder.

Alternatively:
- Hold `Shift` + right-click inside the folder → **Open PowerShell window here** or **Open in Terminal**.

### Step 3: Get a Free Gemini API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with any Google account.
3. Click **Create API Key**.
4. Copy the key (it looks like `AIza...` long string). Keep it private.

### Step 4: Install Everything Automatically

In the terminal (black window) that is open inside the X-Jarvis folder, type:

```
python setup.py
```

Press Enter.  
It will download and install all required packages for Windows. This can take 2–10 minutes depending on your internet.

When it finishes you will see a success message.

**If you get an error about pip or permissions:**
```
python -m pip install --upgrade pip
python setup.py
```

### Step 5: Start X Jarvis

Still in the same terminal, type:

```
python main.py
```

- On first launch a setup screen appears.
- Paste your Gemini API key.
- You can also set your name and the assistant name (default is fine).
- Click Save / Continue.

The HUD window will open. Speak or type to talk to X Jarvis.

### Optional: Enable Wake Word ("Hey Jarvis")

1. Inside the app click the ⚙ (settings) gear.
2. Go to **WAKE WORD**.
3. Click the one-click download/install button.
4. Enable it. Now you can say **"Hey Jarvis"** to wake the assistant.

### Optional: Choose Microphone & Speakers

⚙ → **AUDIO DEVICES** → pick your microphone and speakers by name.

### Make it start with Windows (optional)

⚙ → look for Auto-Start / Startup option and enable it.

---

## 🍎 PART 2 — macOS

### Step 1: Install Python

macOS often has an old system Python. Install a proper one:

**Easiest way (recommended):**
1. Install Homebrew if you don’t have it:  
   Open Terminal and paste:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Then install Python:
   ```
   brew install python@3.12
   ```

**Or download from python.org** (same as Windows) and run the macOS installer. Make sure to install the command-line tools when asked.

**Check:**
```
python3 --version
```
Should show 3.11, 3.12 or 3.13.

### Step 2: Get the Code & Open Terminal

**Git clone (recommended):**
```
git clone https://github.com/YOUR_USERNAME/X-Jarvis.git
cd X-Jarvis
```

**Or** download the ZIP, extract it, then:
1. Open Finder and go to the X-Jarvis folder.
2. Right-click the folder → **New Terminal at Folder** (or drag the folder onto the Terminal icon).

### Step 3: Get Gemini API Key

Same as Windows → https://aistudio.google.com/app/apikey

### Step 4: Install

```
python3 setup.py
```

If it complains about permissions:
```
python3 -m pip install --user -r requirements.txt
```

### Step 5: Run

```
python3 main.py
```

Paste your API key on first launch.

**Note on Microphone / Accessibility:**  
macOS may ask for Microphone permission and (for some features) Accessibility / Screen Recording. Allow them when the system prompts appear.

---

## 🐧 PART 3 — Linux (Ubuntu / Debian / Fedora / etc.)

### Step 1: Install Python & System Packages

**Ubuntu / Debian / Linux Mint:**
```
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-dev portaudio19-dev libasound2-dev
```

**Fedora:**
```
sudo dnf install python3 python3-pip portaudio-devel alsa-lib-devel
```

**Arch:**
```
sudo pacman -S python python-pip portaudio
```

Check version:
```
python3 --version
```
Need 3.11+.

### Step 2: Get the Code

**Git clone (recommended):**
```
git clone https://github.com/YOUR_USERNAME/X-Jarvis.git
cd X-Jarvis
```

**Or** if you already downloaded/extracted the ZIP:
```
cd /path/to/X-Jarvis
```

### Step 3: Get Gemini API Key

https://aistudio.google.com/app/apikey

### Step 4: Install

```
python3 setup.py
```

or manually:
```
python3 -m pip install -r requirements.txt
```

### Step 5: Run

```
python3 main.py
```

---

## 🔑 First Launch Checklist (All OS)

1. Paste Gemini API key when asked.
2. Allow microphone access if the OS asks.
3. Speak clearly or type in the input box.
4. ⚙ Settings → you can change:
   - Assistant name
   - Your name
   - Voice (5 Gemini voices)
   - Theme colour
   - Push-to-Talk
   - Wake Word
   - Audio devices
5. Test by saying or typing: “What time is it?” or “Open Notepad” (Windows) / “Open Safari” (macOS).

---

## 🛠️ Common Problems & Solutions

| Problem | Solution |
|---------|----------|
| `python` is not recognized | Reinstall Python and tick **Add to PATH**. Or try `py main.py` on Windows. |
| `ModuleNotFoundError: No module named 'xxx'` | Run `python -m pip install xxx` or re-run `python setup.py` |
| No sound / X Jarvis can’t hear me | ⚙ → AUDIO DEVICES → select the correct microphone and speakers |
| Microphone permission denied | Windows: Settings → Privacy → Microphone → allow. macOS: System Settings → Privacy & Security → Microphone |
| Black / empty window | Make sure you are using Python 3.11–3.13, not 3.10 or older |
| API key error | Create a new key at aistudio.google.com and paste again |
| Antivirus blocks it | Add the X-Jarvis folder to exclusions (common with new Python apps) |
| Wake word not working | Install it from inside the app (⚙ → WAKE WORD). It is optional. |

---

## 📦 What setup.py Installs (for reference)

The installer is smart and only installs what your OS needs. Typical packages include:

- **PyQt6** — the graphical interface (HUD, avatar, settings)
- **numpy** — avatar math and audio processing
- **sounddevice / pyaudio** — microphone and speakers
- **google-genai** — Gemini Live API connection
- **Pillow** — image handling
- **psutil** — hardware monitoring
- OS-specific helpers for volume, brightness, window control, etc.

You do **not** need to install these by hand if you run `python setup.py`.

---

## 📱 Remote Control from Phone (Optional)

1. Start X Jarvis on the computer.
2. Open ⚙ → look for Dashboard / QR / Remote.
3. Scan the QR code with your phone.
4. You can send messages and control the assistant from the phone browser.

---

## 🛠️ Troubleshooting — Errors & Fixes (Beginner)

Agar koi error aaye to pehle yeh table dekho. 90% problems yahin solve ho jati hain.

| Problem | Kya karein |
|---------|------------|
| `python` not recognized | Python re-install karo aur **Add to PATH** tick karo. Phir naya CMD/PowerShell kholo. |
| `ModuleNotFoundError` | Venv activate karo, phir `python setup.py` dobara. Ya `pip install package_name` |
| `pip` missing | `python -m ensurepip --upgrade` |
| API key invalid | https://aistudio.google.com/app/apikey se naya key banao |
| Mic / speakers kaam nahi kar rahe | OS Privacy settings + app ke andar ⚙ → Audio Devices |
| Playwright / browser fail | `python -m playwright install chromium firefox` |
| Slow on old laptop | Normal — GPU zaroori nahi |
| Shutdown/Restart nahi hua | HUD pe **CONFIRM** button dabana zaroori hai (security) |
| Permission denied (Linux) | `python3 -m pip install --user -r requirements.txt` ya venv use karo |

Poora error message copy karke WhatsApp group / Telegram pe bhej sakte ho (neeche links).

---

## 🔒 Privacy Notes (Simple)

- Everything (memory, settings, API key) stays on **your** computer.
- Only your voice goes to Google while you are talking (Gemini Live API).
- When you close the app or mute, nothing is sent.
- You can delete `memory/long_term.json` anytime to make the assistant forget everything.

---

## 📞 Need Help?

**Development By Awais Mayo Hacker × Haseeb Hacker**  
**Powered By X Hacker Captain Team**

| Contact | Link |
|---------|------|
| 📢 WhatsApp Channel | https://whatsapp.com/channel/0029VbBzlMlIt5rzSeMBE922 |
| 💬 WhatsApp Group | https://chat.whatsapp.com/EPOI1v4hJ6b822unjnlujz |
| 📱 Awais Mayo Hacker (Telegram) | @awaishacker1 |
| 📞 Haseeb Hacker (WhatsApp) | 923295533119 |

---

## ✅ Quick Recap (Copy-Paste Commands)

**Windows (after Python is installed and PATH is set):**
```
cd path\to\X-Jarvis
python setup.py
python main.py
```

**macOS / Linux:**
```
cd /path/to/X-Jarvis
python3 setup.py
python3 main.py
```

That’s it. Enjoy your personal AI assistant — **X JARVIS**.

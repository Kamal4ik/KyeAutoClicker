# KyeAutoclicker [Version: 2.0.0]

> **⚠️ IMPORTANT DISCLAIMER**  
> I AM NOT RESPONSIBLE FOR ANY DAMAGE TO YOUR COMPUTER IF YOU USE THIS PROGRAM INCORRECTLY.  
> It is highly recommended to avoid setting a very high CPS (Clicks Per Second) for basic tasks.

---

## 🎯 Introduction

Hello everyone! Have you been looking for an autoclicker that meets your needs? Whether you need it for gaming or everyday tasks, your search ends here. Meet **KyeAutoclicker** — a feature-rich autoclicker with a high-performance click engine, 6 interface languages, a customizable hotkey, and a real-time status monitor to prevent accidental system issues.

---

## 🖥️ What is KyeAutoclicker?

This autoclicker consists of two main windows:

- **Main Control Panel** – The large window where you configure CPS, enable/disable mouse buttons, change language, and set the waiting-mode hotkey.  
  *(Main Window)*

- **Status Window** – A small overlay that shows whether the autoclicker is currently active or not.  
  *(Status Window)*

---

## ⚙️ How It Works

The autoclicker operates on a simple principle:

1. Set CPS values for specific mouse buttons in the main window.
2. Click the big button and press any key — that key now toggles the waiting mode.
3. When waiting mode is **ON**, click LMB or RMB to start/stop the autoclicker.
4. Use checkboxes to disable activation for certain buttons.
   - When a button is disabled, it won't respond to clicks even in waiting mode.
   - This prevents interference with other programs or gameplay.

### 🎮 Practical Example

- Set LMB (Left Mouse Button) values: *(LMB Settings)*
- Test on [cpstest.org](https://cpstest.org) with autoclicker enabled: *(Test Results)*

---

## 🆕 What's New in v2.0.0

### ✨ Added
- 4 new interface languages: 中文（简体）, Français, Português, Español — **6 languages in total**.
- Huge waiting-mode button — clicking it opens a key capture window.
- Customizable hotkey — press any key in the capture window and it becomes the waiting-mode toggle (Esc to cancel). No more hard-coded `G`!
- Support for any key as the hotkey: F-keys, arrows, media keys, non-English layouts.
- Compatibility with older `pynput` versions (automatic fallback).

### 🚀 Changed
- Click engine completely rewritten for high CPS:
  - **SendInput** instead of the legacy `mouse_event` — press + release sent in a single API call.
  - Removed the 5 ms pause inside every click (the old hard ceiling of ~200 CPS).
  - High-resolution timer (`timeBeginPeriod(1)`) + hybrid sleep→spin scheduler with ~0.05 ms accuracy.
  - Zero allocations in the click loop.
  - Own-click filtering now works by source (input signature + injected flag) instead of by timing.
- Language selection moved to a dropdown menu.
- In-app instructions update automatically when you assign a new key.
- All messages, errors and warnings now follow the selected interface language.

### 🐛 Fixed
- Race condition that could enable the clicker and instantly disable it.
- Russian strings appearing in the English interface — all text is now fully localized into 6 languages.
- The pre-start warning now shows the name of your assigned key.
- Predictable clicker shutdown when waiting mode is turned off or the app is closed.

### ⚠️ Known Limitations (not bugs)
- At very high CPS, the program physically cannot distinguish your real click from a programmatic one (intervals become shorter than human reaction time).
- Game anti-cheats detect injected input — do not use in games with anti-cheat.
- The compiled `.exe` may trigger antivirus heuristics (autoclickers are a classic false-positive pattern) — add an exclusion if needed.

---

## ❓ Frequently Asked Questions

**🚀 What's the maximum CPS supported?**  
The new engine handles hundreds of CPS with ease and accepts settings up to several thousand. Real-world performance depends on your CPU and system load.

**💻 Which operating systems are supported?**  
Currently supports Windows 10 and Windows 11.

**🔍 Is the source code available?**  
Yes! You can download the `.py` file and examine the source code.

**🛡️ Is the program virus-free?**  
I have no reason to harm you. The program is completely safe and virus-free (as long as you don't accidentally enable the autoclicker at the wrong time). Note: some antiviruses may flag any compiled autoclicker as suspicious — this is a false positive. You can verify the file yourself using the SHA256 hash below.

**🔄 How do I turn off the autoclicker?**  
Simply click the close button (X) on the main control panel — this will completely terminate the program. Turning waiting mode off also stops all active clickers.

**⌨️ The hotkey doesn't work. What should I do?**  
Since v2.0.0 you are not stuck with `G`! Click the big button and press the key you want while your current keyboard layout is active — the program will remember it. If a key stops responding after a layout switch, just re-assign it in your active layout.

---

## ⚠️ Important Notes

**ATTENTION:**  
The program **CURRENTLY DOES NOT SUPPORT** macOS or Linux, but support for these operating systems may be added in the future.

### 🔧 Current Limitations

- **Fixed Window Size:** Cannot resize windows — working on a solution.
- **Language Support:** Available in English, Русский, 中文（简体）, Français, Português, Español. Found a mistake in a translation or want to add your language? Contact me: [223kamalrty@gmail.com](mailto:223kamalrty@gmail.com)

---

## 📥 Download

**Option 1:** Download from this repository  
Download the `.exe` file directly from this repository.

**Option 2:** Use the direct link  
[https://mega.nz/file/TQNQXIab#KBSpogAqScTZ38Qf3Y5iPn_NgT2wqXpNH-7Rv_99PWg]

### ✅ File verified (Verify File Integrity)

**SHA256 Hash:**  
⟨1cbb968d49be8e7dc56dc7fac1bbb1ca00f9fa569c2b8ae2372036223526b702⟩ — v2.0.0

> **💡 First launch note:** Windows SmartScreen may show a warning for the `.exe` — click **"More info"** → **"Run anyway"**.

---

Happy clicking! 🎯

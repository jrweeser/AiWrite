# 🤖 Human Typing Simulator

A Python script that types text into any active window with realistic human-like imperfections — variable pacing, proximity-based typos, self-corrections, and natural thinking pauses.

---

## Features

- **Keyboard-proximity typos** — mistakes use adjacent keys, just like real misses
- **Self-correction** — sometimes types one extra character before backspacing, mimicking how people notice errors mid-word
- **Variable pacing** — Gaussian-distributed keystroke timing creates natural bursts and slow-downs
- **Sentence-aware pauses** — longer pauses after `.`, `!`, `?`, shorter ones after `,`
- **Thinking pauses** — random mid-sentence pauses simulate someone gathering their thoughts
- **Multi-line input** — supports full paragraphs, line breaks, and tab characters
- **Works anywhere** — Google Docs, Word, Notion, any text field your cursor can reach

---

## Installation

**Requires Python 3.7+**

```bash
pip install pyautogui
```

> **macOS users:** You may need to grant Accessibility permissions to your terminal.  
> Go to **System Settings → Privacy & Security → Accessibility** and add your terminal app.

---

## Usage

### Interactive mode (paste multi-line text)

```bash
python Auto.py
```

Paste or type your text, then press:
- **Mac/Linux:** `Ctrl+D`
- **Windows:** `Ctrl+Z` then `Enter`

### Command-line mode (single string)

```bash
python Auto.py "Your text goes here."
```

After launching, you have **3 seconds** to click into your target window before typing begins.

---

## Configuration

All behavior is controlled by constants at the top of the script:

| Variable | Default | Description |
|---|---|---|
| `DELAY_BEFORE_START` | `3` | Seconds before typing starts (time to switch windows) |
| `BASE_TYPING_SPEED` | `0.08` | Base delay (seconds) between keystrokes |
| `SPEED_VARIANCE` | `0.07` | Gaussian spread on keystroke timing |
| `TYPO_RATE` | `0.04` | Probability of a typo per alphabetic character |
| `CORRECTION_DELAY` | `0.15` | Pause before backspacing a typo |
| `PAUSE_AFTER_WORD` | `0.05` | Extra delay added after spaces |
| `LONG_PAUSE_RATE` | `0.03` | Probability of a "thinking" pause mid-text |
| `LONG_PAUSE_RANGE` | `(0.4, 1.2)` | Duration range (seconds) for thinking pauses |

### Example: Slower, more error-prone typist

```python
BASE_TYPING_SPEED = 0.12
SPEED_VARIANCE    = 0.10
TYPO_RATE         = 0.08
LONG_PAUSE_RATE   = 0.06
```

### Example: Fast, clean typist

```python
BASE_TYPING_SPEED = 0.04
SPEED_VARIANCE    = 0.02
TYPO_RATE         = 0.01
LONG_PAUSE_RATE   = 0.01
```

---

## How It Works

1. **Input** — text is provided via CLI argument or stdin
2. **Countdown** — a configurable delay gives you time to focus the target window
3. **Character loop** — each character is processed individually:
   - A random roll determines if a typo occurs
   - The typo character is drawn from a `NEARBY_KEYS` map of keyboard-adjacent letters
   - Sometimes a second character is typed before the error is caught and deleted
   - The correct character is then typed
   - A randomized delay is applied before moving to the next character
4. **Pacing modifiers** — spaces, commas, and sentence-ending punctuation each add their own delay on top of the base timing

---

## Requirements

| Package | Version |
|---|---|
| `pyautogui` | ≥ 0.9.53 |
| Python | ≥ 3.7 |

---

## Notes & Limitations

- **Focus the window yourself** — the script types wherever your cursor is; it does not click into a specific app
- **Autocorrect interference** — apps like Google Docs may autocorrect typos before the script can delete them, which can cause unexpected behavior. Consider disabling autocorrect while running
- **Do not move the mouse** — `pyautogui` uses global input; moving the mouse or clicking elsewhere mid-run will interrupt typing
- **Long texts** — for very long inputs, consider increasing `DELAY_BEFORE_START` to ensure you have time to switch windows

---

## License

MIT

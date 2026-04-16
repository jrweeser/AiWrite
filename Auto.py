import pyautogui
import time
import random
import sys

# --- Configuration ---
DELAY_BEFORE_START = 3      # seconds to switch to your target window
BASE_TYPING_SPEED = 0.08    # base seconds between keystrokes
SPEED_VARIANCE = 0.07       # randomness in typing speed
TYPO_RATE = 0.04            # ~4% chance of a typo per character
CORRECTION_DELAY = 0.15     # pause before correcting a typo
PAUSE_AFTER_WORD = 0.05     # extra pause after spaces
LONG_PAUSE_RATE = 0.03      # ~3% chance of a longer "thinking" pause
LONG_PAUSE_RANGE = (0.4, 1.2)  # range for "thinking" pauses in seconds

NEARBY_KEYS = {
    'a': 'sqzw', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wrsdf',
    'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'uojkl', 'j': 'huikmn',
    'k': 'jiolm', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iplk',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx', ' ': ' ',
}

def get_typo(char):
    """Return a nearby key typo for a given character."""
    lower = char.lower()
    if lower in NEARBY_KEYS and len(NEARBY_KEYS[lower]) > 0:
        return random.choice(NEARBY_KEYS[lower])
    return char

def human_type(text):
    """Type text with human-like imperfections."""
    print(f"Starting in {DELAY_BEFORE_START} seconds... Switch to your target window!")
    time.sleep(DELAY_BEFORE_START)
    print("Typing...")

    i = 0
    while i < len(text):
        char = text[i]

        # Random "thinking" pause
        if random.random() < LONG_PAUSE_RATE:
            time.sleep(random.uniform(*LONG_PAUSE_RANGE))

        # Simulate a typo
        if char.isalpha() and random.random() < TYPO_RATE:
            typo_char = get_typo(char)
            pyautogui.typewrite(typo_char, interval=0)
            time.sleep(random.uniform(0.1, CORRECTION_DELAY))

            # Sometimes type one more char before noticing
            if random.random() < 0.4 and i + 1 < len(text):
                pyautogui.typewrite(text[i + 1], interval=0)
                time.sleep(random.uniform(0.1, 0.3))
                pyautogui.hotkey('backspace')
                time.sleep(0.05)

            pyautogui.hotkey('backspace')
            time.sleep(random.uniform(0.05, 0.15))

        # Type the actual character
        if char == '\n':
            pyautogui.press('enter')
        elif char == '\t':
            pyautogui.press('tab')
        else:
            pyautogui.typewrite(char, interval=0)

        # Pacing
        delay = BASE_TYPING_SPEED + random.gauss(0, SPEED_VARIANCE)
        delay = max(0.02, delay)  # never go negative

        if char == ' ':
            delay += PAUSE_AFTER_WORD
        elif char in '.!?':
            delay += random.uniform(0.2, 0.6)  # pause at end of sentences
        elif char == ',':
            delay += random.uniform(0.05, 0.2)

        time.sleep(delay)
        i += 1

    print("\nDone typing!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Text passed as a command-line argument
        input_text = " ".join(sys.argv[1:])
    else:
        # Prompt for multi-line input
        print("Paste or type your text below.")
        print("When done, press Enter then Ctrl+D (Mac/Linux) or Ctrl+Z + Enter (Windows):\n")
        lines = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            pass
        input_text = "\n".join(lines)

    if not input_text.strip():
        print("No text provided. Exiting.")
        sys.exit(1)

    human_type(input_text)
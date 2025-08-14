from machine import Pin
import time, random

# Relay on GP1
relay_pin = Pin(1, Pin.OUT)

# Onboard LED on Pico W (optional)
led_pin = Pin("LED", Pin.OUT)

# Morse code map
MORSE = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',  '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', '.': '.-.-.-', ',': '--..--', '?': '..--..', '=': '-...-', 
    ' ': ' '
}

# Default WPM
wpm = 12
memories = [""] * 6   # memory slots !1..6

def play_symbol(symbol, unit):
    if symbol == '.':
        key_down(unit)
    elif symbol == '-':
        key_down(unit * 3)
    time.sleep(unit / 1000)  # inter-symbol gap

def key_down(duration_ms):
    relay_pin.value(1)
    led_pin.value(1)
    time.sleep(duration_ms / 1000.0)
    relay_pin.value(0)
    led_pin.value(0)

def send_morse(message):
    global wpm
    unit = 1200 / wpm
    message = message.upper()

    for ch in message:
        code = MORSE.get(ch, "")
        for symbol in code:
            play_symbol(symbol, unit)
        time.sleep((unit * 3) / 1000.0)  # gap between letters
    time.sleep((unit * 4) / 1000.0)      # gap after message

def dot_mode():
    unit = 1200 / wpm
    print("Dot mode: Sending dots... Press CTRL+C to stop.")
    try:
        while True:
            key_down(unit)
            time.sleep(unit / 1000.0)
    except KeyboardInterrupt:
        print("\nStopped dot mode.")

def tone_mode():
    unit = 1200 / wpm
    print("Tone mode: Continuous tone... Press CTRL+C to stop.")
    try:
        while True:
            key_down(unit)  # hold tone continuously
    except KeyboardInterrupt:
        relay_pin.value(0)
        led_pin.value(0)
        print("\nStopped tone mode.")

def repeat_text(text):
    for i in range(3):
        send_morse(text)
        time.sleep(1)

def random_groups(n):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for i in range(n):
        group = "".join(random.choice(chars) for _ in range(5))
        print(group)
        send_morse(group)
        time.sleep(1)

def show_help():
    print("\nHelp — Command Reference:")
    print("  *       Exit the program")
    print("  + / -   Increase/decrease speed (WPM)")
    print("  @       Send continuous dots (scope calibration)")
    print("  #       Send continuous tone (frequency counter)")
    print("  #H      Show this help message")
    print("  [text]  Repeat text 3 times with pauses")
    print("  {N}     Send N lines of random 5-character groups")
    print("  !1–!6   Store text into memory slot 1–6")
    print("  $1–$6   Insert text from memory slot 1–6")
    print("  Any other text — Sent as Morse code\n")

def main():
    global wpm, memories
    print("\nZS6BVR Morse Sender (Raspberry Pi Pico W) V2.0")
    print("Type message and press ENTER")
    print("Type #H for help\n")

    while True:
        msg = input("> ").strip()

        if msg == "*":
            break
        elif msg in {"+", "++"}:
            wpm += 5
            print("WPM:", wpm)
        elif msg in {"-", "--"}:
            wpm = max(1, wpm - 5)
            print("WPM:", wpm)
        elif msg == "@":
            dot_mode()
        elif msg == "#":
            tone_mode()
        elif msg.upper() == "#H":
            show_help()
        elif msg.startswith("[") and msg.endswith("]"):
            repeat_text(msg[1:-1])
        elif msg.startswith("{") and msg.endswith("}"):
            try:
                n = int(msg[1:-1])
                random_groups(n)
            except ValueError:
                print("Invalid {N} format")
        elif msg.startswith("!"):
            try:
                slot = int(msg[1]) - 1
                if 0 <= slot < 6:
                    memories[slot] = msg[2:].strip()
                    print(f"Mem{slot+1} stored.")
                else:
                    print("Invalid memory slot. Use !1–!6")
            except:
                print("Invalid memory command")
        elif msg.startswith("$"):
            try:
                slot = int(msg[1]) - 1
                if 0 <= slot < 6:
                    text = memories[slot]
                    print(text)
                    send_morse(text)
                else:
                    print("Invalid memory slot. Use $1–$6")
            except:
                print("Invalid recall command")
        else:
            print("Sending:", msg)
            send_morse(msg)

if __name__ == "__main__":
    main()


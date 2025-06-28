from machine import Pin
import time

# Setup GPIO pin 2 (GP1) as output
relay_pin = Pin(1, Pin.OUT)  # GP1

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

# Default WPM (Words Per Minute)
wpm = 12

def play_symbol(symbol, unit):
    if symbol == '.':
        key_down(unit)
    elif symbol == '-':
        key_down(unit * 3)
    time.sleep(unit / 1000)  # Inter-symbol gap

def key_down(duration_ms):
    relay_pin.value(1)
    time.sleep(duration_ms / 1000.0)
    relay_pin.value(0)

def send_morse(message):
    global wpm
    unit = 1200 / wpm  # standard timing formula: dot duration in ms
    message = message.upper()

    for ch in message:
        code = MORSE.get(ch, "")
        for symbol in code:
            play_symbol(symbol, unit)
        time.sleep((unit * 3) / 1000.0)  # Between letters
    time.sleep((unit * 4) / 1000.0)  # End of message pause

def main():
    global wpm
    print("\nZS6BVR Morse Sender (Raspberry Pi Pico)")
    print("Type message and press ENTER")
    print("Special keys: * = quit, + = faster, - = slower, @ = dots mode\n")

    while True:
        msg = input("> ").strip().upper()
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
        else:
            print("Sending:", msg)
            send_morse(msg)

def dot_mode():
    unit = 1200 / wpm
    print("Dot mode: Sending dots... Press CTRL+C to stop.")
    try:
        while True:
            key_down(unit)
            time.sleep(unit / 1000.0)
    except KeyboardInterrupt:
        print("\nStopped dot mode.")

# Run the main loop
if __name__ == "__main__":
    main()



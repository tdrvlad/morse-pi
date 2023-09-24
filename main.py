import RPi.GPIO as GPIO
import time
from collections import deque

BUTTON_PIN = 27
DOT_DURATION = 0.3
DASH_DURATION = 0.7
DEBOUNCE_TIME = 0.05

WINDOW_SIZE = 5  # Max number of Morse symbols to look back for conversion

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', 
    '8': '---..', '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..', "'": '.----.', 
    '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...', ';': '-.-.-.', 
    '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.', '$': '...-..-', '@': '.--.-.'
}

# Deque will allow us to maintain a moving window buffer of dots/dashes
buffer = deque(maxlen=WINDOW_SIZE)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def get_morse_code():
    pressed_time = 0
    while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
        pressed_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)
    
    if pressed_time < DOT_DURATION:
        return '.'
    elif pressed_time < DASH_DURATION:
        return '-'
    else:
        return ''

def morse_to_text(morse_code):
    return MORSE_CODE_DICT.get(morse_code, "")

try:
    print("Waiting for button press...")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            code = get_morse_code()
            if code:
                print(code, end='', flush=True)
                buffer.append(code)
                
                # # Convert buffer to text
                # morse_string = ''.join(buffer)
                # text = morse_to_text(morse_string)
                # if text:
                #     print(f" [{text}] ", end='', flush=True)
                #     buffer.clear()  # Clear the buffer if we found a valid letter/symbol
                    
            time.sleep(DEBOUNCE_TIME)
        time.sleep(DEBOUNCE_TIME)
        
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    GPIO.cleanup()

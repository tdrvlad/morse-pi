import RPi.GPIO as GPIO
import time
from config import MORSE_INPUT_PIN, TIME_UNIT, DOT_DURATION, DASH_DURATION, LETTER_SPACE_DURATION, WORD_SPACE_DURATION, DEBOUNCE_TIME, MORSE_CODE_DICT
from utils import write_centered_texts

GPIO.setmode(GPIO.BCM)
GPIO.setup(MORSE_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def decode_morse(morse_code):
    words = morse_code.split('   ')
    decoded_words = []

    for word in words:
        letters = word.split()
        decoded_word = ''.join([key for letter in letters for key, value in MORSE_CODE_DICT.items() if letter == value])
        decoded_words.append(decoded_word)

    return ' '.join(decoded_words)


def get_morse_code():
    pressed_time = 0
    while GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
        pressed_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)

    if 0 < pressed_time < DOT_DURATION:
        return '.'
    elif pressed_time < DASH_DURATION:
        return '-'
    elif pressed_time < LETTER_SPACE_DURATION:
        return ''
    elif pressed_time < WORD_SPACE_DURATION:
        return ' '  # Space between letters
    else:
        return '   '  # Space between words


try:
    print("Waiting for button press...")
    morse_string = ''
    decoded = ''
    while True:
        if GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
            code = get_morse_code()
            if code:
                morse_string += code
                print(code, end='', flush=True)
                if code == '   ':
                    decoded += decode_morse(morse_string.strip())
                    print(f"\nDecoded: {decoded}")
                    morse_string = ''
                write_centered_texts([morse_string, decoded])
            time.sleep(DEBOUNCE_TIME)
        else:
            if morse_string:
                time_since_last_press = 0
                while GPIO.input(MORSE_INPUT_PIN) == GPIO.LOW and time_since_last_press < WORD_SPACE_DURATION:
                    time_since_last_press += DEBOUNCE_TIME
                    time.sleep(DEBOUNCE_TIME)

                if time_since_last_press >= WORD_SPACE_DURATION:
                    decoded += decode_morse(morse_string.strip())
                    print(f"\nDecoded: {decoded}")
                    morse_string = ''
                    write_centered_texts([morse_string, decoded])
            time.sleep(DEBOUNCE_TIME)

except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    GPIO.cleanup()

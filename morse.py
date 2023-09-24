import RPi.GPIO as GPIO
import time
from config import (
    MORSE_INPUT_PIN, TIME_UNIT, DOT_DURATION, DASH_DURATION,
    LETTER_SPACE_DURATION, WORD_SPACE_DURATION, DEBOUNCE_TIME,
    MORSE_CODE_DICT, INACTIVITY_THRESHOLD
)
from display import write_centered_text, display_morse_alphabet

GPIO.setmode(GPIO.BCM)
GPIO.setup(MORSE_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def decode_morse(morse_code):
    words = morse_code.split('   ')
    return ' '.join([
        ''.join([
            key for letter in word.split()
            for key, value in MORSE_CODE_DICT.items()
            if letter == value
        ])
        for word in words
    ])


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
        return ' '
    else:
        return '   '


def time_since_button_released():
    released_time = 0
    while GPIO.input(MORSE_INPUT_PIN) == GPIO.LOW and released_time < WORD_SPACE_DURATION:
        released_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)
    return released_time


def print_current(morse_string, decoded_string, last_symbol):
    if last_symbol:
        print(f"MORSE: {morse_string}\nDECODED: {decoded_string}")
        write_centered_text(decoded_string)


def main_loop():
    print("Waiting for button press...")
    all_morse_string = ""
    morse_string = ''
    decoded = ''
    last_activity_time = time.time()
    last_symbol = None

    # Display Morse alphabet initially
    display_morse_alphabet()

    while True:
        current_time = time.time()

        if GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
            code = get_morse_code()
            all_morse_string += code
            morse_string += code

            if code:
                last_symbol = code.strip()
                if last_symbol:
                    decoded += decode_morse(last_symbol)
                    print_current(all_morse_string, decoded, last_symbol)
                    last_symbol = None

            last_activity_time = current_time
            time.sleep(DEBOUNCE_TIME)

        else:
            released_duration = time_since_button_released()
            if released_duration >= WORD_SPACE_DURATION:
                last_symbol = decode_morse(morse_string.strip())
                if last_symbol:
                    decoded += " " + last_symbol
                    all_morse_string += " "
                    print_current(all_morse_string, decoded, last_symbol)
                    last_symbol = None

            # Check for inactivity
            if current_time - last_activity_time > INACTIVITY_THRESHOLD:
                display_morse_alphabet()
                last_activity_time = current_time

            time.sleep(DEBOUNCE_TIME)


try:
    main_loop()
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    GPIO.cleanup()

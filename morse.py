import RPi.GPIO as GPIO
import time
from config import (
    MORSE_INPUT_PIN, TIME_UNIT, DOT_DURATION, DASH_DURATION,
    LETTER_SPACE_DURATION, WORD_SPACE_DURATION, DEBOUNCE_TIME,
    MORSE_CODE_DICT, INACTIVITY_THRESHOLD
)
from display import Display

GPIO.setmode(GPIO.BCM)
GPIO.setup(MORSE_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

display = Display()


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


def get_morse():
    pressed_time = 0
    while GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
        pressed_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)

    if 0 < pressed_time < DOT_DURATION:
        return '.'
    elif pressed_time < DASH_DURATION:
        return '-'
    else:
        return ' '


def print_current(morse_string, decoded_string):
    print(f"MORSE: {morse_string}\nDECODED: {decoded_string}")
    # display.write(decoded_string[:30], x=50,  y=50, font_size=20)


def time_since_button_released():
    released_time = 0
    while GPIO.input(MORSE_INPUT_PIN) == GPIO.LOW and released_time < WORD_SPACE_DURATION:
        released_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)
    return released_time


def main_loop():
    print("Waiting for button press...")
    last_morse_letter = None
    all_morse_words = ""
    morse_word = ''
    decoded_words = ''
    last_button_pressed_timestamp = time.time()
    display.display_morse_alphabet()

    while True:
        decoded = None
        morse_letter = None
        if GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
            morse_letter = get_morse()
            last_button_pressed_timestamp = time.time()

        if time.time() - last_button_pressed_timestamp > LETTER_SPACE_DURATION:
            morse_letter = ' '

        if time.time() - last_button_pressed_timestamp > WORD_SPACE_DURATION:
            morse_letter = '\n'

        if morse_letter != last_morse_letter and morse_letter is not None:
            morse_word += morse_letter
            all_morse_words += morse_letter
            last_morse_letter = morse_letter

        if len(morse_word.strip()) > 0:
            decoded = decode_morse(morse_word.strip())
            morse_word = ''
            decoded_words += decoded
            print_current(all_morse_words, decoded_words)

        if time.time() - last_button_pressed_timestamp > INACTIVITY_THRESHOLD:
            # display.display_morse_alphabet()
            pass

        time.sleep(DEBOUNCE_TIME)

try:
    main_loop()
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    GPIO.cleanup()

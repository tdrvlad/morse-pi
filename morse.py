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


def print_current(morse_string, decoded_string):
    print(f"MORSE: {morse_string}\nDECODED: {decoded_string}")
    display.write(decoded_string[:30], x=50,  y=50, font_size=20)


def time_since_button_released():
    released_time = 0
    while GPIO.input(MORSE_INPUT_PIN) == GPIO.LOW and released_time < WORD_SPACE_DURATION:
        released_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)
    return released_time


def main_loop():
    print("Waiting for button press...")
    all_morse_string = ""
    morse_string = ''
    decoded = ''
    previous_decoded = None  # To store the last known decoded string

    while True:
        if GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
            code = get_morse_code()
            all_morse_string += code
            morse_string += code

            if code == '   ':
                all_morse_string += " "
                decoded += decode_morse(morse_string.strip())
                morse_string = ''

                # Check if the decoded message changed and print it
                if decoded != previous_decoded:
                    print_current(all_morse_string, decoded)
                    previous_decoded = decoded

            time.sleep(DEBOUNCE_TIME)

        else:
            released_duration = time_since_button_released()
            if released_duration >= WORD_SPACE_DURATION:
                decoded += " "
                decoded += decode_morse(morse_string.strip())
                morse_string = ''
                all_morse_string += " "

                # Check if the decoded message changed and print it
                if decoded != previous_decoded:
                    print_current(all_morse_string, decoded)
                    previous_decoded = decoded

            if released_duration > INACTIVITY_THRESHOLD:
                display.display_morse_alphabet()
            time.sleep(DEBOUNCE_TIME)


try:
    main_loop()
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    GPIO.cleanup()

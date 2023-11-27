#!/usr/bin/env python3
import sys
import os

# Append the repo path to the PYTHONPATH so that the display import works
repo_path = os.path.dirname(__file__)
print(repo_path)
sys.path.append(repo_path)

import RPi.GPIO as GPIO
import time
from config import (
    MORSE_INPUT_PIN, TIME_UNIT, DOT_DURATION, DASH_DURATION,
    LETTER_SPACE_DURATION, WORD_SPACE_DURATION, DEBOUNCE_TIME,
    MORSE_CODE_DICT, INACTIVITY_THRESHOLD, RESET_BUTTON
)
from display import Display

GPIO.setmode(GPIO.BCM)
GPIO.setup(MORSE_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RESET_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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


def check_reset_button():
    pressed_time = 0
    if GPIO.input(RESET_BUTTON) == GPIO.LOW:
        return False

    print("Reset button pushed.")
    while GPIO.input(RESET_BUTTON) == GPIO.HIGH:
        print("Reset button active.")
        pressed_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)

    if pressed_time > DEBOUNCE_TIME:
        return True
    return False


def get_morse_unit():
    pressed_time = 0
    if GPIO.input(MORSE_INPUT_PIN) == GPIO.LOW:
        return None

    print("Morse input detected.")
    while GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
        print("Morse input active.")
        pressed_time += DEBOUNCE_TIME
        time.sleep(DEBOUNCE_TIME)

    if 0 < pressed_time < DOT_DURATION:
        return '.'
    elif pressed_time < DASH_DURATION:
        return '-'
    elif pressed_time < LETTER_SPACE_DURATION:
        return ' '
    else:
        return None


def print_current(morse_string, decoded_string):
    print(f"MORSE: {morse_string}\nDECODED: {decoded_string}")
    display.write(decoded_string[-8:], x=25,  y=None, font_size=40)


# def time_since_button_released():
#     released_time = 0
#     while GPIO.input(MORSE_INPUT_PIN) == GPIO.LOW and released_time < WORD_SPACE_DURATION:
#         released_time += DEBOUNCE_TIME
#         time.sleep(DEBOUNCE_TIME)
#     return released_time


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
        if check_reset_button():
            all_morse_words = ""
            morse_word = ''
            decoded_words = ''
            print_current(all_morse_words, decoded_words)
            last_button_pressed_timestamp = time.time()

        if GPIO.input(MORSE_INPUT_PIN) == GPIO.HIGH:
            morse_letter = get_morse_unit()
            if morse_letter is None:
                all_morse_words = ""
                decoded_words = ''
                morse_letter = " "
                print_current(all_morse_words, decoded_words)
            last_button_pressed_timestamp = time.time()

        if time.time() - last_button_pressed_timestamp > LETTER_SPACE_DURATION:
            morse_letter = ' '

        if time.time() - last_button_pressed_timestamp > WORD_SPACE_DURATION:
            morse_letter = '   '

        if morse_letter is not None:
            morse_word = morse_word.strip() + morse_letter

        if len(morse_word.strip()) > 0 and time.time() - last_button_pressed_timestamp > WORD_SPACE_DURATION:
            decoded = decode_morse(morse_word.strip())
            all_morse_words += morse_word
            morse_word = ''
            decoded_words += decoded
            print_current(all_morse_words, decoded_words)

        if time.time() - last_button_pressed_timestamp > INACTIVITY_THRESHOLD:
            display.display_morse_alphabet()
        time.sleep(DEBOUNCE_TIME)

try:
    main_loop()
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    GPIO.cleanup()

import RPi.GPIO as GPIO
import time
from utils import MORSE_CODE_DICT as morse_dict, clear_screen_white, write_centered_text

# Setup the GPIO pins
GPIO.setmode(GPIO.BCM)  # Use BCM mode
BUTTON_PIN = 27
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

DOT_DURATION = 0.2
DASH_DURATION = 0.6
LETTER_GAP = 0.7


def get_morse_signal():
    morse_code = ""
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            press_start = time.time()
            while GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                time.sleep(0.01)
            press_duration = time.time() - press_start
            
            if press_duration < DOT_DURATION:
                morse_code += "."
                write_centered_text(morse_code, 72)
            elif press_duration < DASH_DURATION:
                morse_code += "-"
                write_centered_text(morse_code, 72)
            else:
                break

            # Wait to check for space or another morse signal
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.01)
                if time.time() - press_start > LETTER_GAP:
                    return morse_dict.get(morse_code, None)

def main():
    print("Waiting for Morse input...")
    clear_screen_white()
    while True:
        letter = get_morse_signal()
        if letter:
            write_centered_text(letter, 72)
        else:
            clear_screen_white()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen_white()
        GPIO.cleanup()
        print("\nScript terminated.")

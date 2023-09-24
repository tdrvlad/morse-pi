import RPi.GPIO as GPIO
import time

BUTTON_PIN = 27
DOT_DURATION = 0.3  # Duration (in seconds) for a button press to be considered a 'dot'
DASH_DURATION = 0.7  # Duration (in seconds) for a button press to be considered a 'dash'
DEBOUNCE_TIME = 0.05  # Time (in seconds) to debounce button presses

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

try:
    print("Waiting for button press...")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            code = get_morse_code()
            if code:
                print(code, end='', flush=True)
            time.sleep(DEBOUNCE_TIME)
        time.sleep(DEBOUNCE_TIME)
        
except KeyboardInterrupt:
    print("\nScript terminated by user.")
finally:
    GPIO.cleanup()

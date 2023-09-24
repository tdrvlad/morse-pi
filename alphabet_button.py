import RPi.GPIO as GPIO
from utils import display_morse_alphabet, epd2in9_V2, Image, ImageDraw, PICDIR

# Setup the GPIO pins
GPIO.setmode(GPIO.BCM)  # Use BCM mode
BUTTON_PIN = 27
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def clear_screen(epd):
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()

def main():
    epd = epd2in9_V2.EPD()
    while True:
        # Check if button is pressed
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            display_morse_alphabet(epd)
        else:
            clear_screen(epd)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nScript terminated.")




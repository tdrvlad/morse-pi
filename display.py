import sys
import os
import logging
from config import MORSE_CODE_DICT
import time

PICDIR = os.getenv('EPAPER_LIB_DIR', "./e-Paper/RaspberryPi_JetsonNano/python/pic")
LIBDIR = os.getenv('EPAPER_PIC_DIR', "./e-Paper/RaspberryPi_JetsonNano/python/lib")

if not os.path.exists(LIBDIR):
    raise ValueError("Lib not found.")
sys.path.append(LIBDIR)

from waveshare_epd import epd2in9_V2
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)
epd = epd2in9_V2.EPD()

import functools

def skip_duplicate_calls(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Use a unique identifier for the method and its arguments
        current_call = (func.__name__, args, frozenset(kwargs.items()))

        # If the current call matches the last call, skip it
        if hasattr(self, '_last_call') and self._last_call == current_call:
            # print(f"Skipped duplicate call: {func.__name__}")
            return

        # Store the current call as the last call
        self._last_call = current_call

        return func(self, *args, **kwargs)

    return wrapper


class Display:
    def __init__(self):
        epd.init()
        last_text = None
        print('Initialized Display')

    @skip_duplicate_calls
    def black_screen(self):
        epd.Clear(0x00)

    @skip_duplicate_calls
    def white_screen(self):
        epd.Clear(0xFF)

    @skip_duplicate_calls
    def write(self, text, font_size, x=20, y=20):
        print(f"Writing: {text}.")
        font = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), font_size)

        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)
        text_width, text_height = draw.textsize(text, font=font)

        if x is None:
            x = (epd.height - text_width) / 2
        if y is None:
            y = (epd.width - text_height) / 2

        draw.text((x, y), text, font=font, fill=0)
        epd.display(epd.getbuffer(Himage))

    @skip_duplicate_calls
    def display_morse_alphabet(self, start_x=5, start_y=3, font_size=14, line_gap=3, column_width=60):
        print("Displaying Morse Alphabet")
        font = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), font_size)
        Himage = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(Himage)

        x, y = start_x, start_y
        line_height = font_size + line_gap

        # Loop through Morse code dict and display each letter and its Morse code
        for char, morse in MORSE_CODE_DICT.items():
            text = f"{char.upper()} {morse}"

            # If the next line would go off the screen, move to the next column
            if y + line_height > epd.width - start_y:
                y = start_y
                x += column_width

            draw.text((x, y), text, font=font, fill=0)
            y += line_height

        epd.display(epd.getbuffer(Himage))

    def sleep(self):
        epd.sleep()



if __name__ == '__main__':
    display = Display()
    time.sleep(1)
    display.write("C", font_size=20)
    time.sleep(1)
    display.write("C", font_size=20)
    time.sleep(1)
    display.write("C", font_size=20)
    time.sleep(1)
    display.write("C", font_size=20)



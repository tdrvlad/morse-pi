#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time

PICDIR = "./e-Paper/RaspberryPi_JetsonNano/python/pic"
LIBDIR = "./e-Paper/RaspberryPi_JetsonNano/python/lib"

if not os.path.exists(LIBDIR):
    raise ValueError("Lib not found.")
sys.path.append(LIBDIR)

from waveshare_epd import epd2in9_V2
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

def clear_screen_white(epd):
    """Clears the screen to white color."""
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()

def clear_screen_black(epd):
    """Clears the screen to black color."""
    epd.init()
    epd.Clear(0x00)  # Full black
    epd.sleep()

def write_centered_text(epd, text, font_size):
    """Writes the provided text centered on the screen with the given font size."""
    epd.init()
    epd.Clear(0xFF)
    font = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), font_size)
    
    # Create an image to draw on
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    
    # Get text width and height
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate X, Y position of the text
    x = (epd.height - text_width) / 2
    y = (epd.width - text_height) / 2

    draw.text((x, y), text, font=font, fill=0)
    epd.display(epd.getbuffer(Himage))
    epd.sleep()

MORSE_CODE_DICT = {
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".",
    "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---",
    "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---",
    "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-",
    "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--",
    "z": "--..", ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--",
    "-": "-....-", "/": "-..-.", "@": ".--.-.", "(": "-.--.", ")": "-.--.-"
}

def display_morse_alphabet(epd):
    epd.init()
    epd.Clear(0xFF)
    
    # Set the font size and create a new image
    font_size = 8
    font = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), font_size)
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)
    
    # Starting position for drawing
    x, y = 3, 3
    line_height = font_size + 2

    # Loop through Morse code dict and display each letter and code
    for char, morse in MORSE_CODE_DICT.items():
        text = f"{char.upper()}: {morse}"
        
        # If the next line would go off the screen, we stop
        if y + line_height > epd.width:
            break
        
        draw.text((x, y), text, font=font, fill=0)
        y += line_height
        
        # If a column is filled, move to the next column
        if y + line_height > epd.width - 10:
            y = 10
            x += 100  # adjust the spacing as needed

    epd.display(epd.getbuffer(Himage))
    epd.sleep()

# Test the function
epd = epd2in9_V2.EPD()
display_morse_alphabet(epd)

#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import time
from config import MORSE_CODE_DICT

PICDIR = "./e-Paper/RaspberryPi_JetsonNano/python/pic"
LIBDIR = "./e-Paper/RaspberryPi_JetsonNano/python/lib"

if not os.path.exists(LIBDIR):
    raise ValueError("Lib not found.")
sys.path.append(LIBDIR)

from waveshare_epd import epd2in9_V2
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)
epd = epd2in9_V2.EPD()


def clear_screen_white():
    """Clears the screen to white color."""
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()

def clear_screen_black():
    """Clears the screen to black color."""
    epd.init()
    epd.Clear(0x00)  # Full black
    epd.sleep()

def write_centered_text(text, font_size=12):
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


def write_centered_texts(texts, font_size=12):
    """Writes the provided text centered on the screen with the given font size."""
    epd.init()
    epd.Clear(0xFF)
    font = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), font_size)

    # Create an image to draw on
    Himage = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(Himage)

    # Calculate total height of all lines combined
    total_text_height = sum([draw.textsize(line, font=font)[1] for line in texts])

    # Calculate starting Y position
    y = (epd.width - total_text_height) / 2

    for text in texts:
        # Get text width for the current line
        text_width, text_height = draw.textsize(text, font=font)

        # Calculate X position of the text
        x = (epd.height - text_width) / 2

        draw.text((x, y), text, font=font, fill=0)

        # Move the Y position down for the next line
        y += text_height

    epd.display(epd.getbuffer(Himage))
    epd.sleep()



def display_morse_alphabet(start_x=5, start_y=5, font_size=14, line_gap=3, column_width = 60):
    # epd.init()
    epd.Clear(0xFF)
    
    # Set a smaller font size and create a new image
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
    epd.sleep()

# Test the function
display_morse_alphabet()

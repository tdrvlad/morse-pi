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

# Test the functions
epd = epd2in9_V2.EPD()
clear_screen_white(epd)
time.sleep(2)
clear_screen_black(epd)
time.sleep(2)
write_centered_text(epd, "Hello World", 24)


# try:
#     logging.info("epd2in9 V2 Demo") 
#     epd = epd2in9_V2.EPD()

#     logging.info("init and Clear")
#     epd.init()
#     epd.Clear(0xFF)

#     font24 = ImageFont.truetype(os.path.join(PICDIR, 'Font.ttc'), 24)

#     # Drawing on the Horizontal image
#     logging.info("Drawing on the Horizontal image...")
#     Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
#     draw = ImageDraw.Draw(Himage)
#     draw.text((10, 0), 'Hello world', font=font24, fill=0)
#     epd.display(epd.getbuffer(Himage))

#     logging.info("Goto Sleep...")
#     epd.sleep()

# except IOError as e:
#     logging.info(e)

# except KeyboardInterrupt:    
#     logging.info("ctrl + c:")
#     epd2in9_V2.epdconfig.module_exit()
#     exit()

# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

from themes import getTheme as getTheme
from themes import changeTheme as changeTheme

class Popup(object):

    def __init__(self):
        pass

    def draw(self, drawO):
        print('Popup.draw()')
        drawO.rectangle([(20, 40), (110, 100)], fill=(0, 0, 0, 255), outline=(255, 0, 0, 255))
        drawO.text((25, 60), 'Are you sure?', fill=getTheme()["headline_color"])

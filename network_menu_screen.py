# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import LCD_1in44
import LCD_Config
import datetime
import time
import math
from PIL import Image, ImageDraw, ImageFont, ImageColor
from themes import getTheme as getTheme
from themes import changeTheme as changeTheme
from screen import Screen
from threading import Timer
from menu_screen import MenuScreen

class NetworkMenuScreen(MenuScreen):
    def __init__(self, LCD, screenManager):
        # super(NetworkMenuScreen, self, LCD, screenManager).__init__()
        super(NetworkMenuScreen, self).__init__(LCD, screenManager)
        # print("MenuScreen.MenuScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentline = 0
        self.menu_headline_text = 'N E T W O R K'
        self.entries = [
            {"name": "Status", "screenname": "network_status"},
            {"name": "Wifi", "screenname": "network_wifi"}
        ]

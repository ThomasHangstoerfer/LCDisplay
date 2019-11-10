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

class MainMenuScreen(MenuScreen):
    def __init__(self, LCD, screenManager):
        super(MainMenuScreen, self).__init__(LCD, screenManager)
        # print("MainMenuScreen.MainMenuScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentline = 0
        self.menu_headline_text = 'M A I N'
        self.entries = [
            {"name": "SmartHome", "screenname": "smarthome"},
            {"name": "SecurityCam", "screenname": "cam"},
            {"name": "WebCam", "screenname": "webcam"},
            {"name": "Network", "screenname": "network_menu"},
            {"name": "Slideshow", "screenname": "slideshow"},
            {"name": "Breakout", "screenname": "breakout"},
            {"name": "System", "screenname": "system"}
        ]

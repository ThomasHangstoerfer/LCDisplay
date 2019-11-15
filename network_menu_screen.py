# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

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
    def __init__(self, screenManager):
        super(NetworkMenuScreen, self).__init__(screenManager)
        # print("MenuScreen.MenuScreen() ")
        self.screenManager = screenManager
        self.currentline = 0
        self.menu_headline_text = 'N E T W O R K'
        self.entries = [
            {"name": "Status", "screenname": "network_status"},
            {"name": "Wifi", "screenname": "network_wifi"}
        ]

# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import LCD_1in44
import LCD_Config
import RPi.GPIO as GPIO
import time
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

from themes import getTheme as getTheme
from themes import changeTheme as changeTheme
from keys import get_key_event, KEY_UP_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_RIGHT_PIN, KEY_PRESS_PIN, KEY1_PIN, KEY2_PIN, KEY3_PIN


class ScreenManager(object):

    def __init__(self, LCD, GPIO):
        self.LCD = LCD
        self.GPIO = GPIO
        self.take_screenshot = False
        self.screens = {}
        self.currentscreen = "menu"
        self.popup = None
        pass

    def addScreen(self, name, screen):
        self.screens[name] = screen

    def switchToScreen(self, screen):
        print('ScreenManager.switchToScreen(%s)' % screen)
        if screen in self.screens and self.screens[screen] is not None:
            self.screens[self.currentscreen].setVisible(False)
            self.currentscreen = screen
            self.screens[self.currentscreen].setVisible(True)
        else:
            print('ScreenManager.switchToScreen() invalid screen %s' % screen)

    def draw(self, image):
        if self.take_screenshot:
            image.save('screenshot.png')
            draw = ImageDraw.Draw(image)
            draw.text((15, 60), 'Screenshot saved', fill=getTheme()["headline_color"])

        if self.popup is not None:
            draw = ImageDraw.Draw(image)
            self.popup.draw(draw)

        self.LCD.LCD_ShowImage(image, 0, 0)

        if self.take_screenshot:
            time.sleep(2)
            self.take_screenshot = False

    def handle_key_event(self, input_pin):
        print("ScreenManager.handle_key_event: %s currentscreen: %s " % (input_pin, self.currentscreen))

        key_event = get_key_event(input_pin)
        if key_event == 'KEY1_RELEASED':
            self.switchToScreen('menu')
        else:
            if self.popup is not None:
                # TODO pass keyevent to popup
                pass
            else:
                self.screens[self.currentscreen].key(key_event)

        # self.screens[self.currentscreen].update()

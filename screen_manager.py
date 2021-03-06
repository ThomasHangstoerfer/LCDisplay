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
        self.screen_width = self.LCD.width
        self.screen_height = self.LCD.height
        self.GPIO = GPIO
        self.take_screenshot = False
        self.screens = {}
        self.currentscreen = "menu"
        self.popup = None
        pass

    def addScreen(self, name, screen, parent_screen='menu'):
        self.screens[name] = {'screen': screen, 'parent_screen': parent_screen}
        print(self.screens['menu']['parent_screen'])

    def switchToScreen(self, screen):
        print('ScreenManager.switchToScreen(%s)' % screen)
        if screen in self.screens and self.screens[screen]['screen'] is not None:
            self.screens[self.currentscreen]['screen'].setVisible(False)
            self.currentscreen = screen
            self.screens[self.currentscreen]['screen'].setVisible(True)
        else:
            print('ScreenManager.switchToScreen() invalid screen %s' % screen)

    def draw(self, image):
        if self.take_screenshot:
            image.save('screenshot.png')
            draw = ImageDraw.Draw(image)
            draw.text((15, 60), 'Screenshot saved', fill=getTheme()["headline_color"])

        if self.popup is not None:
            image = Image.eval(image, lambda x: x/3) # dim image below popup
            draw = ImageDraw.Draw(image)
            # draw.rectangle([(50, 50), (127, 127)], fill=(0, 0, 0, 100))

            self.popup.draw(draw)

        self.LCD.LCD_ShowImage(image, 0, 0)

        if self.take_screenshot:
            time.sleep(2)
            self.take_screenshot = False

    def update(self):
        self.screens[self.currentscreen]['screen'].update()

    def shutdown(self):
        self.screens[self.currentscreen]['screen'].setVisible(False)
        self.currentscreen = None

    def handle_key_event(self, input_pin):
        print("\n\n\nScreenManager.handle_key_event: %s currentscreen: %s " % (input_pin, self.currentscreen))

        key_event = get_key_event(input_pin)
        if key_event == '':
            print('ignored key_event')
            return
        if key_event == 'KEY1_RELEASED':
            self.switchToScreen('menu')
            self.popup = None
        else:
            if self.popup is not None:
                self.popup.key(key_event)
            else:
                handled = self.screens[self.currentscreen]['screen'].key(key_event)
                if not handled:
                    print('key was not handled by currentscreen')
                    if key_event == 'KEY2_RELEASED':
                        self.switchToScreen(self.screens[self.currentscreen]['parent_screen'])

        # self.screens[self.currentscreen].update()

    def addPopup(self, newpopup):
        newpopup.screen_manager = self
        self.popup = newpopup

    def clearPopup(self):
        self.popup = None

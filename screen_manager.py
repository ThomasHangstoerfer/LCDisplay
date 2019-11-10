# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import LCD_1in44
import LCD_Config
import RPi.GPIO as GPIO
from keys import KEY_UP_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_RIGHT_PIN, KEY_PRESS_PIN, KEY1_PIN, KEY2_PIN, KEY3_PIN

class ScreenManager(object):
    def __init__(self, LCD, GPIO):
        self.LCD = LCD
        self.GPIO = GPIO
        self.take_screenshot = False
        self.screens = {}
        self.currentscreen = "menu"
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

        self.LCD.LCD_ShowImage(image, 0, 0)

        if self.take_screenshot:
            time.sleep(2)
            self.take_screenshot = False

    def handle_key_event(self, input_pin):
        print("handle_key_event: %s currentscreen: %s " %( input_pin, self.currentscreen))

        if input_pin == KEY_UP_PIN:
            if GPIO.input(KEY_UP_PIN) == 0:
                self.screens[self.currentscreen].key('UP_PRESSED')
                print("Up pressed")
            else:
                self.screens[self.currentscreen].key('UP_RELEASED')
                print("Up released")
        if input_pin == KEY_DOWN_PIN:
            if GPIO.input(KEY_DOWN_PIN) == 0:
                self.screens[self.currentscreen].key('DOWN_PRESSED')
                print("Down pressed")
            else:
                self.screens[self.currentscreen].key('DOWN_RELEASED')
                print("Down released")
        if input_pin == KEY_LEFT_PIN:
            if GPIO.input(KEY_LEFT_PIN) == 0:
                self.screens[self.currentscreen].key('LEFT_PRESSED')
                print("Left pressed")
            else:
                self.screens[self.currentscreen].key('LEFT_RELEASED')
                print("Left released")
        if input_pin == KEY_RIGHT_PIN:
            if GPIO.input(KEY_RIGHT_PIN) == 0:
                self.screens[self.currentscreen].key('RIGHT_PRESSED')
                print("Right pressed")
            else:
                self.screens[self.currentscreen].key('RIGHT_RELEASED')
                print("Right released")
        if input_pin == KEY_PRESS_PIN:
            if GPIO.input(KEY_PRESS_PIN) == 0:
                self.screens[self.currentscreen].key('JOYSTICK_PRESSED')
                print("Joystick pressed")
            else:
                self.screens[self.currentscreen].key('JOYSTICK_RELEASED')
                print("Joystick released")
        if input_pin == KEY1_PIN:
            if GPIO.input(KEY1_PIN) == 0:
                print("Key1 pressed")
                self.screens[self.currentscreen].key('KEY1_PRESSED')
            else:
                print("Key1 released")
                self.screens[self.currentscreen].key('KEY1_RELEASED')
                self.switchToScreen("menu")

        if input_pin == KEY2_PIN:
            if GPIO.input(KEY2_PIN) == 0:
                print("Key2 pressed")
                self.screens[self.currentscreen].key('KEY2_PRESSED')
            else:
                print("Key2 released")
                self.screens[self.currentscreen].key('KEY2_RELEASED')

        if input_pin == KEY3_PIN:
            if GPIO.input(KEY3_PIN) == 0:
                print("Key3 pressed")
                self.screens[self.currentscreen].key('KEY3_PRESSED')
            else:
                print("Key3 released")
                self.screens[self.currentscreen].key('KEY3_RELEASED')

        # self.screens[self.currentscreen].update()

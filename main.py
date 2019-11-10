#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import LCD_1in44
import LCD_Config

from PIL import Image, ImageDraw, ImageFont, ImageColor
import RPi.GPIO as GPIO
import time
import utils
from screen import Screen
from themes import getTheme as getTheme
from menu_screen import MenuScreen
from main_menu_screen import MainMenuScreen
from slideshow_screen import SlideshowScreen
from cam_screen import CamScreen
from webcam_screen import WebcamScreen
from breakout_screen import BreakoutScreen
from system_screen import SystemScreen
from smarthome_screen import SmarthomeScreen
from network_menu_screen import NetworkMenuScreen
from network_status_screen import NetworkStatusScreen
from screen_manager import ScreenManager
from keys import KEY_UP_PIN, KEY_DOWN_PIN, KEY_LEFT_PIN, KEY_RIGHT_PIN, KEY_PRESS_PIN, KEY1_PIN, KEY2_PIN, KEY3_PIN

#init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up

LCD = LCD_1in44.LCD()
print("**********Init LCD**********")
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
LCD.LCD_Init(Lcd_ScanDir)
LCD.LCD_Clear()

screenManager = ScreenManager(LCD, GPIO)

screenManager.addScreen("menu", MainMenuScreen(LCD, screenManager))
screenManager.addScreen("smarthome", SmarthomeScreen(LCD, screenManager))
screenManager.addScreen("network_status", NetworkStatusScreen(LCD, screenManager))
screenManager.addScreen("slideshow", SlideshowScreen(LCD, screenManager))
screenManager.addScreen("cam", CamScreen(LCD, screenManager))
screenManager.addScreen("webcam", WebcamScreen(LCD, screenManager))
screenManager.addScreen("breakout", BreakoutScreen(LCD, screenManager))
screenManager.addScreen("system", SystemScreen(LCD, screenManager))
screenManager.addScreen("network_menu", NetworkMenuScreen(LCD, screenManager))

#screenManager.switchToScreen("menu")
screenManager.switchToScreen("system")


def handle_key_event(input_pin):
    global screenManager
    screenManager.handle_key_event(input_pin)


def main():

    # Caution: this runs in an other thread
    GPIO.add_event_detect(KEY_UP_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_DOWN_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_LEFT_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_RIGHT_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_PRESS_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY1_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY2_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY3_PIN, GPIO.BOTH, callback=handle_key_event)

    image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")
    draw = ImageDraw.Draw(image)
    # LCD_Config.Driver_Delay_ms(5000)
    # screens[currentscreen].update()

    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        utils.cpu_load.stop()
        screens[currentscreen].setVisible(False)
        image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")
        draw = ImageDraw.Draw(image)
        LCD.LCD_ShowImage(image,0,0)
        GPIO.cleanup()


if __name__ == '__main__':
    main()

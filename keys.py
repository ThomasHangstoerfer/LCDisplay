# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import RPi.GPIO as GPIO

KEY_UP_PIN = 6
KEY_DOWN_PIN = 19
KEY_LEFT_PIN = 5
KEY_RIGHT_PIN = 26
KEY_PRESS_PIN = 13
KEY1_PIN = 21
KEY2_PIN = 20
KEY3_PIN = 16


def get_key_event(input_pin):
    print("handle_key_event: %s" % (input_pin))

    key_event = ''
    if input_pin == KEY_UP_PIN:
        if GPIO.input(KEY_UP_PIN) == 0:
            key_event = 'UP_PRESSED'
            print("Up pressed")
        else:
            key_event = 'UP_RELEASED'
            print("Up released")
    if input_pin == KEY_DOWN_PIN:
        if GPIO.input(KEY_DOWN_PIN) == 0:
            key_event = 'DOWN_PRESSED'
            print("Down pressed")
        else:
            key_event = 'DOWN_RELEASED'
            print("Down released")
    if input_pin == KEY_LEFT_PIN:
        if GPIO.input(KEY_LEFT_PIN) == 0:
            key_event = 'LEFT_PRESSED'
            print("Left pressed")
        else:
            key_event = 'LEFT_RELEASED'
            print("Left released")
    if input_pin == KEY_RIGHT_PIN:
        if GPIO.input(KEY_RIGHT_PIN) == 0:
            key_event = 'RIGHT_PRESSED'
            print("Right pressed")
        else:
            key_event = 'RIGHT_RELEASED'
            print("Right released")
    if input_pin == KEY_PRESS_PIN:
        if GPIO.input(KEY_PRESS_PIN) == 0:
            key_event = 'JOYSTICK_PRESSED'
            print("Joystick pressed")
        else:
            key_event = 'JOYSTICK_RELEASED'
            print("Joystick released")
    if input_pin == KEY1_PIN:
        if GPIO.input(KEY1_PIN) == 0:
            print("Key1 pressed")
            key_event = 'KEY1_PRESSED'
        else:
            print("Key1 released")
            key_event = 'KEY1_RELEASED'
            self.switchToScreen("menu")

    if input_pin == KEY2_PIN:
        if GPIO.input(KEY2_PIN) == 0:
            print("Key2 pressed")
            key_event = 'KEY2_PRESSED'
        else:
            print("Key2 released")
            key_event = 'KEY2_RELEASED'

    if input_pin == KEY3_PIN:
        if GPIO.input(KEY3_PIN) == 0:
            print("Key3 pressed")
            key_event = 'KEY3_PRESSED'
        else:
            print("Key3 released")
            key_event = 'KEY3_RELEASED'

    return key_event

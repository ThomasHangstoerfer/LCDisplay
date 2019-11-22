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

RELEASED = 'RELEASED'
PRESSED = 'PRESSED'

key_state = {
    KEY_UP_PIN: RELEASED,
    KEY_DOWN_PIN: RELEASED,
    KEY_LEFT_PIN: RELEASED,
    KEY_RIGHT_PIN: RELEASED,
    KEY_PRESS_PIN: RELEASED,
    KEY1_PIN: RELEASED,
    KEY2_PIN: RELEASED,
    KEY3_PIN: RELEASED
}


def get_key_event(input_pin):
    print("keys.get_key_event() input_pin = %s" % (input_pin))
    print("GPIO.input(input_pin) = %s" % GPIO.input(input_pin))
    print("key_state[%s] = %s" % (input_pin, key_state[input_pin]))

    key_event = ''
    if input_pin == KEY_UP_PIN:
        if GPIO.input(KEY_UP_PIN) == 0 and key_state[KEY_UP_PIN] == RELEASED:
            key_state[KEY_UP_PIN] = PRESSED
            key_event = 'UP_PRESSED'
            print("Up pressed")
        else:
            if key_state[KEY_UP_PIN] == 'PRESSED':
                key_event = 'UP_RELEASED'
                print("Up released")
                key_state[KEY_UP_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY_UP_PIN] = 'RELEASED'

    if input_pin == KEY_DOWN_PIN:
        if GPIO.input(KEY_DOWN_PIN) == 0 and key_state[KEY_DOWN_PIN] == RELEASED:
            key_state[KEY_DOWN_PIN] = PRESSED
            key_event = 'DOWN_PRESSED'
            print("Down pressed")
        else:
            if key_state[KEY_DOWN_PIN] == 'PRESSED':
                key_event = 'DOWN_RELEASED'
                print("Down released")
                key_state[KEY_DOWN_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY_DOWN_PIN] = 'RELEASED'

    if input_pin == KEY_LEFT_PIN:
        if GPIO.input(KEY_LEFT_PIN) == 0 and key_state[KEY_LEFT_PIN] == RELEASED:
            key_state[KEY_LEFT_PIN] = PRESSED
            key_event = 'LEFT_PRESSED'
            print("Left pressed")
        else:
            if key_state[KEY_LEFT_PIN] == 'PRESSED':
                key_event = 'LEFT_RELEASED'
                print("Left released")
                key_state[KEY_LEFT_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY_LEFT_PIN] = 'RELEASED'

    if input_pin == KEY_RIGHT_PIN:
        if GPIO.input(KEY_RIGHT_PIN) == 0 and key_state[KEY_RIGHT_PIN] == RELEASED:
            key_state[KEY_RIGHT_PIN] = PRESSED
            key_event = 'RIGHT_PRESSED'
            print("Right pressed")
        else:
            if key_state[KEY_RIGHT_PIN] == 'PRESSED':
                key_event = 'RIGHT_RELEASED'
                print("Right released")
                key_state[KEY_RIGHT_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY_RIGHT_PIN] = 'RELEASED'

    if input_pin == KEY_PRESS_PIN:
        if GPIO.input(KEY_PRESS_PIN) == 0 and key_state[KEY_PRESS_PIN] == RELEASED:
            key_state[KEY_PRESS_PIN] = PRESSED
            key_event = 'JOYSTICK_PRESSED'
            print("Joystick pressed")
        else:
            if key_state[KEY_PRESS_PIN] == 'PRESSED':
                key_event = 'JOYSTICK_RELEASED'
                print("Joystick released")
                key_state[KEY_PRESS_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY_PRESS_PIN] = 'RELEASED'

    if input_pin == KEY1_PIN:
        if GPIO.input(KEY1_PIN) == 0 and key_state[KEY1_PIN] == RELEASED:
            key_state[KEY1_PIN] = PRESSED
            print("Key1 pressed")
            key_event = 'KEY1_PRESSED'
        else:
            if key_state[KEY1_PIN] == 'PRESSED':
                print("Key1 released")
                key_event = 'KEY1_RELEASED'
                key_state[KEY1_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY1_PIN] = 'RELEASED'


    if input_pin == KEY2_PIN:
        if GPIO.input(KEY2_PIN) == 0 and key_state[KEY2_PIN] == RELEASED:
            key_state[KEY2_PIN] = PRESSED
            print("Key2 pressed")
            key_event = 'KEY2_PRESSED'
        else:
            if key_state[KEY2_PIN] == 'PRESSED':
                print("Key2 released")
                key_event = 'KEY2_RELEASED'
                key_state[KEY2_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY2_PIN] = 'RELEASED'


    if input_pin == KEY3_PIN:
        if GPIO.input(KEY3_PIN) == 0 and key_state[KEY3_PIN] == RELEASED:
            key_state[KEY3_PIN] = PRESSED
            print("Key3 pressed")
            key_event = 'KEY3_PRESSED'
        else:
            if key_state[KEY3_PIN] == 'PRESSED':
                print("Key3 released")
                key_event = 'KEY3_RELEASED'
                key_state[KEY3_PIN] = 'RELEASED'
            else:
                print("Key event ignored. (ghost event?)")
                key_state[KEY3_PIN] = 'RELEASED'


    return key_event


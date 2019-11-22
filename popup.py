# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import math

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

from themes import getTheme as getTheme
from themes import changeTheme as changeTheme

class Popup(object):

    def __init__(self):
        self.screen_manager = None
        self.title = 'Popup'
        self.text = ''
        self.actionCallback = None
        self.actions = []
        self.active_action = 0
        pass

    def draw(self, drawO):
        # print('Popup.draw()')
        popup_width = 100
        popup_height = 80
        popup_x = (127-popup_width)/2
        popup_y = (127-popup_height)/2
        tab_height = 15
        drawO.rectangle([(popup_x, popup_y), (popup_x + popup_width, popup_y + popup_height)], fill=(0, 0, 0, 255), outline=(255, 255, 255, 255))
        text_x = popup_x + popup_width/2 - (len(self.text)*8)/2
        drawO.text((25, 60), self.text, fill=getTheme()["headline_color"])

        count = len(self.actions)
        width_per_i = math.floor(popup_width / count)

        for i in range(count):
            iname = self.actions[i]
            # print('iname: ', iname)
            
            # tab background
            drawO.rectangle([(i*width_per_i + popup_x + 1, popup_y + popup_height - tab_height), (popup_x + i*width_per_i+width_per_i-2, popup_y + popup_height - 1)], fill=(50, 50, 50, 128))

            # tab text
            text_x = popup_x + i*width_per_i + (width_per_i - len(str(iname))*8)/2
            drawO.text((text_x, popup_y + popup_height - 11),
                        str(iname),
                        fill=(getTheme()["highlight_text_color"] if i == self.active_action else getTheme()["text_color"]),
                        font=getTheme()["font"])

        # cursor-line over active tab
        drawO.line([(popup_x + self.active_action*width_per_i + 1, popup_y + popup_height - tab_height), (popup_x + self.active_action*width_per_i+width_per_i-2, popup_y + popup_height - tab_height)],
                    fill=getTheme()["cursor_color"])
        

    def key(self, event):
        # print("Popup.key(): %s" % event)
        action_count = len(self.actions)
        if event == "UP_RELEASED":
            #self.currentline = (self.currentline - 1) % entry_count
            pass
        if event == "DOWN_RELEASED":
            #self.currentline = (self.currentline + 1) % entry_count
            pass
        if event == "LEFT_RELEASED":
            self.active_action = (self.active_action - 1 ) % action_count
            self.screen_manager.update()
        if event == "RIGHT_RELEASED":
            self.active_action = (self.active_action + 1 ) % action_count
            self.screen_manager.update()
        if event == "JOYSTICK_RELEASED":
            """
            if self.entries[self.currentline]["screenname"] == "reboot":
                # TODO implement popup
                # self.screenManager.popup = Popup()
                utils.reboot()
            if self.entries[self.currentline]["screenname"] == "shutdown":
                utils.shutdown()
            """
            if self.actionCallback is not None:
                print('trigger callback')
                self.actionCallback(self.actions[self.active_action])
            else:
                print('dont trigger callback')

            pass
        if event == "KEY2_RELEASED":
            print('BACK')
            self.screen_manager.clearPopup()
            #self.screenManager.take_screenshot = True
            pass
        if event == "KEY3_RELEASED":
            #print('self.take_screenshot = True')
            #self.screenManager.take_screenshot = True
            pass
        print('self.active_action = %i' % self.active_action )

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


class MenuScreen(Screen):
    def __init__(self, screenManager):
        super(MenuScreen, self).__init__()
        # print("MenuScreen.MenuScreen() ")
        self.screenManager = screenManager
        self.menu_headline_text = 'M E N U'
        self.show_clock = False
        self.currentline = 0

    def setVisible(self, visible):
        # print("MenuScreen.setVisible(%s)" % visible)
        if visible and not self.isVisible():
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if not visible and self.isVisible():
            self.t.cancel()
        super(MenuScreen, self).setVisible(visible)

    def updateTimeout(self):
        # print("MenuScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def update(self):
        # print("MenuScreen.update() %s" % self.isVisible())
        if not self.isVisible():
            return
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        # draw.rectangle([(1,1),(127,10)],fill = "RED")

        text_x = (self.screenManager.screen_width/2) - (len(self.menu_headline_text)*8)/2  # center headline text
        draw.text((text_x, 1), self.menu_headline_text, fill=getTheme()["headline_color"], font=getTheme()["headlinefont"])
        draw.line([(0, 18), (127, 18)], fill="BLACK", width=1)

        y_offset = 24
        for i in range(len(self.entries)):
            if self.entries[i]["name"] != "":
                o = 0
                if self.currentline == i:
                    o = o + 5
                draw.text((1 + o, y_offset), self.entries[i]["name"], fill=(
                    getTheme()["highlight_text_color"] if (self.currentline == i) else getTheme()["text_color"]),
                          font=getTheme()["font"])
                if self.currentline == i:
                    draw.line([(0, y_offset), (127, y_offset)], fill=getTheme()["cursor_color"], width=1)
                    draw.line([(0, y_offset + 10), (127, y_offset + 10)], fill=getTheme()["cursor_color"],
                              width=1)

            y_offset += 12

        if self.show_clock:
            draw.text((40, 110), datetime.datetime.now().strftime('%H:%M:%S'), fill=getTheme()["highlight_text_color"],
                      font=getTheme()["clockfont"])

        self.screenManager.draw(image)

    def key(self, event):
        # print("MenuScreen.key(): %s" % event)
        entry_count = len(self.entries)
        if event == "UP_RELEASED":
            self.currentline = (self.currentline - 1) % entry_count
        if event == "DOWN_RELEASED":
            self.currentline = (self.currentline + 1) % entry_count
        if event == "LEFT_RELEASED":
            # self.currentline = (self.currentline - 1 ) % entry_count
            changeTheme("blue")
        if event == "RIGHT_RELEASED":
            # self.currentline = (self.currentline + 1 ) % entry_count
            changeTheme("red")
        if event == "JOYSTICK_RELEASED":
            # print('MenuScreen.key(): ' + self.entries[self.currentline]["screenname"] )
            if self.entries[self.currentline]["screenname"] != "":
                self.screenManager.switchToScreen(self.entries[self.currentline]["screenname"])
        if event == "KEY3_RELEASED":
            # print('self.take_screenshot = True')
            self.screenManager.take_screenshot = True
        self.update()

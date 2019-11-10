# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import LCD_1in44
import LCD_Config
import datetime
import time
import cv2
import sys
import array as arr
from random import randrange

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

from screen import Screen
from threading import Timer
from themes import getTheme as getTheme
from themes import changeTheme as changeTheme
import utils



class SystemScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(SystemScreen, self).__init__()
        # print("SystemScreen.SystemScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentline = 0
        self.dynamic_y_axis = False
        self.take_screenshot = False
        self.entries = [
            {"name": "Reboot", "screenname": "reboot"},
            {"name": "Shutdown", "screenname": "shutdown"}
        ]

    def setVisible(self, visible):
        print("SystemScreen.setVisible(%s)" % visible)
        if visible and not self.isVisible():
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if not visible and self.isVisible():
            self.t.cancel()
        super(SystemScreen, self).setVisible(visible)

    def updateTimeout(self):
        # print("SystemScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def drawGraph(self, draw):
        graph_height = 65
        graph_top_y = 35
        draw.rectangle([(1, graph_top_y), (127, graph_top_y + graph_height)], fill=(50, 50, 50, 255))
        # last value is displayed on the right -> add new values at the end of the list
        # load = [0.5, 0.7, 0.3, 0.2, 0.5, 0.2, 0.8, 1.1, 1.0, 1.4, 1.8, 2.0, 0.9, 0.8]
        # load = [0.5, 0.25, 1.0]
        load = utils.cpu_load.history
        if len(load) <= 0:
            return
        cur_x = 115
        bar_width = 10
        if self.dynamic_y_axis:
            factor = graph_height / max(load)
        else:
            factor = 1.0
        print('factor ', factor)
        for i in reversed(range(len(load))):
            draw.rectangle([(cur_x, max(graph_top_y, graph_top_y+graph_height-(load[i]*factor))), (cur_x+bar_width, graph_top_y+graph_height)], fill=(150, 150, 250, 255))
            cur_x -= bar_width
            if cur_x < 0:
                break

    def update(self):
        # print("SystemScreen.update() %s" % self.isVisible())
        if not self.isVisible():
            return
        # self.LCD.LCD_Clear()
        # image = Image.new("RGB", (self.LCD.width, self.LCD.height), "WHITE")
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        # draw.rectangle([(1,1),(127,10)],fill = "RED")

        draw.text((15, 1), 'S Y S T E M', fill=getTheme()["headline_color"], font=getTheme()["headlinefont"])
        draw.line([(0, 18), (127, 18)], fill=getTheme()["headline_color"], width=1)

        draw.text((1, 24), "CPU:", fill=(getTheme()["text_color"]), font=getTheme()["font"])
        draw.text((30, 24), utils.get_cpu_temp(), fill=(getTheme()["highlight_text_color"]), font=getTheme()["font"])
        draw.text((65, 24), "Up:", fill=(getTheme()["text_color"]), font=getTheme()["font"])
        draw.text((90, 24), utils.get_uptime(), fill=(getTheme()["highlight_text_color"]), font=getTheme()["font"])

        self.drawGraph(draw)

        y_offset = 104
        for i in range(len(self.entries)):
            if self.entries[i]["name"] != "":
                o = 0
                if self.currentline == i:
                    o = o + 5
                draw.text((1 + o, y_offset), self.entries[i]["name"], fill=(
                    getTheme()["highlight_text_color"] if (self.currentline == i) else getTheme()["text_color"]),
                          font=getTheme()["font"])
                if self.currentline == i:
                    draw.line([(0, y_offset), (127, y_offset)], fill=getTheme()["highlight_text_color"], width=1)
                    draw.line([(0, y_offset + 10), (127, y_offset + 10)], fill=getTheme()["highlight_text_color"],
                              width=1)

            y_offset += 12

        # draw.text((40, 110), datetime.datetime.now().strftime('%H:%M:%S'), fill=getTheme()["highlight_text_color"],
        #           font=getTheme()["clockfont"])

        if self.take_screenshot:
            image.save('screenshot.png')
            draw.text((15, 60), 'Screenshot saved', fill=getTheme()["headline_color"])

        self.LCD.LCD_ShowImage(image, 0, 0)

        if self.take_screenshot:
            time.sleep(2)
            self.take_screenshot = False

    def key(self, event):
        global screenManager
        print("SystemScreen.key(): %s" % event)
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
            if self.entries[self.currentline]["screenname"] == "reboot":
                utils.reboot()
            if self.entries[self.currentline]["screenname"] == "shutdown":
                utils.shutdown()
        if event == "KEY3_RELEASED":
            print('self.take_screenshot = True')
            self.take_screenshot = True
        self.update()

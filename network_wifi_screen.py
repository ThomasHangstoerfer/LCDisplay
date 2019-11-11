# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import LCD_1in44
import LCD_Config
import datetime
import time
import netifaces
import math

from PIL import Image,ImageDraw,ImageFont,ImageColor
from themes import getTheme as getTheme
from themes import changeTheme as changeTheme

from screen import Screen
from threading import Timer
import utils


class NetworkWifiScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(NetworkWifiScreen, self).__init__()
        #print("NetworkWifiScreen.NetworkStatusScreen() ")
        self.screenManager = screenManager
        self.currentline = 0
        self.bitrate = 0
        self.bitrate_unit = ""
        self.quality = 0
        self.essid = ""
        self.selected_interface = 0


    def setVisible(self, visible):
        print("NetworkWifiScreen.setVisible(%s)" % visible)
        if (visible and not self.isVisible() ):
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if (not visible and self.isVisible() ):
            self.t.cancel()
        super(NetworkWifiScreen, self).setVisible(visible)

    def updateTimeout(self):
        #print("NetworkWifiScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def update(self):
        #print("NetworkWifiScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return

        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        #draw.rectangle([(1,1),(127,10)],fill = "RED")

        # print('Network-interfaces: ', netifaces.interfaces() )

        try:
            self.bitrate, self.bitrate_unit, self.quality, self.essid = utils.get_network_info('wlan0')

            #print('WifiState update output: ' + output + ' raw: ', raw, ' quality: ', quality)
            #if ( self.quality < 20 ):
            #    self.source = 'gfx/wifi1.png'
            #elif ( self.quality < 40 ):
            #    self.source = 'gfx/wifi2.png'
            #elif ( self.quality < 80 ):
            #    self.source = 'gfx/wifi3.png'
            #else:
            #    self.source = 'gfx/wifi4.png'
        except Exception as e:
            #self.source = 'gfx/wifi0.png'
            print('WifiState.update(): ', e)

        draw.text((5, 1), 'N E T W O R K', fill=getTheme()["headline_color"], font=getTheme()["headlinefont"])
        draw.line([(0,18),(127,18)], fill="BLACK", width=1)
        draw.text((1, 24), self.essid, fill=getTheme()["highlight_text_color"], font=getTheme()["headlinefont"])
        draw.text((1, 42), 'Quality: ' + str(self.quality) + '% ' + str(self.bitrate) + "" + self.bitrate_unit, fill=("BLACK" if (self.currentline==0) else "BLUE"))
        draw.text((1, 54), 'IP: ' + utils.get_ip_address(), fill=("BLACK" if (self.currentline==0) else "BLUE"))
        # draw.text((1, 66), 'CPU: ' + utils.get_cpu_temp(), fill=("BLACK" if (self.currentline==0) else "BLUE"))
        draw.text((1, 78), 'Hostname: ' + utils.get_hostname(), fill=("BLACK" if (self.currentline==0) else "BLUE"))
        # draw.text((1, 78), 'Make: ' + utils.get_make_running(), fill = "WHITE")

        self.screenManager.draw(image)

    def key(self, event):
        print("NetworkStatusScreen.key(): %s" % event)
        icount = len(netifaces.interfaces())
        if ( event == "UP_RELEASED" ):
            self.currentline = (self.currentline - 1 ) % 1
        if ( event == "DOWN_RELEASED" ):
            self.currentline = (self.currentline + 1 ) % 1
        if ( event == "LEFT_RELEASED" ):
            self.selected_interface = (self.selected_interface - 1 ) % icount
        if ( event == "RIGHT_RELEASED" ):
            self.selected_interface = (self.selected_interface + 1 ) % icount
        if ( event == "JOYSTICK_RELEASED" ):
            # self.screenManager.switchToScreen("menu")
            pass
        if event == "KEY3_RELEASED":
            print('self.screenManager.take_screenshot = True')
            self.screenManager.take_screenshot = True
        self.update()


# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

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


class NetworkStatusScreen(Screen):
    def __init__(self, screenManager):
        super(NetworkStatusScreen, self).__init__()
        #print("NetworkStatusScreen.NetworkStatusScreen() ")
        self.screenManager = screenManager
        self.currentline = 0
        self.bitrate = 0
        self.bitrate_unit = ""
        self.quality = 0
        self.essid = ""
        self.selected_interface = 0


    def setVisible(self, visible):
        print("NetworkStatusScreen.setVisible(%s)" % visible)
        if (visible and not self.isVisible() ):
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if (not visible and self.isVisible() ):
            self.t.cancel()
        super(NetworkStatusScreen, self).setVisible(visible)

    def updateTimeout(self):
        #print("NetworkStatusScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def update(self):
        #print("NetworkStatusScreen.update() %s" % self.isVisible())
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
        draw.text((1, 30 ), 'Hostname:  ' + utils.get_hostname(), fill="BLACK")
        count = len(netifaces.interfaces())
        width_per_i = math.floor(self.screenManager.screen_width / count)
        print('count: %i' % count)
        print('width_per_i: ' + str(width_per_i))
        print('selected_interface: ' + str(self.selected_interface))
        try:
            print('interfaces: ', netifaces.interfaces())
            addresses = netifaces.ifaddresses(netifaces.interfaces()[self.selected_interface])
            print('addresses', addresses)
            if netifaces.AF_INET in addresses:
                ip4addresses = addresses[netifaces.AF_INET]
                for a in range(len(ip4addresses)):
                    print('ifaddresses: ', ip4addresses[a]['addr'])
                    draw.text((1, 42 + a * 10), 'IPv4: ' + ip4addresses[a]['addr'], fill="BLACK")
            else:
                print('no netifaces.AF_INET in addresses')
                draw.text((1, 42 ), 'No IPv4 addresses ', fill="BLACK")
                draw.text((1, 52 ), 'assigned ', fill="BLACK")

            for i in range(count):
                iname = netifaces.interfaces()[i]
                # print('iname: ', iname)
                
                # tab background
                draw.rectangle([(i*width_per_i, 110), (i*width_per_i+width_per_i-2, 127)], fill=(50, 50, 50, 128))

                # tab text
                draw.text((i*width_per_i, 114),
                            str(iname),
                            fill=(getTheme()["highlight_text_color"] if i == self.selected_interface else getTheme()["text_color"]),
                            font=getTheme()["font"])

            # cursor-line over active tab
            draw.line([(self.selected_interface*width_per_i, 110), (self.selected_interface*width_per_i+width_per_i-2, 110)],
                        fill=getTheme()["cursor_color"])
        except:
            print('Exception in NetworkStatusScreen.update()')

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


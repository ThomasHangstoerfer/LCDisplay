# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import LCD_1in44
import LCD_Config
import datetime
import netifaces
import math

from PIL import Image,ImageDraw,ImageFont,ImageColor
from themes import getTheme as getTheme
from themes import changeTheme as changeTheme

from screen import Screen
from threading import Timer
import utils


# duration is in seconds
# wait for time completion
#t.join()

class NetworkScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(NetworkScreen, self).__init__()
        #print("NetworkScreen.NetworkScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentline = 0
        self.bitrate = 0
        self.bitrate_unit = ""
        self.quality = 0
        self.essid = ""
        self.big_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 15)
        self.subscreen = 1
        self.selected_interface = 0


    def setVisible(self, visible):
        print("NetworkScreen.setVisible(%s)" % visible)
        if (visible and not self.isVisible() ):
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if (not visible and self.isVisible() ):
            self.t.cancel()
        super(NetworkScreen, self).setVisible(visible)

    def updateTimeout(self):
        #print("NetworkScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def update(self):
        #print("NetworkScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return
        #image = Image.new("RGB", (self.LCD.width, self.LCD.height), "WHITE")
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        #draw.rectangle([(1,1),(127,10)],fill = "RED")

        print('Network-interfaces: ', netifaces.interfaces() )

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



        draw.text((5, 1), 'N E T W O R K', fill = getTheme()["headline_color"], font = getTheme()["headlinefont"])
        draw.line([(0,18),(127,18)], fill = getTheme()["headline_color"], width = 3)
        if self.subscreen == 0:
            draw.text((1, 24), self.essid, fill = getTheme()["highlight_text_color"], font = self.big_font)
            draw.text((1, 42), 'Quality: ' + str(self.quality) + '% ' + str(self.bitrate) + "" + self.bitrate_unit, fill = ("BLACK" if (self.currentline==0) else "BLUE"))
            draw.text((1, 54), 'IP: ' + utils.get_ip_address(), fill = ("BLACK" if (self.currentline==0) else "BLUE"))
            draw.text((1, 66), 'CPU: ' + utils.get_cpu_temp(), fill = ("BLACK" if (self.currentline==0) else "BLUE"))
            # draw.text((1, 78), 'Make: ' + utils.get_make_running(), fill = "WHITE")
        elif self.subscreen == 1:
            count = len(netifaces.interfaces())
            width_per_i = math.floor(127 / count)
            print('width_per_i: ' + str(width_per_i))
            print('selected_interface: ' + str(self.selected_interface))
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
                
                draw.rectangle([(i*width_per_i, 110), (i*width_per_i+width_per_i-2, 127)], fill=(50, 50, 50, 128))
                draw.text((i*width_per_i, 114), str(iname), fill=getTheme()["text_color"], font=getTheme()["font"])
            draw.line([(self.selected_interface*width_per_i, 110), (self.selected_interface*width_per_i+width_per_i-2, 110)], fill=getTheme()["highlight_text_color"])

                                                              


        #draw.text((80, 118), datetime.datetime.now().strftime('%H:%M:%S'), fill = getTheme()["headline_color"])

        self.LCD.LCD_ShowImage(image,0,0)

    def key(self, event):
        global screenManager
        print("NetworkScreen.key(): %s" % event)
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
            self.screenManager.switchToScreen("menu")
        self.update()


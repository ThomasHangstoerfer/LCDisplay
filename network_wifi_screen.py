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
from popup import Popup

from screen import Screen
from threading import Timer
import utils


class NetworkWifiScreen(Screen):

    def __init__(self, screenManager):
        super(NetworkWifiScreen, self).__init__()
        #print("NetworkWifiScreen.NetworkWifiScreen() ")
        self.screenManager = screenManager
        self.currentline = 0
        self.bitrate = 0
        self.bitrate_unit = ""
        self.quality = 0
        self.essid = ""
        self.selected_item = 0
        self.menu_items = ['Mode', 'Test']

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

        menu_headline_text = 'W I F I'
        text_x = (self.screenManager.screen_width/2) - (len(menu_headline_text)*8)/2  # center headline text
        draw.text((text_x, 1), menu_headline_text, fill=getTheme()["headline_color"], font=getTheme()["headlinefont"])
        draw.line([(0,18),(127,18)], fill="BLACK", width=1)
        mode_text = 'Access Point' if utils.get_wifi_mode() == 'ap' else 'Wifi-Client' if utils.get_wifi_mode() == 'client' else 'unknown'
        draw.text((1, 24), 'Mode   : ' + mode_text, fill=getTheme()["highlight_text_color"])

        if utils.get_wifi_mode() == 'ap':
            draw.text((1, 34), 'SSID   : ' + utils.get_ap_ssid(), fill=getTheme()["highlight_text_color"])
            draw.text((1, 44), 'Pwd    : ' + utils.get_ap_password(), fill=getTheme()["highlight_text_color"])
            draw.text((1, 54), 'Clients: 0', fill=getTheme()["highlight_text_color"])

        else:
            draw.text((1, 34), 'SSID:  : ' + self.essid, fill=getTheme()["highlight_text_color"])
            draw.text((1, 44), 'Quality: ' + str(self.quality) + '% ' + str(self.bitrate) + "" + self.bitrate_unit, fill=getTheme()["highlight_text_color"])
            draw.text((1, 54), 'IP: ' + utils.get_ip_address(), fill=getTheme()["highlight_text_color"])

        count = len(self.menu_items)
        width_per_i = math.floor(self.screenManager.screen_width / count)
        
        for i in range(count):
            iname = self.menu_items[i]
            # print('iname: ', iname)
            
            # tab background
            draw.rectangle([(i*width_per_i, 110), (i*width_per_i+width_per_i-2, 127)], fill=(50, 50, 50, 128))

            # tab text
            draw.text((i*width_per_i, 114),
                        str(iname),
                        fill=(getTheme()["highlight_text_color"] if i == self.selected_item else getTheme()["text_color"]),
                        font=getTheme()["font"])

        # cursor-line over active tab
        draw.line([(self.selected_item*width_per_i, 110), (self.selected_item*width_per_i+width_per_i-2, 110)],
                    fill=getTheme()["cursor_color"])

        self.screenManager.draw(image)

    def popupAction(self, action):
        print("NetworkWifiScreen.popupAction(%s)" % action)
        self.screenManager.popup = None
        # self.screenManager.popup.text = 'Switching mode'
        utils.switch_wifi_mode(action.lower())

    def key(self, event):
            print("NetworkWifiScreen.key(): %s" % event)
            icount = len(self.menu_items)
            handled = False
            if ( event == "UP_RELEASED" ):
                self.currentline = (self.currentline - 1 ) % 1
                handled = True
            if ( event == "DOWN_RELEASED" ):
                self.currentline = (self.currentline + 1 ) % 1
                handled = True
            if ( event == "LEFT_RELEASED" ):
                self.selected_item = (self.selected_item - 1 ) % icount
                handled = True
            if ( event == "RIGHT_RELEASED" ):
                self.selected_item = (self.selected_item + 1 ) % icount
                handled = True
            if ( event == "JOYSTICK_RELEASED" ):
                # self.screenManager.switchToScreen("menu")
                print('Create popup')
                popup = Popup()
                popup.text = 'Switch mode?'
                popup.actions = ['AP', 'Client']
                popup.actionCallback = self.popupAction
                self.screenManager.addPopup(popup)
                handled = True

                pass
            if event == "KEY3_RELEASED":
                print('self.screenManager.take_screenshot = True')
                self.screenManager.take_screenshot = True
                handled = True
            self.update()
            return handled


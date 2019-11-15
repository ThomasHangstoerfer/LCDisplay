# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import datetime
import time
import cv2

from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageOps

from screen import Screen
from threading import Timer


# duration is in seconds
# wait for time completion
#t.join()

class SlideshowScreen(Screen):
    def __init__(self, screenManager):
        super(SlideshowScreen, self).__init__()
        #print("SlideshowScreen.SlideshowScreen() ")
        self.screenManager = screenManager
        self.currentimage = 0
        self.images = ["assets/murch.bmp", "assets/time.bmp", "assets/sky.bmp", "assets/am.bmp"]

    def update(self):
        #print("SlideshowScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return

        image = Image.open(self.images[self.currentimage])
        self.screenManager.draw(image)

    def key(self, event):
        print("SlideshowScreen.key(): %s" % event)
        if ( event == "UP_RELEASED" ):
            self.currentimage = (self.currentimage - 1 ) % len(self.images)
        if ( event == "DOWN_RELEASED" ):
            self.currentimage = (self.currentimage + 1 ) % len(self.images)
        if ( event == "LEFT_RELEASED" ):
            self.currentimage = (self.currentimage - 1 ) % len(self.images)
        if ( event == "RIGHT_RELEASED" ):
            self.currentimage = (self.currentimage + 1 ) % len(self.images)
        if ( event == "JOYSTICK_RELEASED" ):
            self.screenManager.switchToScreen("menu")
        self.update()


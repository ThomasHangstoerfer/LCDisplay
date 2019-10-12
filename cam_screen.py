import LCD_1in44
import LCD_Config
import datetime

from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageOps

from screen import Screen
from threading import Timer
import os, sys
import utils
from os import listdir

# duration is in seconds
# wait for time completion
#t.join()

class CamScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(CamScreen, self).__init__()
        #print("CamScreen.CamScreen() ")
        self.LCD = LCD
        self.isPlaying = False
        self.screenManager = screenManager
        self.currentimage = -1
        #self.images = ["murch.bmp", "time.bmp", "sky.bmp", "cam.bmp"]
        self.timer = utils.RepeatedTimer(0.5, self.key, "LEFT_RELEASED") # it auto-starts, no need of rt.start()
        self.timer.stop()

    def setVisible(self, visible):
        print("CamScreen.setVisible(%s)" % visible)
        if (visible and not self.isVisible() ):
            #self.timer.start()
            #self.update()
            pass
        if (not visible and self.isVisible() ):
            self.isPlaying = False
            self.timer.stop()
            pass
        super(CamScreen, self).setVisible(visible)



    def update(self):
        print("1CamScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return
        #image = Image.open(self.images[self.currentimage])

        path = "/qnap/Download/today/"
        if not os.path.isdir(path):
            path = "assets/cam/"

        loadedImages = []
        try:
            imagesList = listdir(path)
            for image in imagesList:
                #img = PImage.open(path + image)
                loadedImages.append(image)
            loadedImages.sort()
        except:
            pass
        if len(loadedImages) <= 0:
            image = Image.new("RGB", (self.LCD.width, self.LCD.height), "BLACK")
            draw = ImageDraw.Draw(image)
            draw.text((35, 40), 'NO IMAGES', fill = "BLUE")
            self.LCD.LCD_ShowImage(image, 0, 0)
            return

        if self.currentimage == -1 or self.currentimage >= len(loadedImages):
            self.currentimage = len(loadedImages)-1

        print('Loading ' + path + loadedImages[self.currentimage])
        image = Image.open(path + loadedImages[self.currentimage])
        size = 128, 128
        #image.thumbnail(size, Image.ANTIALIAS)
        #image.resize(size)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        draw = ImageDraw.Draw(image)
        draw.rectangle([(0,116),(127,127)],fill = "BLACK")
        draw.text((0, 118), loadedImages[self.currentimage], fill = "BLUE")

        self.LCD.LCD_ShowImage(image,0,0)

    def key(self, event):
        print("CamScreen.key(): %s" % event)
        if ( event == "UP_RELEASED" ):
            self.currentimage = (self.currentimage - 1 )
        if ( event == "DOWN_RELEASED" ):
            self.currentimage = (self.currentimage + 1 )
        if ( event == "LEFT_RELEASED" ):
            self.currentimage = (self.currentimage - 1 )
        if ( event == "RIGHT_RELEASED" ):
            self.currentimage = (self.currentimage + 1 )
        if (event == "KEY2_RELEASED"):
            if self.isPlaying:
                self.timer.stop()
            else:
                self.timer.start()
            self.isPlaying = not self.isPlaying
        if (event == "KEY3_RELEASED"):
            self.currentimage = -1
        if ( event == "JOYSTICK_RELEASED" ):
            self.screenManager.switchToScreen("menu")
        self.update()


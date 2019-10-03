import LCD_1in44
import LCD_Config
import datetime

from PIL import Image,ImageDraw,ImageFont,ImageColor

from screen import Screen
from threading import Timer


# duration is in seconds
# wait for time completion
#t.join()

class SlideshowScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(SlideshowScreen, self).__init__()
        print("SlideshowScreen.SlideshowScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentimage = 0
        self.images = ["murch.bmp", "time.bmp", "sky.bmp", "cam.bmp"]

    def update(self):
        print("SlideshowScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return
        image = Image.open(self.images[self.currentimage])
        self.LCD.LCD_ShowImage(image,0,0)

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


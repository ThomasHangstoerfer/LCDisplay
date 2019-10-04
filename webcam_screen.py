import LCD_1in44
import LCD_Config
import datetime
import time
import cv2

from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageOps

from screen import Screen
from threading import Timer
from themes import getTheme as getTheme


# duration is in seconds
# wait for time completion
#t.join()

class WebcamScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(WebcamScreen, self).__init__()
        #print("WebcamScreen.WebcamScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentimage = 0
        self.camera = None

    def setVisible(self, visible):
        print("WebcamScreen.setVisible(%s)" % visible)
        if (visible and not self.isVisible() ):
            self.showInitScreen()
            self.t = Timer(5, self.updateTimeout)
            self.t.start()
            self.update()
            #camera_port = 0
            #self.camera = cv2.VideoCapture(camera_port)
            #time.sleep(0.1)  # If you don't wait, the image will be dark
        if (not visible and self.isVisible() ):
            self.t.cancel()
            #del (self.camera)
        super(WebcamScreen, self).setVisible(visible)

    def updateTimeout(self):
        #print("WebcamScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(5, self.updateTimeout)
        self.t.start()
        self.update()

    def showInitScreen(self):
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        draw.text((7, 114), "Initializing camera", fill=getTheme()["headline_color"])
        self.LCD.LCD_ShowImage(image, 0, 0)

    def showErrorScreen(self):
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        draw.text((10, 114), "No camera detected", fill=getTheme()["headline_color"])
        self.LCD.LCD_ShowImage(image, 0, 0)

    def update(self):
        print("WebcamScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return

        camera_port = 0

        try:
            self.camera = cv2.VideoCapture(camera_port)
            time.sleep(0.1)  # If you don't wait, the image will be dark
        except:
            self.showErrorScreen()

        if self.camera is None:
            print("camera is not available")
            self.showErrorScreen()
            return

        try:
            return_value, cv2_im = self.camera.read()
            del (self.camera)
            cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im)
            size = 128, 128
            image = ImageOps.fit(pil_im, size, Image.ANTIALIAS)

            self.LCD.LCD_ShowImage(image,0,0)
        except:
            self.showErrorScreen()

    def key(self, event):
        print("WebcamScreen.key(): %s" % event)
        if ( event == "JOYSTICK_RELEASED" ):
            self.screenManager.switchToScreen("menu")
        self.update()


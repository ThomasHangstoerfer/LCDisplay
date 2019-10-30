import LCD_1in44
import LCD_Config
import datetime
import time
import cv2

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

from screen import Screen
from threading import Timer
from themes import getTheme as getTheme


# duration is in seconds
# wait for time completion
# t.join()

class WebcamScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(WebcamScreen, self).__init__()
        # print("WebcamScreen.WebcamScreen() ")
        self.imagepath = '/home/pi/'
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentimage = 0
        self.camera = None
        self.camTimer = None
        self.screenTimer = None
        self.updateCamTime = 5
        self.updateScreenTime = 1
        self.isRecording = False
        self.recordingIconVisible = False
        self.camimage = None
        self.menuselection = 0
        self.running = True
        self.lastRecordingStatus = 0

    def stop(self):
        print("STOP")
        self.running = False

        self.camTimer.cancel()
        del self.camTimer
        self.screenTimer.cancel()
        del self.screenTimer

    def setVisible(self, visible):
        print("WebcamScreen.setVisible(%s)" % visible)

        if visible and not self.isVisible():
            self.running = True
            self.showInitScreen()
            self.camTimer = Timer(self.updateCamTime, self.updateCamTimeout)
            self.camTimer.start()
            self.screenTimer = Timer(self.updateScreenTime, self.updateScreenTimeout)
            self.screenTimer.start()
            # camera_port = 0
            # self.camera = cv2.VideoCapture(camera_port)
            # time.sleep(0.1)  # If you don't wait, the image will be dark
        if not visible and self.isVisible():
            self.stop()

        super(WebcamScreen, self).setVisible(visible)

        if visible and self.isVisible():
            self.updateCam()
            self.update()



    def restartCamTimer(self):
        self.camTimer.cancel()
        self.camTimer = Timer(self.updateCamTime, self.updateCamTimeout)
        self.camTimer.start()

    def updateCamTimeout(self):
        print("WebcamScreen.updateCamTimeout() %s" % self.isVisible())
        if not self.running:
            return
        self.restartCamTimer()
        self.updateCam()
        self.update()

    def updateScreenTimeout(self):
        print("WebcamScreen.updateScreenTimeout() %s" % self.isVisible())
        if not self.running:
            return
        self.screenTimer.cancel()
        self.screenTimer = Timer(self.updateScreenTime, self.updateScreenTimeout)
        self.screenTimer.start()
        self.update()

    def showInitScreen(self):
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        draw.text((7, 94), "Initializing camera", fill=getTheme()["headline_color"])
        self.LCD.LCD_ShowImage(image, 0, 0)
        self.camimage = image

    def showErrorScreen(self):
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        draw.text((10, 94), "No camera detected", fill=getTheme()["headline_color"])
        # self.LCD.LCD_ShowImage(image, 0, 0)
        self.camimage = image

    def updateCam(self):
        print("WebcamScreen.updateCam() %s" % self.isVisible())
        if not self.running:
            return

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
            del self.camera
            cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(cv2_im)
            if self.isRecording:
                pil_im.save(self.imagepath + datetime.datetime.now().strftime('%H_%M_%S') + '_image.png')
            size = 128, 128
            self.camimage = ImageOps.fit(pil_im, size, Image.ANTIALIAS)

        except:
            self.showErrorScreen()

    def update(self):
        print("WebcamScreen.update() %s" % self.isVisible())
        if not self.isVisible():
            return

        # work on a copy of the cam image
        if self.camimage is not None:
            drawimage = self.camimage.copy()
        else:
            drawimage = getTheme()["background_image"].copy()

        draw = ImageDraw.Draw(drawimage, 'RGBA')

        self.drawRecordingStatus(draw)

        timertext = '' + str(self.updateCamTime) + 's'
        draw.rectangle([(2, 110), (30, 127)], fill=(50, 50, 50, 128))
        if self.menuselection == 0:
            draw.line([(2, 110), (30, 110)], fill=getTheme()["highlight_text_color"])
        draw.text((30-(len(timertext)*7), 114), timertext, fill=getTheme()["text_color"], font=getTheme()["font"])

        self.LCD.LCD_ShowImage(drawimage, 0, 0)
        del drawimage


    def drawRecordingStatus(self, draw):

        r = 5
        x = 118
        y = 118

        draw.rectangle([(x-10, 110), (x+10, 127)], fill=(50, 50, 50, 128))
        if self.menuselection == 1:
            draw.line([(x-10, 110), (x+10, 110)], fill=getTheme()["highlight_text_color"])
        if self.isRecording:
            # draw.rectangle([(1,1),(127,10)],fill = "RED")
            # draw.polygon([(50, 0), (100, 100), (0, 100)], (255, 0, 0, 125))
            # draw.polygon([(50, 100), (100, 0), (0, 0)], (0, 255, 0, 125))
            if self.recordingIconVisible:
                draw.ellipse((x - r, y - r + 2, x + r, y + r + 2), outline=(255, 0, 0, 255))
            else:
                draw.ellipse((x - r, y - r + 2, x + r, y + r + 2), fill=(255, 0, 0, 255))
        else:
            draw.ellipse((x - r, y - r + 2, x + r, y + r + 2), outline=(128, 128, 128, 255))

        # smooth recording-button blinking, even if update() is called multiple times in one second
        now = time.monotonic()
        if (now - self.lastRecordingStatus) >= 1:
            self.recordingIconVisible = not self.recordingIconVisible
            self.lastRecordingStatus = now

    def key(self, event):
        print("WebcamScreen.key(): %s" % event)
        if event == "JOYSTICK_RELEASED":
            if self.menuselection == 1:
                self.isRecording = not self.isRecording
        if event == "UP_RELEASED":
            if self.menuselection == 0:
                self.updateCamTime = self.updateCamTime + 5
            self.restartCamTimer()
        if event == "DOWN_RELEASED":
            if self.menuselection == 0:
                self.updateCamTime = self.updateCamTime - 5
            self.restartCamTimer()
        if event == "LEFT_RELEASED":
            self.menuselection = (self.menuselection - 1) % 2
        if event == "RIGHT_RELEASED":
            self.menuselection = (self.menuselection + 1) % 2

        if self.updateCamTime < 5:
            self.updateCamTime = 5

        self.update()

import LCD_1in44
import LCD_Config
import datetime
import time
import cv2
import array as arr
from random import randrange

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

from screen import Screen
from threading import Timer
from themes import getTheme as getTheme


class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.visible = True


class SystemScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(SystemScreen, self).__init__()
        # print("SystemScreen.SystemScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.screenTimer = None
        self.updateScreenTime = 0.2
        self.running = True
        self.blocks = []
        self.ball_speed_x = 0.0
        self.ball_speed_y = 0.0
        self.ball_x = 0
        self.ball_y = 0

        self.bat_x = 0
        self.bat_y = 0
        self.bat_size = 0
        self.remaining_balls = 0

        self.reset()

    def reset(self):
        self.ball_speed_x = 2.0
        self.ball_speed_y = 2.0
        self.ball_x = 60
        self.ball_y = 60

        self.bat_x = 60
        self.bat_y = 120
        self.bat_size = 40
        self.remaining_balls = 3
        self.blocks = []

        self.blocks.append(Block(10, 10, (190, 40, 40, 255)))
        self.blocks.append(Block(30, 10, (0, 180, 80, 255)))
        self.blocks.append(Block(50, 10, (120, 180, 0, 255)))
        self.blocks.append(Block(70, 10, (120, 80, 250, 255)))
        self.blocks.append(Block(90, 10, (0, 255, 255, 255)))

        self.blocks.append(Block(20, 20, (90, 240, 140, 255)))
        self.blocks.append(Block(40, 20, (100, 10, 180, 255)))
        self.blocks.append(Block(60, 20, (220, 180, 255, 255)))
        self.blocks.append(Block(80, 20, (0, 250, 250, 255)))

        self.blocks.append(Block(10, 30, (190, 240, 140, 255)))
        self.blocks.append(Block(30, 30, (100, 80, 280, 255)))
        self.blocks.append(Block(50, 30, (220, 20, 100, 255)))
        self.blocks.append(Block(70, 30, (90, 80, 50, 255)))
        self.blocks.append(Block(90, 30, (120, 100, 150, 255)))


    def stop(self):
        print("STOP")
        self.running = False

        self.screenTimer.cancel()
        del self.screenTimer

    def setVisible(self, visible):
        print("SystemScreen.setVisible(%s)" % visible)

        if visible and not self.isVisible():
            self.running = True
            self.screenTimer = Timer(self.updateScreenTime, self.updateScreenTimeout)
            self.screenTimer.start()
        if not visible and self.isVisible():
            self.stop()

        super(SystemScreen, self).setVisible(visible)

        if visible and self.isVisible():
            self.update()


    def updateScreenTimeout(self):
        # print("SystemScreen.updateScreenTimeout() %s" % self.isVisible())
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

    def showErrorScreen(self):
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        draw.text((10, 94), "No camera detected", fill=getTheme()["headline_color"])
        self.LCD.LCD_ShowImage(image, 0, 0)


    def checkBallCollision(self):
        if self.ball_y >= self.bat_y:
            if self.bat_x < self.ball_x < (self.bat_x + self.bat_size):
                # ball hits the bat
                self.ball_speed_y = -self.ball_speed_y
                self.ball_speed_x = self.ball_speed_x + randrange(5)/10
            else:
                # ball is out
                self.remaining_balls -= 1
                self.ball_x = 60
                self.ball_y = 60
                if self.remaining_balls <= 0:
                    self.ball_speed_x = 0
                    self.ball_speed_y = 0
        if self.ball_x >= 125 or self.ball_x <= 0:
            self.ball_speed_x = -self.ball_speed_x
        if self.ball_y <= 0:
            self.ball_speed_y = -self.ball_speed_y
        for b in self.blocks:
            if b.visible and b.x < self.ball_x < (b.x+20) and b.y < self.ball_y < b.y+10:
                b.visible = False
                self.ball_speed_y = -self.ball_speed_y
                self.ball_speed_x = -self.ball_speed_x

        print('self.ball_speed_x: ', self.ball_speed_x)

    def drawRemainingBalls(self, draw):
        if self.remaining_balls >= 3:
            draw.rectangle([(100, 2), (104, 6)], fill=(50, 80, 90, 255))
        if self.remaining_balls >= 2:
            draw.rectangle([(108, 2), (112, 6)], fill=(50, 80, 90, 255))
        if self.remaining_balls >= 1:
            draw.rectangle([(116, 2), (120, 6)], fill=(50, 80, 90, 255))

    def drawBlock(self, draw, rect, col):
        draw.rectangle(rect, fill=col, outline=(0, 0, 0, 255))

    def drawBlocks(self, draw):

        for b in self.blocks:
            if b.visible:
                self.drawBlock(draw, [(b.x, b.y), (b.x+20, b.y+10)], b.color)

        # for i in range(len(ar)):
        #    theSum = theSum + ar[i]


    def drawBat(self, draw, rect, col):
        draw.rectangle(rect, fill=col, outline=(0, 0, 0, 255))

    def drawBall(self, draw):
        draw.rectangle([(self.ball_x-2, self.ball_y-2), (self.ball_x+2, self.ball_y+2)], fill=(50, 80, 90, 255))

    def update(self):
        print("SystemScreen.update() %s" % self.isVisible())
        if not self.isVisible():
            return

        drawimage = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(drawimage, 'RGBA')

        self.drawBlocks(draw)
        self.drawBall(draw)
        self.drawBat(draw, [(self.bat_x, self.bat_y), (self.bat_x+self.bat_size, self.bat_y+5)], (50, 80, 90, 255))
        self.drawRemainingBalls(draw)
        self.checkBallCollision()

        self.ball_x = self.ball_x + self.ball_speed_x
        self.ball_y = self.ball_y + self.ball_speed_y

        if self.remaining_balls == 0:
            draw.text((25, 60), 'GAME OVER', fill=getTheme()["headline_color"], font=getTheme()["headlinefont"])

        self.LCD.LCD_ShowImage(drawimage, 0, 0)
        del drawimage


    def key(self, event):
        print("SystemScreen.key(): %s" % event)
        if event == "JOYSTICK_RELEASED":
            pass
        if event == "KEY2_RELEASED":
            self.reset()
        if event == "UP_RELEASED":
            pass
        if event == "DOWN_RELEASED":
            pass
        if event == "LEFT_RELEASED":
            self.bat_x = self.bat_x - 10;
        if event == "RIGHT_RELEASED":
            self.bat_x = self.bat_x + 10;

        if self.bat_x < 0:
            self.bat_x = 0

        # self.update()

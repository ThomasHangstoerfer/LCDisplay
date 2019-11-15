# -*- coding: utf-8 -*-
#
# Author: Thomas Hangstoerfer
# License: MIT
#

import datetime
import time
import cv2
import sys
import array as arr
from random import randrange

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps

from screen import Screen
from threading import Timer
from themes import getTheme as getTheme


class SpecialItem:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.size = 5
        self.speed_y = 2.0
        self.visible = False
        if item_type == 1:
            self.color = (255, 0, 0, 255)
            self.outline_color = (255, 255, 255, 255)
        else:
            self.color = (0, 255, 0, 255)
            self.outline_color = (255, 0, 0, 255)
        self.duration = 5
        self.item_type = item_type

    def draw(self, drawO):
        if self.visible:
            drawO.rectangle([(self.x, self.y), (self.x + self.size, self.y + self.size)], fill=self.color, outline=self.outline_color)

    def move(self):
        if self.visible:
            self.y += self.speed_y


class Block:
    def __init__(self, x, y, color, special_item=None, hits=1):
        self.x = x
        self.y = y
        self.color = color
        self.visible = True
        self.hits = hits
        self.state = self.hits
        self.special_item = special_item

    def wasHit(self):
        self.state -= 1
        if self.state <= 0:
            self.state = 0

    def isVisible(self):
        return self.state > 0

    def draw(self, drawO):

        #self.drawBlock(draw, [(self.x, self.y), (self.x + 20, self.y + 10)], self.color)
        drawO.rectangle([(self.x, self.y), (self.x + 20, self.y + 10)], fill=self.color, outline=(0, 0, 0, 255))
        if self.hits > 1 and self.state > 1:
            drawO.rectangle([(self.x+1, self.y+1), (self.x + 20 - 1, self.y + 10 - 1)], outline=(0, 0, 0, 255))


class Bat:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.default_size = size
        self.size = self.default_size
        self.default_color = (50, 80, 90, 255)
        self.default_outline_color = (0, 0, 0, 255)
        self.special_item = None
        self.special_timestamp = 0

        self.color = self.default_color
        self.outline_color = self.default_outline_color

    def draw(self, drawO):
        # print('Bat.draw()', self.special_item)
        if self.special_item is not None:
            # print('duration %i special_timestamp %i' % (self.special_item.duration, self.special_timestamp))
            if self.special_item.duration < time.monotonic() - self.special_timestamp:
                self.color = self.default_color
                self.outline_color = self.default_outline_color
                self.special_item = None
                self.size = self.default_size
        drawO.rectangle([(self.x, self.y), (self.x+self.size, self.y+5)], fill=self.color, outline=self.outline_color)

    def setSpecialItem(self, special_item):
        # print('Bat.setSpecialItem()', special_item)
        self.special_item = special_item
        self.color = special_item.color
        self.outline_color = special_item.outline_color
        self.special_timestamp = time.monotonic()
        if special_item.item_type == 2:
            self.size = self.size/2

    def getSpecialItemType(self):
        return self.special_item.item_type if self.special_item is not None else 0



class BreakoutScreen(Screen):
    def __init__(self, screenManager):
        super(BreakoutScreen, self).__init__()
        # print("BreakoutScreen.BreakoutScreen() ")
        self.screenManager = screenManager
        self.screenTimer = None
        self.updateScreenTime = 0.2
        self.running = True
        self.blocks = []
        self.special_items = []
        self.ball_speed_x = 0.0
        self.ball_speed_y = 0.0
        self.ball_x = 0
        self.ball_y = 0

        self.bat = Bat(0, 0, 30)
        #self.bat.x = 0
        #self.bat.y = 0
        #self.bat.size = 0
        self.remaining_balls = 0
        self.level = 1
        self.level_count = 3
        self.reset()

    def setupLevel(self, level):
        self.ball_x = self.bat.x+(self.bat.size/2)
        self.ball_y = self.bat.y-2
        self.ball_speed_x = 0.0
        self.ball_speed_y = 0.0
        self.blocks = []
        self.special_items = []

        if level == 1:
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
            self.blocks.append(Block(50, 30, (220, 20, 100, 255), None, 2))
            self.blocks.append(Block(70, 30, (90, 80, 50, 255), SpecialItem(70+10, 30+10, 1)))
            self.blocks.append(Block(90, 30, (120, 100, 150, 255)))
        elif level == 2:
            self.blocks.append(Block(10, 10, (190, 40, 40, 255)))
            self.blocks.append(Block(30, 10, (0, 180, 80, 255)))
            self.blocks.append(Block(50, 10, (120, 180, 0, 255)))
            self.blocks.append(Block(70, 10, (120, 80, 250, 255)))
            self.blocks.append(Block(90, 10, (0, 255, 255, 255)))

            self.blocks.append(Block(10, 30, (90, 240, 140, 255)))
            self.blocks.append(Block(50, 30, (100, 10, 180, 255)))
            self.blocks.append(Block(90, 30, (220, 180, 255, 255)))
            #self.blocks.append(Block(80, 30, (0, 250, 250, 255)))

            self.blocks.append(Block(10, 50, (190, 240, 140, 255), SpecialItem(10+10, 50+10, 2)))
            self.blocks.append(Block(30, 50, (100, 80, 280, 255)))
            self.blocks.append(Block(50, 50, (220, 20, 100, 255)))
            self.blocks.append(Block(70, 50, (90, 80, 50, 255)))
            self.blocks.append(Block(90, 50, (120, 100, 150, 255)))
        else:
            self.blocks.append(Block(30, 10, (0, 180, 80, 255), None, 2))
            self.blocks.append(Block(70, 10, (120, 80, 250, 255), None, 2))

            self.blocks.append(Block(50, 30, (100, 10, 180, 255), SpecialItem(50+10, 30+10, 1)))

            self.blocks.append(Block(10, 50, (190, 240, 140, 255)))
            self.blocks.append(Block(30, 60, (100, 80, 280, 255)))
            self.blocks.append(Block(50, 70, (220, 20, 100, 255)))
            self.blocks.append(Block(70, 60, (90, 80, 50, 255)))
            self.blocks.append(Block(90, 50, (120, 100, 150, 255)))


    def reset(self):

        self.bat.size = 40
        self.bat.x = 60
        self.bat.y = 120
        self.ball_x = self.bat.x+(self.bat.size/2)
        self.ball_y = self.bat.y-2
        self.ball_speed_x = 0.0
        self.ball_speed_y = 0.0

        self.remaining_balls = 3
        self.level = 1
        self.blocks = []

        self.setupLevel(self.level)

        # test-setup:
        #self.blocks = []
        #self.blocks.append(Block(90, 30, (120, 100, 150, 255)))
        #self.ball_speed_x = 2.0
        #self.ball_speed_y = -2.0
        #self.ball_x = 70
        #self.ball_y = 65

    def stop(self):
        print("STOP")
        self.running = False

        self.screenTimer.cancel()
        del self.screenTimer

    def setVisible(self, visible):
        print("BreakoutScreen.setVisible(%s)" % visible)

        if visible and not self.isVisible():
            self.running = True
            self.screenTimer = Timer(self.updateScreenTime, self.updateScreenTimeout)
            self.screenTimer.start()
        if not visible and self.isVisible():
            self.stop()

        super(BreakoutScreen, self).setVisible(visible)

        if visible and self.isVisible():
            self.update()


    def updateScreenTimeout(self):
        # print("BreakoutScreen.updateScreenTimeout() %s" % self.isVisible())
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
        self.screenManager.draw(image)

    def showErrorScreen(self):
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        draw.text((10, 94), "No camera detected", fill=getTheme()["headline_color"])
        self.screenManager.draw(image)


    def checkBallCollision(self):

        if self.ball_speed_x == 0 and self.ball_speed_y == 0:
            return

        # collision with walls
        if self.ball_x+2 >= 125 or self.ball_x-2 <= 0:
            print('collision with wall: ball (%i, %i, %i, %i)' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2))
            self.ball_speed_x = -self.ball_speed_x

        # collision with bat
        if self.ball_y+2 >= self.bat.y:
            if self.bat.x < self.ball_x < (self.bat.x + self.bat.size):
                # ball hits the bat
                print('ball hits the bat: ball (%i, %i, %i, %i) bat (%i, %i, %i, %i)' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2, self.bat.x, self.bat.y, self.bat.x + self.bat.size, self.bat.y+10))
                self.ball_speed_y = -self.ball_speed_y
                self.ball_speed_x = self.ball_speed_x + randrange(5)/10
            else:
                # ball is out
                print('ball is out: ball (%i, %i, %i, %i) bat (%i, %i, %i, %i)' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2, self.bat.x, self.bat.y, self.bat.x + self.bat.size, self.bat.y+10))
                self.remaining_balls -= 1
                self.ball_x = 60
                self.ball_y = 60
                if self.remaining_balls <= 0:
                    self.ball_speed_x = 0
                    self.ball_speed_y = 0

        # collision with ceiling
        if self.ball_y-2 <= 0:
            print('collision with ceiling: ball (%i, %i, %i, %i)' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2))
            self.ball_speed_y = -self.ball_speed_y

        # collision with blocks
        for b in self.blocks:
            # print('checkCollision() ball (%i, %i, %i, %i) block (%i, %i, %i, %i) ' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2, b.x, b.y, b.x+20, b.y+10))
            if b.isVisible():
                # collision from below
                block_was_hit = False
                if b.y + 10 >= self.ball_y - 2 >= b.y and b.x <= self.ball_x <= b.x + 20:  # unterkante_block == oberkante_ball
                    print('collision from below ball (%i, %i, %i, %i) block (%i, %i, %i, %i) ' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2, b.x, b.y, b.x+20, b.y+10))
                    block_was_hit = True
                    if self.bat.getSpecialItemType() == 1:
                        pass  # ball goes through blocks
                    else:
                        self.ball_speed_y = -self.ball_speed_y
                    # self.ball_y = b.y + 10 + 2
                # collision from above
                elif self.ball_y+2 >= b.y >= self.ball_y-2 and self.ball_x-2 >= b.x and self.ball_x+2 <= b.x+20:  # oberkante_block == unterkante_ball:
                    print('collision from above ball (%i, %i, %i, %i) block (%i, %i, %i, %i) ' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2, b.x, b.y, b.x+20, b.y+10))
                    block_was_hit = True
                    if self.bat.getSpecialItemType() == 1:
                        pass  # ball goes through blocks
                    else:
                        self.ball_speed_y = -self.ball_speed_y
                    # self.ball_y = b.y - 2
                # collision from left
                elif self.ball_x+2 >= b.x >= self.ball_x-2 and self.ball_y+2 >= b.y and self.ball_y-2 <= b.y+10:  # linkekante_block == rechtekante_ball:
                    print('collision from left ball (%i, %i, %i, %i) block (%i, %i, %i, %i) ' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2, b.x, b.y, b.x+20, b.y+10))
                    block_was_hit = True
                    if self.bat.getSpecialItemType() == 1:
                        pass  # ball goes through blocks
                    else:
                        self.ball_speed_x = -self.ball_speed_x
                    # self.ball_x = b.x - 2
                # collision from right
                elif b.x+20 >= self.ball_x-2 and self.ball_x+2 >= b.x and self.ball_y+2 >= b.y and self.ball_y-2 <= b.y+10:  # rechtekante_block == linkekante_ball:
                    print('collision from right ball (%i, %i, %i, %i) block (%i, %i, %i, %i) ' % (self.ball_x-2, self.ball_y-2, self.ball_x+2, self.ball_y+2, b.x, b.y, b.x+20, b.y+10))
                    block_was_hit = True
                    if self.bat.getSpecialItemType() == 1:
                        pass  # ball goes through blocks
                    else:
                        self.ball_speed_x = -self.ball_speed_x
                    # self.ball_x = b.x+20 + 2
                if block_was_hit:
                    b.wasHit()
                    if b.special_item is not None:
                        b.special_item.visible = True
                        self.special_items.append(b.special_item)
                    self.ball_speed_x += 0.2 if self.ball_speed_x > 0 else -0.2
                    self.ball_speed_y += 0.2 if self.ball_speed_y > 0 else -0.2
                    break

        # bat collision with special_items
        for i in self.special_items:
            if self.bat.x <= i.x <= (self.bat.x + self.bat.size):
                if i.visible and i.y+i.size >= self.bat.y:
                    print('bat collision with special_items')
                    i.visible = False
                    self.bat.setSpecialItem(i)

        print('self.ball_speed_x: ', self.ball_speed_x)

    def drawRemainingBalls(self, draw):
        if self.remaining_balls >= 3:
            draw.rectangle([(100, 2), (104, 6)], fill=(50, 80, 90, 255))
        if self.remaining_balls >= 2:
            draw.rectangle([(108, 2), (112, 6)], fill=(50, 80, 90, 255))
        if self.remaining_balls >= 1:
            draw.rectangle([(116, 2), (120, 6)], fill=(50, 80, 90, 255))

    def drawBlocks(self, draw):

        for b in self.blocks:
            if b.isVisible():
                b.draw(draw)
                #self.drawBlock(draw, [(b.x, b.y), (b.x+20, b.y+10)], b.color)

        # for i in range(len(ar)):
        #    theSum = theSum + ar[i]

    def drawBall(self, draw):
        draw.rectangle([(self.ball_x-2, self.ball_y-2), (self.ball_x+2, self.ball_y+2)], fill=(50, 80, 90, 255))

    def drawSpecialItems(self, draw):
        for i in self.special_items:
            i.draw(draw)

    def moveSpecialItems(self):
        for i in self.special_items:
            i.move()

    def update(self):
        # print("BreakoutScreen.update() %s" % self.isVisible())
        if not self.isVisible():
            return

        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image, 'RGBA')

        self.ball_x = self.ball_x + self.ball_speed_x
        self.ball_y = self.ball_y + self.ball_speed_y

        self.moveSpecialItems()
        self.drawSpecialItems(draw)
        self.drawBlocks(draw)
        self.drawBall(draw)
        # self.drawBat(draw, [(self.bat.x, self.bat.y), (self.bat.x+self.bat.size, self.bat.y+5)], (50, 80, 90, 255))
        self.bat.draw(draw)
        self.drawRemainingBalls(draw)
        self.checkBallCollision()

        if self.remaining_balls == 0:
            draw.text((25, 60), 'GAME OVER', fill=getTheme()["headline_color"], font=getTheme()["headlinefont"])

        remaining_blocks = 0
        for b in self.blocks:
            if b.isVisible():
                remaining_blocks += 1
        if remaining_blocks == 0:
            self.level = (self.level+1) % self.level_count
            self.setupLevel(self.level)

        self.screenManager.draw(image)

        del image

    def key(self, event):
        print("BreakoutScreen.key(): %s" % event)
        if event == "JOYSTICK_RELEASED":
            if self.ball_speed_x == 0 and self.ball_speed_y == 0:
                self.ball_speed_x = 3.0
                self.ball_speed_y = -3.0
        if event == "KEY2_RELEASED":
            self.reset()
        if event == "KEY3_RELEASED":
            print('self.take_screenshot = True')
            self.screenManager.take_screenshot = True
        if event == "UP_RELEASED":
            self.level = (self.level+1) % self.level_count
            self.setupLevel(self.level)
        if event == "DOWN_RELEASED":
            self.level = (self.level-1) % self.level_count
            self.setupLevel(self.level)
        if event == "LEFT_RELEASED":
            self.bat.x = self.bat.x - 10
            if self.ball_speed_x == 0 and self.ball_speed_y == 0:
                # ball follows bat
                self.ball_x = self.bat.x+(self.bat.size/2)
                self.ball_y = self.bat.y-2

        if event == "RIGHT_RELEASED":
            self.bat.x = self.bat.x + 10
            if self.ball_speed_x == 0 and self.ball_speed_y == 0:
                # ball follows bat
                self.ball_x = self.bat.x+(self.bat.size/2)
                self.ball_y = self.bat.y-2

        if self.bat.x < 0:
            self.bat.x = 0
        if self.bat.x+self.bat.size > 128:
            self.bat.x = 128 - self.bat.size

        # self.update()

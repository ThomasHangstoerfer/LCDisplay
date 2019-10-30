import LCD_1in44
import LCD_Config
import datetime
import math
from PIL import Image, ImageDraw, ImageFont, ImageColor
from themes import getTheme as getTheme
from themes import changeTheme as changeTheme
from screen import Screen
from threading import Timer


# duration is in seconds
# wait for time completion
# t.join()

class MenuScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(MenuScreen, self).__init__()
        # print("MenuScreen.MenuScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentline = 0
        self.entries = [
            {"name": "SmartHome", "screenname": "smarthome"},
            {"name": "Cam", "screenname": "cam"},
            {"name": "WebCam", "screenname": "webcam"},
            {"name": "Network", "screenname": "network"},
            {"name": "Slideshow", "screenname": "slideshow"},
            {"name": "Dilli", "screenname": ""},
            {"name": "System", "screenname": "system"}
        ]

    def setVisible(self, visible):
        print("MenuScreen.setVisible(%s)" % visible)
        if visible and not self.isVisible():
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if not visible and self.isVisible():
            self.t.cancel()
        super(MenuScreen, self).setVisible(visible)

    def updateTimeout(self):
        # print("MenuScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def update(self):
        # print("MenuScreen.update() %s" % self.isVisible())
        if not self.isVisible():
            return
        # self.LCD.LCD_Clear()
        # image = Image.new("RGB", (self.LCD.width, self.LCD.height), "WHITE")
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)
        # draw.rectangle([(1,1),(127,10)],fill = "RED")

        draw.text((35, 1), 'M E N U', fill=getTheme()["headline_color"], font=getTheme()["headlinefont"])
        draw.line([(0, 18), (127, 18)], fill=getTheme()["headline_color"], width=3)

        y_offset = 24
        for i in range(len(self.entries)):
            if self.entries[i]["name"] != "":
                o = 0
                if self.currentline == i:
                    o = o + 5
                draw.text((1 + o, y_offset), self.entries[i]["name"], fill=(
                    getTheme()["highlight_text_color"] if (self.currentline == i) else getTheme()["text_color"]),
                          font=getTheme()["font"])
                if self.currentline == i:
                    draw.line([(0, y_offset), (127, y_offset)], fill=getTheme()["highlight_text_color"], width=1)
                    draw.line([(0, y_offset + 10), (127, y_offset + 10)], fill=getTheme()["highlight_text_color"],
                              width=1)

            y_offset += 12

        draw.text((40, 110), datetime.datetime.now().strftime('%H:%M:%S'), fill=getTheme()["highlight_text_color"],
                  font=getTheme()["clockfont"])

        self.LCD.LCD_ShowImage(image, 0, 0)

    def key(self, event):
        global screenManager
        print("MenuScreen.key(): %s" % event)
        entry_count = len(self.entries)
        if event == "UP_RELEASED":
            self.currentline = (self.currentline - 1) % entry_count
        if event == "DOWN_RELEASED":
            self.currentline = (self.currentline + 1) % entry_count
        if event == "LEFT_RELEASED":
            # self.currentline = (self.currentline - 1 ) % entry_count
            changeTheme("blue")
        if event == "RIGHT_RELEASED":
            # self.currentline = (self.currentline + 1 ) % entry_count
            changeTheme("red")
        if event == "JOYSTICK_RELEASED":
            if self.entries[self.currentline]["screenname"] != "":
                self.screenManager.switchToScreen(self.entries[self.currentline]["screenname"])
        print("theme[text_color] " + getTheme()["text_color"])
        self.update()

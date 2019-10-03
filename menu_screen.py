import LCD_1in44
import LCD_Config
import datetime

from PIL import Image,ImageDraw,ImageFont,ImageColor

from screen import Screen
from threading import Timer


# duration is in seconds
# wait for time completion
#t.join()

class MenuScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(MenuScreen, self).__init__()
        print("MenuScreen.MenuScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentline = 0

    def setVisible(self, visible):
        print("MenuScreen.setVisible(%s)" % visible)
        if (visible and not self.isVisible() ):
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if (not visible and self.isVisible() ):
            self.t.cancel()
        super(MenuScreen, self).setVisible(visible)

    def updateTimeout(self):
        #print("MenuScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def update(self):
        print("MenuScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return
        #self.LCD.LCD_Clear()
        image = Image.new("RGB", (self.LCD.width, self.LCD.height), "WHITE")
        draw = ImageDraw.Draw(image)
        #draw.rectangle([(1,1),(127,10)],fill = "RED")

        draw.text((40, 1), 'M E N U', fill = "BLUE")
        #draw.text((1, 6), '--------------------', fill = "BLUE")
        draw.text((1, 24), 'SmartHome', fill = ("BLACK" if (self.currentline==0) else "BLUE"))
        draw.text((1, 36), 'Network', fill = ("BLACK" if (self.currentline==1) else "BLUE"))
        draw.text((1, 48), 'Slideshow', fill = ("BLACK" if (self.currentline==2) else "BLUE"))
        draw.text((1, 60), 'Dilli', fill = ("BLACK" if (self.currentline==3) else "BLUE"))
        draw.text((1, 84), 'System (Shutdown, Reboot)', fill = ("BLACK" if (self.currentline==4) else "BLUE"))
        draw.text((80, 118), datetime.datetime.now().strftime('%H:%M:%S'), fill = "BLUE")
        
        self.LCD.LCD_ShowImage(image,0,0)

    def key(self, event):
        global screenManager
        print("MenuScreen.key(): %s" % event)
        if ( event == "UP_RELEASED" ):
            self.currentline = (self.currentline - 1 ) % 4
        if ( event == "DOWN_RELEASED" ):
            self.currentline = (self.currentline + 1 ) % 4
        if ( event == "LEFT_RELEASED" ):
            self.currentline = (self.currentline - 1 ) % 4
        if ( event == "RIGHT_RELEASED" ):
            self.currentline = (self.currentline + 1 ) % 4
        if ( event == "JOYSTICK_RELEASED" ):
            if ( self.currentline == 1):
                self.screenManager.switchToScreen("network")
            if ( self.currentline == 2):
                self.screenManager.switchToScreen("slideshow")
        self.update()


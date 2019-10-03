import LCD_1in44
import LCD_Config
import datetime

from PIL import Image,ImageDraw,ImageFont,ImageColor

from screen import Screen
from threading import Timer
import utils


# duration is in seconds
# wait for time completion
#t.join()

class NetworkScreen(Screen):
    def __init__(self, LCD, screenManager):
        super(NetworkScreen, self).__init__()
        print("NetworkScreen.NetworkScreen() ")
        self.LCD = LCD
        self.screenManager = screenManager
        self.currentline = 0
        self.bitrate = 0
        self.quality = 0
        self.essid = ""

    def setVisible(self, visible):
        print("NetworkScreen.setVisible(%s)" % visible)
        if (visible and not self.isVisible() ):
            self.t = Timer(1, self.updateTimeout)
            self.t.start()
            self.update()
        if (not visible and self.isVisible() ):
            self.t.cancel()
        super(NetworkScreen, self).setVisible(visible)

    def updateTimeout(self):
        #print("NetworkScreen.updateTimeout() %s" % self.isVisible())
        self.t.cancel()
        self.t = Timer(1, self.updateTimeout)
        self.t.start()
        self.update()

    def update(self):
        print("NetworkScreen.update() %s" % self.isVisible())
        if (not self.isVisible()):
            return
        #self.LCD.LCD_Clear()
        image = Image.new("RGB", (self.LCD.width, self.LCD.height), "WHITE")
        draw = ImageDraw.Draw(image)
        #draw.rectangle([(1,1),(127,10)],fill = "RED")

        try:
            self.bitrate, self.quality, self.essid = utils.get_network_info('wlan0')

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



        draw.text((30, 1), 'N E T W O R K', fill = "BLUE")
        #draw.text((1, 6), '--------------------', fill = "BLUE")
        draw.text((1, 24), 'WiFi: ' + self.essid, fill = ("BLACK" if (self.currentline==0) else "BLUE"))
        draw.text((1, 36), 'WiFi: ' + str(self.quality) + '% ' + str(self.bitrate), fill = ("BLACK" if (self.currentline==0) else "BLUE"))
        draw.text((1, 48), 'IP: ' + utils.get_ip_address(), fill = ("BLACK" if (self.currentline==0) else "BLUE"))
        draw.text((80, 118), datetime.datetime.now().strftime('%H:%M:%S'), fill = "BLUE")
        
        self.LCD.LCD_ShowImage(image,0,0)

    def key(self, event):
        global screenManager
        print("NetworkScreen.key(): %s" % event)
        if ( event == "UP_RELEASED" ):
            self.currentline = (self.currentline - 1 ) % 1
        if ( event == "DOWN_RELEASED" ):
            self.currentline = (self.currentline + 1 ) % 1
        if ( event == "LEFT_RELEASED" ):
            self.currentline = (self.currentline - 1 ) % 1
        if ( event == "RIGHT_RELEASED" ):
            self.currentline = (self.currentline + 1 ) % 1
        if ( event == "JOYSTICK_RELEASED" ):
            self.screenManager.switchToScreen("menu")
        self.update()


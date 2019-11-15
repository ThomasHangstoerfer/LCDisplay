import datetime
import time
import paho.mqtt.client as mqtt #import the client1

from PIL import Image,ImageDraw,ImageFont,ImageColor
from themes import getTheme as getTheme
from themes import changeTheme as changeTheme

from screen import Screen
from threading import Timer
import utils


import asyncio
import websockets



async def hello():
    # uri = "ws://apollo:8765"
    try:
        uri = "ws://apollo:8083/fhem?XHR=1&inform=type=status;filter=room=Wohnzimmer;since=1567258298;fmt=JSON&fw_id=73&timestamp=1567258300581"
        async with websockets.connect(uri) as websocket:
            #name = input("What's your name? ")

            #await websocket.send(name)
            #print(f"> {name}")

            greeting = await websocket.recv()
            print("< ${greeting}")
    except:
        pass

asyncio.get_event_loop().run_until_complete(hello())
class SmarthomeScreen(Screen):
    def __init__(self, screenManager):
        super(SmarthomeScreen, self).__init__()
        #print("SmarthomeScreen.SmarthomeScreen() ")
        self.screenManager = screenManager
        self.currentline = 0
        self.big_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 15)
        self.update_timer = None

        self.mqtt_broker = "apollo"
        self.mqtt_client = mqtt.Client("lcdisplay@chilipi")
        self.mqtt_client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)
        print("message qos=",  message.qos)
        print("message retain flag=", message.retain)

    def setVisible(self, visible):
        print("SmarthomeScreen.setVisible(%s)" % visible)
        if visible and not self.isVisible():
            self.update_timer = Timer(1, self.updateTimeout)
            self.update_timer.start()
            self.update()
            print("connecting to broker")
            try:
                self.mqtt_client.connect(self.mqtt_broker)
                self.mqtt_client.loop_start()
                self.mqtt_client.subscribe("house/bulbs/bulb1")
                self.mqtt_client.publish("house/bulbs/bulb1","OFF")
            except:
                print('Exception in mqtt-connection')

        if not visible and self.isVisible():
            try:
                self.update_timer.cancel()
                self.mqtt_client.disconnect()
                self.mqtt_client.loop_stop()
            except:
                print('Exceptions while disconnecting mqtt-client')

        super(SmarthomeScreen, self).setVisible(visible)

    def updateTimeout(self):
        # print("SmarthomeScreen.updateTimeout() %s" % self.isVisible())
        self.update_timer.cancel()
        self.update_timer = Timer(1, self.updateTimeout)
        self.update_timer.start()
        self.update()

    def update(self):
        # print("SmarthomeScreen.update() %s" % self.isVisible())
        if not self.isVisible():
            return
        image = getTheme()["background_image"].copy()
        draw = ImageDraw.Draw(image)

        draw.text((5, 1), 'SMARTHOME', fill = getTheme()["headline_color"], font=getTheme()["headlinefont"])
        draw.line([(0, 18), (127, 18)], fill="BLACK", width=1)
        draw.text((1, 42), 'Licht: ', fill=("BLACK" if (self.currentline == 0) else "BLUE"))
        draw.text((1, 54), 'Heizung: ', fill=("BLACK" if (self.currentline == 0) else "BLUE"))
        draw.text((1, 66), 'Fenster: ', fill=("BLACK" if (self.currentline == 0) else "BLUE"))
        # draw.text((1, 78), 'Make: ' + utils.get_make_running(), fill = "WHITE")

        draw.text((80, 118), datetime.datetime.now().strftime('%H:%M:%S'), fill=getTheme()["headline_color"])

        self.screenManager.draw(image)

    def key(self, event):
        print("SmarthomeScreen.key(): %s" % event)
        if ( event == "UP_RELEASED" ):
            self.currentline = (self.currentline - 1 ) % 1
        if ( event == "DOWN_RELEASED" ):
            self.currentline = (self.currentline + 1 ) % 1
        if ( event == "LEFT_RELEASED" ):
            self.currentline = (self.currentline - 1 ) % 1
        if ( event == "RIGHT_RELEASED" ):
            self.currentline = (self.currentline + 1 ) % 1
        if ( event == "JOYSTICK_RELEASED" ):
            #self.screenManager.switchToScreen("menu")
            pass
        self.update()


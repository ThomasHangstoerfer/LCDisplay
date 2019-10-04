import LCD_1in44
import LCD_Config

from PIL import Image,ImageDraw,ImageFont,ImageColor
import RPi.GPIO as GPIO
import time
from screen import Screen
from menu_screen import MenuScreen
from slideshow_screen import SlideshowScreen
from network_screen import NetworkScreen
from cam_screen import CamScreen
from webcam_screen import WebcamScreen

KEY_UP_PIN     = 6 
KEY_DOWN_PIN   = 19
KEY_LEFT_PIN   = 5
KEY_RIGHT_PIN  = 26
KEY_PRESS_PIN  = 13
KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

#init GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.cleanup()
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

LCD = LCD_1in44.LCD()
print( "**********Init LCD**********")
Lcd_ScanDir = LCD_1in44.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
LCD.LCD_Init(Lcd_ScanDir)
LCD.LCD_Clear()

class ScreenManager(object):
    def __init__(self):
        pass

    def switchToScreen(self, screen):
        global currentscreen
        global screens
        if screen in screens and screens[screen] is not None:
            screens[currentscreen].setVisible(False)
            currentscreen = screen
            screens[currentscreen].setVisible(True)

screenManager = ScreenManager()

screens = {}
currentscreen = "menu"
screens["menu"] = MenuScreen(LCD, screenManager)
screens["network"] = NetworkScreen(LCD, screenManager)
screens["slideshow"] = SlideshowScreen(LCD, screenManager)
screens["cam"] = CamScreen(LCD, screenManager)
screens["webcam"] = WebcamScreen(LCD, screenManager)

screenManager.switchToScreen("menu")
#screenManager.switchToScreen("webcam")
screens[currentscreen].setVisible(True)

def handle_key_event(input_pin): 
    global currentscreen
    global screens
    global screenManager
    print("handle_key_event %s currentscreen %s " %( input_pin, currentscreen))
    
    if input_pin == KEY_UP_PIN:
        if GPIO.input(KEY_UP_PIN) == 0:
            screens[currentscreen].key('UP_PRESSED')
            print "Up pressed"        
        else:
            screens[currentscreen].key('UP_RELEASED')
            print "Up released"        
    if input_pin == KEY_DOWN_PIN:
        if GPIO.input(KEY_DOWN_PIN) == 0:
            screens[currentscreen].key('DOWN_PRESSED')
            print "Down pressed"        
        else:
            screens[currentscreen].key('DOWN_RELEASED')
            print "Down released"        
    if input_pin == KEY_LEFT_PIN:
        if GPIO.input(KEY_LEFT_PIN) == 0:
            screens[currentscreen].key('LEFT_PRESSED')
            print "Left pressed"        
        else:
            screens[currentscreen].key('LEFT_RELEASED')
            print "Left released"        
    if input_pin == KEY_RIGHT_PIN:
        if GPIO.input(KEY_RIGHT_PIN) == 0:
            screens[currentscreen].key('RIGHT_PRESSED')
            print "Right pressed"        
        else:
            screens[currentscreen].key('RIGHT_RELEASED')
            print "Right released"        
    if input_pin == KEY_PRESS_PIN:
        if GPIO.input(KEY_PRESS_PIN) == 0:
            screens[currentscreen].key('JOYSTICK_PRESSED')
            print "Joystick pressed"        
        else:
            screens[currentscreen].key('JOYSTICK_RELEASED')
            print "Joystick released"        
    if input_pin == KEY1_PIN:
        if GPIO.input(KEY1_PIN) == 0:
            print "Key1 pressed"        
            screens[currentscreen].key('KEY1_PRESSED')
        else:
            print "Key1 released"        
            screens[currentscreen].key('KEY1_RELEASED')
            screenManager.switchToScreen("menu")

    if input_pin == KEY2_PIN:
        if GPIO.input(KEY2_PIN) == 0:
            print "Key2 pressed"
            screens[currentscreen].key('KEY2_PRESSED')
            #screenManager.switchToScreen("slideshow")
            #image = Image.open('time.bmp')
            #LCD.LCD_ShowImage(image,0,0)

        else:
            print "Key2 released"        
            screens[currentscreen].key('KEY2_RELEASED')
    if input_pin == KEY3_PIN:
        if GPIO.input(KEY3_PIN) == 0:
            print "Key3 pressed"        
            screens[currentscreen].key('KEY3_PRESSED')
        else:
            print "Key3 released"        
            screens[currentscreen].key('KEY3_RELEASED')

    screens[currentscreen].update()

#try:
def main():
    
    # Caution: this runs in an other thread
    GPIO.add_event_detect(KEY_UP_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_DOWN_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_LEFT_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_RIGHT_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY_PRESS_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY1_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY2_PIN, GPIO.BOTH, callback=handle_key_event)
    GPIO.add_event_detect(KEY3_PIN, GPIO.BOTH, callback=handle_key_event)
    
 
    #image = Image.new("RGB", (LCD.width, LCD.height), "WHITE")
    image = Image.new("RGB", (LCD.width, LCD.height), "BLACK")
    draw = ImageDraw.Draw(image)

    ##font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 16)
    #print "***draw line"
    #draw.line([(0,0),(127,0)], fill = "BLUE",width = 5)
    #draw.line([(127,0),(127,127)], fill = "BLUE",width = 5)
    #draw.line([(127,127),(0,127)], fill = "BLUE",width = 5)
    #draw.line([(0,127),(0,0)], fill = "BLUE",width = 5)
    #print "***draw rectangle"
    #draw.rectangle([(18,10),(110,20)],fill = "RED")
    ##LCD_Config.Driver_Delay_ms(5000)

    #print "***draw text"
    #draw.text((33, 22), 'Jetzt ', fill = "BLUE")
    #draw.text((32, 36), 'kommt ein', fill = "BLUE")
    ##draw.text((28, 48), '1.44inch LCD ', fill = "BLUE")
    #draw.text((28, 48), 'MURCH ', fill = "BLUE")
    #LCD.LCD_ShowImage(image,0,0)
    #LCD_Config.Driver_Delay_ms(3000)

    #image = Image.open('time.bmp')
    #LCD.LCD_ShowImage(image,0,0)

    screens[currentscreen].update()
    
    #while (True):
    while 1:
        #time.sleep(.01)
        time.sleep(1)
    
if __name__ == '__main__':
    main()

#except:
#    print("except")
#    GPIO.cleanup()

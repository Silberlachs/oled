from machine import Pin, SPI, Timer, RTC
from ssd1306 import SSD1306_SPI
import time
from GuiBuilder import GuiBuilder
from usbridge import USBridge
from utime import sleep_ms

def main():
    
    guiBuilder.showLogo()
    guiBuilder.showLoadingScreen()
    payload = getMsg()
    
    guiBuilder.setAnimationCycle("running")
    guiBuilder.showConMsg()
    sleep_ms(100)

    firstPass = True	#emulate do-while loop

    #main working loop
    while True:
        if not firstPass:
            payload = getMsg()
        else:
            firstPass = False
            
        data = payload.split("#")
        
        #we are trying to (re)set GUI
        if(data[0][0] == "$"):
            guiBuilder.drawSystemHUD(data)
            continue
        
        #hardcoded for project
        guiBuilder.refreshDisplayValues()
        guiBuilder.updateValues(data)

    
#poll a message from bus, update animation until next message arrives
def getMsg():

    while True:
        try:
            serialMsg = usbridge.pollInput()

            if(serialMsg != "" and len(serialMsg) > 1):
                return serialMsg
            
            guiBuilder.update()	#update routine
            oled.show()
            sleep_ms(50)
        except:
            return -1

if __name__ == "__main__":
    spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
    oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16)) #WIDTH, HEIGHT, spi, dc,rst, cs
    oled.fill(0) 		# clear OLED
    oled.show()			# update OLED
    
    contrast = 128                                     	# 8 bit val: 0 - 255
    oled.contrast(contrast)
    guiBuilder = GuiBuilder(oled, contrast)
    usbridge = USBridge()
    
    while True:
        initialized = main()

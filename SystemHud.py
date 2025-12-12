from machine import Pin, SPI, Timer, RTC
from ssd1306 import SSD1306_SPI
import time
from GuiBuilder import GuiBuilder
from usbridge import USBridge
from utime import sleep_ms

def main():
    
    guiBuilder.showLogo()
    guiBuilder.showLoadingScreen()
    
    handshake = waitforconnection()
    
    #confirm protocol
    secret = getMsg()
    if((handshake[0] + handshake[1]) == int(secret)):
        guiBuilder.showConMsg()
        sleep_ms(200)
    
    payload = getMsg()
    names = extractGuiData(payload)
    data = extractValues(payload)

    guiBuilder.drawSystemHUD()
    guiBuilder.addEntries(names)
    
    #from now on we just need to check the requestNo. and data values
    while True:
        payload = getMsg()
        data = extractValues(payload)
        
        #hardcoded for project
        guiBuilder.refreshDisplayValue()
        guiBuilder.updateValues(data)
    
#extract values from a payload
def extractValues(payload):
    ordered = payload.split("#")
    values = []
    for x in range(0,len(ordered)):
        if(":" in ordered[x]):
            valueRaw = ordered[x].split(":")[1].strip().split(" ")
            values.append(int(valueRaw[0]))
            continue
        try:		#kind of butchering try-catch idea but w/e
            values.append(int(ordered[x]))
        except:
            continue
            
    return values
            
#prepare names for gui-HUD
def extractGuiData(payload):
    stats = payload.split("#")
    names = [stats[0]]
    for x in range(1,len(stats)):
        if(":" in stats[x]):
            #skip for now
            continue
        if(x%2 == 0):
            names.append(stats[x].replace("_",""))
    
    return names
    
#define a simple handshake protocoll
def waitforconnection():

    while True:
        try:
            serialMsg = usbridge.pollInput()

            if(serialMsg != "" and len(serialMsg) > 1):
                connect = serialMsg
                handshake = connect[1:].split("#")
                return [int(handshake[0]) , int(handshake[1])]
                
            oled.show()	#update animation here (guibuilder)
            sleep_ms(50)
        except:
            return -1

#poll a message from messagebus
def getMsg():
    while True:
        try:
            serialMsg = usbridge.pollInput()
            if(serialMsg != "" and len(serialMsg) > 1):
                return serialMsg
        except:
            return -1

if __name__ == "__main__":
    spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
    oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16)) #WIDTH, HEIGHT, spi, dc,rst, cs
    oled.fill(0) 	# clear OLED
    oled.show()		# update OLED
    oled.contrast(128)
    guiBuilder = GuiBuilder(oled)
    usbridge = USBridge()
    main()
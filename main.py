from machine import Pin, SPI, Timer, RTC
from ssd1306 import SSD1306_SPI
import time
from GuiBuilder import GuiBuilder
from usbridge import USBridge
from utime import sleep_ms

def main(initialized):
    
    if(initialized == 0):
        guiBuilder.showLogo()
        guiBuilder.showLoadingScreen()
        handshake = waitforconnection()
        initialized = 1
    
    #confirm protocol (not a handshake tcncly)
    #handshake sends 2 numbers, secret has to match these with every msg, or reset!
    secret = getMsg()
    secret = secret.split('#')[0]
    if((handshake[0] + handshake[1]) == int(secret)):
        guiBuilder.showConMsg()
        sleep_ms(200)
    
    payload = getMsg()
    names = extractGuiData(payload)
    data = extractValues(payload, int(secret))

    if(data[0] == -1):
        return 1

    guiBuilder.drawSystemHUD()
    guiBuilder.addEntries(names)
    
    #from now on we just need to check the requestNo. and data values
    while True:
        payload = getMsg()
        data = extractValues(payload, int(secret))
        
        if(data[0] == -1):
            return 1
        
        #hardcoded for project
        guiBuilder.refreshDisplayValue()
        guiBuilder.updateValues(data)


#extract values from a payload
def extractValues(payload, secretNum):
    ordered = payload.split("#")
    print(ordered)
    if(int(ordered[0]) != secretNum):
        return [-1]
    
    values = []
    for x in range(1,len(ordered)):
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
    names = []
    for x in range(1,len(stats)):
        if(":" in stats[x]):
            #skip for now
            continue
        if(x%2 == 1):
            names.append(stats[x].replace("_",""))
    
    return names
    
#define a simple protocoll
def waitforconnection():

    while True:
        try:
            serialMsg = usbridge.pollInput()

            if(serialMsg != "" and len(serialMsg) > 1):
                connect = serialMsg
                handshake = connect[1:].split("#")
                return [int(handshake[0]) , int(handshake[1])]
            
            guiBuilder.updateLoadingAnimation()	#update animation here (guibuilder)
            oled.show()
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
    initialized = 0
    
    while True:
        initialized = main(initialized)

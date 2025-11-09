from machine import Pin, SPI, Timer, RTC
from ssd1306 import SSD1306_SPI
import time
from GuiBuilder import GuiBuilder
from usbridge import USBridge
from utime import sleep_ms

turnOffScreen = 0

#begin functions
def main():

    if turnOffScreen: return
    guiBuilder.showLogo()

    #timer_start = time.ticks_ms()

    while True:
        try:
            #if((time.ticks_ms() - timer_start) > 1000):
                #print("tick tock")
                #timer_start = time.ticks_ms()

            oled.text("test",15,30)
            oled.pixel(0,0,1)
            oled.pixel(10,10,1)

            serialMsg = usbridge.pollInput()
            if(serialMsg != "" and len(serialMsg) > 1):
                print("#" + serialMsg)	#hack for flushing
                
            oled.show()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    
    # use these to initialize time and print to user
    # we can save energy by using lower work count
    # clock = RTC()
    # clock.datetime((2025, 12, 24, 0, 1, 12, 48, 0))
    
    spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
    oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16)) #WIDTH, HEIGHT, spi, dc,rst, cs
    oled.fill(0) # clear the OLED
    oled.contrast(180)
    guiBuilder = GuiBuilder(oled,["top","kek"])
    usbridge = USBridge()
    
    main()

### avoid using threading unless good option
### idea is to go into usbridge -> poll
### and if data present hand that to SystemHud

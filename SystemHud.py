from machine import Pin, SPI, Timer, RTC
from ssd1306 import SSD1306_SPI
import time
from GuiBuilder import GuiBuilder
from usbridge import USBridge
from utime import sleep_ms

#begin functions
def main():

    #timer_start = time.ticks_ms()
    guiBuilder.initAnimation()
    sleep_ms(2000)
    while True:
        try:
            #periodically update ? maybe just scratch
            #if((time.ticks_ms() - timer_start) > 1000):
                #print("tick tock")
                #timer_start = time.ticks_ms()

            oled.text("HELLO_FRIEND",15,30)
            oled.pixel(0,0,1)
            oled.pixel(10,10,1)

            serialMsg = usbridge.read()
            if(serialMsg != ""):
                print(serialMsg)
                
            oled.show()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    
    # use these to initialize time and print to user
    # clock = RTC()
    # clock.datetime((2025, 12, 24, 0, 1, 12, 48, 0))
    
    spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
    oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16)) #WIDTH, HEIGHT, spi, dc,rst, cs
    oled.rotate(180)
    guiBuilder = GuiBuilder(oled)
    usbridge = USBridge()
    
    main()

### avoid using threading unless good option
### idea is to go into usbridge -> poll
### and if data present hand that to SystemHud

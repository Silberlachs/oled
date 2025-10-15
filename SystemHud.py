from machine import Pin, SPI
from ssd1306 import SSD1306_SPI
import framebuf
from GuiBuilder import GuiBuilder
from usbridge import USBridge
from utime import sleep_ms

#begin functions
def main():

    guiBuilder.showArgs()
    while True:
        try: 
            oled.fill(0)
            oled.show()
            oled.text("HELLO_FRIEND",0,0)
            oled.show()
            sleep_ms(15)
            usbridge.read()
        except KeyboardInterrupt:
            break
  
  

if __name__ == "__main__":
    
    spi = SPI(0, 100000, mosi=Pin(19), sck=Pin(18))
    oled = SSD1306_SPI(128, 64, spi, Pin(17),Pin(20), Pin(16)) #WIDTH, HEIGHT, spi, dc,rst, cs
    oled.rotate(180)
    guiBuilder = GuiBuilder(["CPU_H", "RAM_%", "HEAT"])
    usbridge = USBridge()
    
    main()

### avoid using threading unless good option
### idea is to go into usbridge -> poll
### and if data present hand that to SystemHud
